package org.clulab.aske.automates.text

import org.clulab.aske.automates.TestUtils._

class TestFunctions extends ExtractionTest {

  // Tests from paper: ASCE-2005-The ASCE Standardized Reference-TechReport-petasce

  val t1a = "Rnl, net long-wave radiation, is the difference between upward long-wave radiation from the standardized surface (Rlu) and downward long-wave radiation from the sky (Rld),"
  passingTest should s"find functions from t1a: ${t1a}" taggedAs(Somebody) in {
    val desired = Seq(
      "Rnl" -> Seq("difference between upward long-wave radiation from the standardized surface", "downward long-wave radiation from the sky")
    )
    val mentions = extractMentions(t1a)
    testFunctionEvent(mentions, desired)
  }


  // Tests from paper: ASCE-2005-The ASCE Standardized Reference-TechReport-petasce
  // todo: "Rnl, net long-wave radiation, is the difference between upward long-wave radiation from the standardized surface (Rlu) and downward long-wave radiation from the sky (Rld),"
 
  // todo: "Similar to equation 2, E0 is calculated as the product of Kcd and ETpm." (example from TestDefinitions)

  // Tests from COVID_ACT_NOW
  // todo: "Initial conditions for total cases and total exposed are calculated by dividing hospitalizations by the hospitalization rate."
  // todo: "The default infection propagation rate ( β mild ) used in this model is an US average extracted from actual death data."
  // todo: "Cases estimated by multiplying confirmed cases by 20."


  // Tests from CHIME-online-manual
  // todo: "which is the transmissibility τ multiplied by the average number of people exposed c."
  // todo: "γ is the inverse of the mean recovery time, in days."
  // 


}