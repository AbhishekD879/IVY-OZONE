package com.oxygen.middleware.common.service

import com.coral.oxygen.middleware.common.service.ChangeDetector
import com.coral.oxygen.middleware.pojos.model.ChangeDetect
import com.coral.oxygen.middleware.pojos.model.IdHolder
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import com.google.gson.GsonBuilder
import spock.lang.Ignore
import spock.lang.Specification

import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths

@Ignore
class ChangeDetectorSpec extends Specification {

  def "Test Changed"(){

    given:
    def v1 = new ForTest()
    def v2 = new ForTest()

    when:
    v1.setA(1)
    v2.setB(2)

    then:
    ChangeDetector.changeDetected(v1,v2)
  }

  def "Test SubObject Changed"(){

    given:
    def v1 = new ForTest()
    def v2 = new ForTest()

    when:
    v1.setSubObject(new ForTest())
    v2.setSubObject(new ForTest())
    v1.getSubObject().setA(1)
    v2.getSubObject().setA(2)

    then:
    ChangeDetector.changeDetected(v1,v2)
  }

  def "Test Changed Collection Keys"() {
    given:
    def v1 = new ForTest()
    def v2 = new ForTest()

    when:
    v1.setCollection(new ArrayList<>())
    v2.setCollection(new LinkedList<>())
    v1.getCollection().add(new ForTest())
    v2.getCollection().add(new ForTest())
    v1.getCollection().get(0).setA(1)
    v2.getCollection().get(0).setA(2)

    then:
    ChangeDetector.changeDetected(v1, v2)
  }

  def "Test Collection Keys With Empty Collection"() {
    given:
    def v1 = new ForTest()
    def v2 = new ForTest()

    when:
    v1.setCollection(new ArrayList<>())
    v2.setCollection(new LinkedList<>())
    v1.getCollection().add(new ForTest())
    v1.getCollection().get(0).setA(1)

    then:
    ChangeDetector.changeDetected(v1, v2)
  }

  def "Test Changed collection content"() {
    given:
    def v1 = new ForTest()
    def v2 = new ForTest()

    when:
    v1.setCollection(new ArrayList<>())
    v2.setCollection(new LinkedList<>())
    v1.getCollection().add(new ForTest())
    v2.getCollection().add(new ForTest())
    v1.getCollection().get(0).setA(1)
    v2.getCollection().get(0).setA(1)
    v1.getCollection().get(0).setSubObject(new ForTest())
    v2.getCollection().get(0).setSubObject(new ForTest())
    v1.getCollection().get(0).getSubObject().setA(10)
    v2.getCollection().get(0).getSubObject().setA(20)

    then:
    ChangeDetector.changeDetected(v1, v2)

    when:
    v2.getCollection().get(0).getSubObject().setA(10)

    then:
    !ChangeDetector.changeDetected(v1, v2)
    !ChangeDetector.changeDetected(v1, v2, true)

    when:
    v1.setMinorCollection(new ArrayList<>())
    v2.setMinorCollection(new LinkedList<>())
    v1.getMinorCollection().add(new ForTest())
    v2.getMinorCollection().add(new ForTest())
    v1.getMinorCollection().get(0).setA(1)
    v2.getMinorCollection().get(0).setA(1)
    v1.getMinorCollection().get(0).setSubObject(new ForTest())
    v2.getMinorCollection().get(0).setSubObject(new ForTest())
    v1.getMinorCollection().get(0).getSubObject().setA(10)
    v2.getMinorCollection().get(0).getSubObject().setA(20)

    then:
    !ChangeDetector.changeDetected(v1, v2)
    ChangeDetector.changeDetected(v1, v2, true)
  }

  def "Test Not Changed"() {
    given:
    def v1 = new ForTest()
    def v2 = new ForTest()

    when:
    v1.setA(1)
    v2.setA(1)
    v1.setB(2)
    v2.setB(3)

    then:
    !ChangeDetector.changeDetected(v1, v2)
  }

  def "Compare Sport Segments OnMarket Change Detected"() {
    given:
    def gson = new GsonBuilder().create()
    def segment1 = gson.fromJson(MODELS.SPORT_SEGEMENT.getSource1(), SportSegment.class)
    def segment2 = gson.fromJson(MODELS.SPORT_SEGEMENT.getSource2(), SportSegment.class)

    expect:
    !ChangeDetector.changeDetected(segment1, segment2)
  }

  def "Compare Empty Sport Segments"() {
    expect:
    !ChangeDetector.changeDetected(new SportSegment(), new SportSegment())
  }

  // ---------- helpers --------
  class ForTest implements IdHolder {

    int a
    int b
    ForTest subObject
    List<ForTest> collection
    List<ForTest> minorCollection

    @ChangeDetect
    int getA() {
      return a
    }

    void setA(int a) {
      this.a = a
    }

    int getB() {
      return b
    }

    void setB(int b) {
      this.b = b
    }

    @ChangeDetect(compareNestedObject = true)
    ForTest getSubObject() {
      return subObject
    }

    void setSubObject(ForTest subObject) {
      this.subObject = subObject
    }

    @ChangeDetect(compareCollection = true)
    List<ForTest> getCollection() {
      return collection
    }

    void setCollection(List<ForTest> collection) {
      this.collection = collection
    }

    @ChangeDetect(compareCollection = true, minor = true)
    List<ForTest> getMinorCollection() {
      return minorCollection
    }

    void setMinorCollection(List<ForTest> minorCollection) {
      this.minorCollection = minorCollection
    }

    @Override
    String idForChangeDetection() {
      return String.valueOf(a)
    }

  }


  enum MODELS {
    SPORT_SEGEMENT("SportSegment0.json", "SportSegment1.json")


    final String source1
    final String source2

    MODELS(String fileName1, String fileName2) {
      try {
        Path resource = Paths.get(ClassLoader.getSystemResource(fileName1).toURI())
        this.source1 = new String(Files.readAllBytes(resource))
        Path resource1 = Paths.get(ClassLoader.getSystemResource(fileName2).toURI())
        this.source2 = new String(Files.readAllBytes(resource1))

      } catch (IOException | URISyntaxException e) {
        throw new RuntimeException(e)
      }
    }

    String getSource1() {
      return source1
    }

    String getSource2() {
      return source2
    }

  }
}
