package org.clulab.aske.automates

import com.typesafe.config.Config
import com.typesafe.config.ConfigFactory
import org.clulab.odin.{ExtractorEngine, Mention, State}
import org.clulab.processors.{Document, Processor, Sentence}
import org.clulab.processors.fastnlp.FastNLPProcessor
import org.clulab.aske.automates.entities.{EntityFinder, GrobidEntityFinder, RuleBasedEntityFinder, StringMatchEntityFinder}
import org.clulab.sequences.LexiconNER
import org.clulab.utils.{DocumentFilter, FileUtils, FilterByLength, PassThroughFilter}
import org.slf4j.LoggerFactory
import ai.lum.common.ConfigUtils._
import org.clulab.aske.automates.actions.ExpansionHandler



class OdinEngine(
  val proc: Processor,
  masterRulesPath: String,
  taxonomyPath: String,
  val entityFinders: Seq[EntityFinder],
  val lexiconNER: Option[LexiconNER],
  enableExpansion: Boolean,
  filterType: Option[String]) {

  // Initial State for Odin
  // todo: cleaner way than a var?
  private var initialState = new State()

  val documentFilter: DocumentFilter = filterType match {
    case None => PassThroughFilter()
    case Some("length") => FilterByLength(proc, cutoff = 150)
    case _ => throw new NotImplementedError(s"Invalid DocumentFilter type specified: $filterType")
  }

  class LoadableAttributes(
    // These are the values which can be reloaded.  Query them for current assignments.
    val actions: OdinActions,
    val engine: ExtractorEngine,
  )

  object LoadableAttributes {

    def apply(): LoadableAttributes = {
      // Reread these values from their files/resources each time based on paths in the config file.
      val masterRules = FileUtils.getTextFromResource(masterRulesPath)
      val actions = OdinActions(taxonomyPath, enableExpansion)
      val extractorEngine = ExtractorEngine(masterRules, actions, actions.globalAction)

      new LoadableAttributes(
        actions,
        extractorEngine
      )
    }
  }

  var loadableAttributes = LoadableAttributes()

  // These public variables are accessed directly by clients which
  // don't know they are loadable and which had better not keep copies.
  def engine = loadableAttributes.engine
  def reload() = loadableAttributes = LoadableAttributes()

  // Accessor Method for initial state
  def updateInitialState(ms: Seq[Mention]) = initialState = initialState.updated(ms)
  def resetInitialState(ms: Seq[Mention]) = initialState = State(ms)

  // MAIN PIPELINE METHOD
  def extractFromText(text: String, keepText: Boolean = false, filename: Option[String]): Seq[Mention] = {
    val doc = annotate(text, keepText, filename)   // CTM: processors runs (sentence splitting, tokenization, POS, dependency parse, NER, chunking)
    val odinMentions = OdinActions.deleteDuplicates(extractFrom(doc))  //extractFrom(doc)  // CTM: runs the Odin grammar
    //println(s"\nodinMentions() -- entities : \n\t${odinMentions.map(m => m.text).sorted.mkString("\n\t")}")

    odinMentions  // CTM: collection of mentions ; to be converted to some form (json)
  }


  def extractFrom(doc: Document): Vector[Mention] = {
    // Add any mentions from the entityFinders to the initial state
    if (entityFinders.nonEmpty) {
      println("Using EFs")
      initialState = initialState.updated(entityFinders.flatMap(ef => ef.extract(doc)))
    }
//     println(s"In extractFrom() -- res : ${initialState.allMentions.map(m => m.text).mkString(",\t")}")

    // Run the main extraction engine, pre-populated with the initial state
    val events =  engine.extractFrom(doc, initialState).toVector
    //println(s"In extractFrom() -- res : ${res.map(m => m.text).mkString(",\t")}")

    // todo: some appropriate version of "keepMostComplete"
    loadableAttributes.actions.keepLongest(events).toVector
  }

  // ---------- Helper Methods -----------

  // Annotate the text using a Processor and then populate lexicon labels
  def annotate(text: String, keepText: Boolean = false, filename: Option[String]= None): Document = {
    val tokenized = proc.mkDocument(text, keepText = true)  // Formerly keepText, must now be true
    val filtered = documentFilter.filter(tokenized)         // Filter noise from document if enabled (else "pass through")
    val doc = proc.annotate(filtered)
    if (lexiconNER.nonEmpty) {           // Add any lexicon/gazetteer tags
      doc.sentences.foreach(addLexiconNER)
    }
    doc.id = filename
    doc
  }

  // Add tags to flag tokens that are found in the provided lexicons/gazetteers
  protected def addLexiconNER(s: Sentence) = {
    // Not all parsers generate entities (e.g., Portuguese clulab processor), so we want to create an empty list here
    // for further processing and filtering operations that expect to be able to query the entities
    if (s.entities.isEmpty) s.entities = Some(Array.fill[String](s.words.length)("O"))
    for {
      (lexiconNERTag, i) <- lexiconNER.get.find(s).zipWithIndex
      if lexiconNERTag != OdinEngine.NER_OUTSIDE
    } s.entities.get(i) = lexiconNERTag
  }

}

