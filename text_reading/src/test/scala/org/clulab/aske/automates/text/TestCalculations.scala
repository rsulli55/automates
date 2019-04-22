package org.clulab.aske.automates.text

import org.clulab.aske.automates.TestUtils._

class TestCalculations extends ExtractionTest {

  // Tests from paper: 2017-IMPLEMENTING STANDARDIZED REFERENCE EVAPOTRANSPIRATION AND DUAL CROP COEFFICIENT APPROACH IN THE DSSAT CROPPING SYSTEM MODEL

  val t1a = "The average soil water potential ( S , J kg−1) is calculated based on a representative root length fraction for each soil layer (fr,j):"
  passingTest should s"extract calculations from t1a: ${t1a}" taggedAs (Somebody) in {
    val desired = Seq(
      "S" -> Seq("representative root length fraction")
    )
    val mentions = extractMentions(t1a)
    testCalculationEvent(mentions, desired)
  }

}