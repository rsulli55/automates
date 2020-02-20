package org.clulab.aske.automates.apps
import org.clulab.serialization.json._
import java.io.File
import java.io.FileWriter
import java.io.BufferedWriter

import org.clulab.processors.corenlp.CoreNLPProcessor
import ai.lum.common.ConfigUtils._
import com.typesafe.config.{Config, ConfigFactory}
import org.clulab.aske.automates.data.{DataLoader, TextRouter}
import org.clulab.aske.automates.OdinEngine
import org.clulab.utils.{DisplayUtils, FileUtils, Serializer}
import org.clulab.odin.Mention
import org.clulab.odin.serialization.json.JSONSerializer
import org.clulab.processors.Document
import org.clulab.serialization.DocumentSerializer
import org.json4s
import org.json4s.JValue
import org.json4s.jackson.JsonMethods._

/**
  * App used to extract mentions from files in a directory and produce the desired output format (i.e., serialized
  * mentions or any other format we may need).  The input and output directories as well as the desired export
  * formats are specified in the config file (located in src/main/resources).
  * This makes ONE output file for each of the input files.
  */
object ExtractDoc extends App {

  def getExporter(exporterString: String, filename: String): Exporter = {
    exporterString match {
      case "serialized" => SerializedExporter(filename)
      case "json" => JSONExporter(filename)
      case _ => throw new NotImplementedError(s"Export mode $exporterString is not supported.")
    }
  }

  val config = ConfigFactory.load()


  val inputDir = "/home/alexeeva/Desktop/automatesLiteratureToIndex/sci-par-jsons"
  val outputDir = config[String]("apps.outputDirectory")
  val inputType = config[String]("apps.inputType")
  val dataLoader = DataLoader.selectLoader(inputType) // pdf, txt or json are supported, and we assume json == science parse json
  val exportAs: List[String] = config[List[String]]("apps.exportAs")
  val files = FileUtils.findFiles(inputDir, dataLoader.extension)
  val reader = OdinEngine.fromConfig(config[Config]("TextEngine"))
  val proc = new CoreNLPProcessor()
  val serializer = new DocumentSerializer
  val exporter = new JSONDocExporter()

  //uncomment these for using the text/comment router
//  val commentReader = OdinEngine.fromConfig(config[Config]("CommentEngine"))
//  val textRouter = new TextRouter(Map(TextRouter.TEXT_ENGINE -> reader, TextRouter.COMMENT_ENGINE -> commentReader))

  // For each file in the input directory:
  files.par.foreach { file =>
    // 1. Open corresponding output file and make all desired exporters
    println(s"Extracting from ${file.getName}")
    // 2. Get the input file contents
    // note: for science parse format, each text is a section
    val text = dataLoader.loadFile(file).mkString(" ")
    // 3. Extract causal mentions from the texts
    // todo: here I am choosing to pass each text/section through separately -- this may result in a difficult coref problem
//    val mentions = texts.flatMap(reader.extractFromText(_, filename = Some(file.getName)))
    //The version of mention that includes routing between text vs. comment
//    val mentions = texts.flatMap(text => textRouter.route(text).extractFromText(text, filename = Some(file.getName))).seq

    val document = proc.annotate(text)
//    serializer.save(document)
    val json = document.json(pretty = true)
//    println(json)
    println(file.toString())
    val newFileName = file.toString().replace(".json", "_seralized").replace("sci-par-jsons", "docs_serialized")
    exporter.export(json, newFileName)


//    exportAs.foreach { format =>
//        val exporter = getExporter(format, s"$outputDir/${file.getName}")
//        exporter.export(mentions)
//        exporter.close() // close the file when you're done
//    }



  }
}

case class JSONDocExporter()  {
    def export(str: String, filename: String): Unit = {

    val file = new File(filename + ".json")
    val bw = new BufferedWriter(new FileWriter(file))
    bw.write(str)
    bw.close()
  }

  def close(): Unit = ()
}
//trait Exporter {
//  def export(mentions: Seq[Mention]): Unit
//  def close(): Unit // for closing the file, if needed
//}


//case class SerializedExporter(filename: String) extends Exporter {
//  override def export(mentions: Seq[Mention]): Unit = {
//    Serializer.save[SerializedMentions](new SerializedMentions(mentions), filename + ".serialized")
//  }
//
//  override def close(): Unit = ()
//}
//
//case class JSONExporter(filename: String) extends Exporter {
//  override def export(mentions: Seq[Mention]): Unit = {
//    val ast = JSONSerializer.jsonAST(mentions)
//    val text = compact(render(ast))
//    val file = new File(filename + ".json")
//    val bw = new BufferedWriter(new FileWriter(file))
//    bw.write(text)
//    bw.close()
//  }
//
//  override def close(): Unit = ()
//}
//
//// Helper Class to facilitate serializing the mentions
//@SerialVersionUID(1L)
//class SerializedMentions(val mentions: Seq[Mention]) extends Serializable {}
//object SerializedMentions {
//  def load(file: File): Seq[Mention] = Serializer.load[SerializedMentions](file).mentions
//  def load(filename: String): Seq[Mention] = Serializer.load[SerializedMentions](filename).mentions
//}
//
//
//object ExporterUtils {
//
//  def removeTabAndNewline(s: String) = s.replaceAll("(\\n|\\t)", " ")
//}