object OdinEngine {

  // todo: ability to load/use diff processors
  lazy val proc: Processor = new FastNLPProcessor()

  // Mention labels
  val DEFINITION_LABEL: String = "Definition"
  val INTERVAL_PARAMETER_SETTING_LABEL: String = "IntervalParameterSetting"
  val PARAMETER_SETTING_LABEL: String = "ParameterSetting"
  val VALUE_LABEL: String = "Value"
  val VARIABLE_LABEL: String = "Variable"
  // Mention argument types
  val VARIABLE_ARG: String = "variable"
  val VALUE_LEAST_ARG: String = "ValueLeast"
  val VALUE_MOST_ARG: String = "ValueMost"
  val DEFINITION_ARG: String = "definition"
  val VALUE_ARG: String = "value"

  val logger = LoggerFactory.getLogger(this.getClass())
  // Used by LexiconNER
  val NER_OUTSIDE = "O"

  def fromConfig(odinConfig: Config = ConfigFactory.load("automates")[Config]("TextEngine")): OdinEngine = {
//    // The config with the main settings
//    val odinConfig: Config = config[Config]("TextEngine")

    // document filter: used to clean the input ahead of time
    // fixme: should maybe be moved?
    val filterType = odinConfig.get[String]("documentFilter")

    // Odin Grammars
    val masterRulesPath: String = odinConfig[String]("masterRulesPath")
    val taxonomyPath: String = odinConfig[String]("taxonomyPath")

    // EntityFinders: used to find entities ahead of time
    val enableEntityFinder: Boolean = odinConfig.get[Boolean]("entityFinder.enabled").getOrElse(false)
    val entityFinders: Seq[EntityFinder] = if (enableEntityFinder) {
      val entityFinderConfig: Config = odinConfig[Config]("entityFinder")
      val finderTypes: List[String] = entityFinderConfig[List[String]]("finderTypes")
      finderTypes.map(finderType => EntityFinder.loadEntityFinder(finderType, entityFinderConfig))
    } else Seq.empty[EntityFinder]

    // LexiconNER: Used to annotate the documents with info from a gazetteer
    val enableLexiconNER: Boolean = odinConfig.get[Boolean]("lexiconNER.enable").getOrElse(false)
    val lexiconNER = if(enableLexiconNER) {
      val lexiconNERConfig = odinConfig[Config]("lexiconNER")
      val lexicons = lexiconNERConfig[List[String]]("lexicons")
      Some(LexiconNER(lexicons, caseInsensitiveMatching = true))
    } else None

    // expansion: used to optionally expand mentions in certain situations to get more complete text spans
    val enableExpansion: Boolean = odinConfig[Boolean]("enableExpansion")

    new OdinEngine(proc, masterRulesPath, taxonomyPath, entityFinders, lexiconNER, enableExpansion, filterType)
  }

}
