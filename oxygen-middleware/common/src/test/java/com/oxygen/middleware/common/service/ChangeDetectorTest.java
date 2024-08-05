package com.oxygen.middleware.common.service;

import com.coral.oxygen.middleware.JsonFacade;
import com.coral.oxygen.middleware.common.service.ChangeDetector;
import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.IdHolder;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.google.gson.Gson;
import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import org.junit.Assert;
import org.junit.Ignore;
import org.junit.Test;

@Deprecated
@Ignore
public class ChangeDetectorTest {

  @Test
  public void testChanged() {
    ForTest v1 = new ForTest();
    ForTest v2 = new ForTest();
    v1.setA(1);
    v2.setA(2);

    Assert.assertTrue(ChangeDetector.changeDetected(v1, v2));
  }

  @Test
  public void testChangedSubObject() {
    ForTest v1 = new ForTest();
    ForTest v2 = new ForTest();
    v1.setSubObject(new ForTest());
    v2.setSubObject(new ForTest());
    v1.getSubObject().setA(1);
    v2.getSubObject().setA(2);

    Assert.assertTrue(ChangeDetector.changeDetected(v1, v2));
  }

  @Test
  public void testChangedCollectionKeys() {
    ForTest v1 = new ForTest();
    ForTest v2 = new ForTest();
    v1.setCollection(new ArrayList<>());
    v2.setCollection(new LinkedList<>());
    v1.getCollection().add(new ForTest());
    v2.getCollection().add(new ForTest());
    v1.getCollection().get(0).setA(1);
    v2.getCollection().get(0).setA(2);

    Assert.assertTrue(ChangeDetector.changeDetected(v1, v2));
  }

  @Test
  public void testChangedCollectionKeysWithEmptyCollection() {
    ForTest v1 = new ForTest();
    ForTest v2 = new ForTest();
    v1.setCollection(new ArrayList<>());
    v2.setCollection(new LinkedList<>());
    v1.getCollection().add(new ForTest());
    v1.getCollection().get(0).setA(1);

    Assert.assertTrue(ChangeDetector.changeDetected(v1, v2));
  }

  @Test
  public void testChangedCollectionContent() {
    ForTest v1 = new ForTest();
    ForTest v2 = new ForTest();
    v1.setCollection(new ArrayList<>());
    v2.setCollection(new LinkedList<>());
    v1.getCollection().add(new ForTest());
    v2.getCollection().add(new ForTest());
    v1.getCollection().get(0).setA(1);
    v2.getCollection().get(0).setA(1);
    v1.getCollection().get(0).setSubObject(new ForTest());
    v2.getCollection().get(0).setSubObject(new ForTest());
    v1.getCollection().get(0).getSubObject().setA(10);
    v2.getCollection().get(0).getSubObject().setA(20);

    Assert.assertTrue(ChangeDetector.changeDetected(v1, v2));

    v2.getCollection().get(0).getSubObject().setA(10);

    Assert.assertFalse(ChangeDetector.changeDetected(v1, v2));
    Assert.assertFalse(ChangeDetector.changeDetected(v1, v2, true));

    v1.setMinorCollection(new ArrayList<>());
    v2.setMinorCollection(new LinkedList<>());
    v1.getMinorCollection().add(new ForTest());
    v2.getMinorCollection().add(new ForTest());
    v1.getMinorCollection().get(0).setA(1);
    v2.getMinorCollection().get(0).setA(1);
    v1.getMinorCollection().get(0).setSubObject(new ForTest());
    v2.getMinorCollection().get(0).setSubObject(new ForTest());
    v1.getMinorCollection().get(0).getSubObject().setA(10);
    v2.getMinorCollection().get(0).getSubObject().setA(20);

    Assert.assertFalse(ChangeDetector.changeDetected(v1, v2));
    Assert.assertTrue(ChangeDetector.changeDetected(v1, v2, true));
  }

  @Test
  public void testNotChanged() {
    ForTest v1 = new ForTest();
    ForTest v2 = new ForTest();
    v1.setA(1);
    v2.setA(1);
    v1.setB(2);
    v2.setB(3);

    Assert.assertFalse(ChangeDetector.changeDetected(v1, v2));
  }

  public class ForTest implements IdHolder {

    private int a;

    private int b;

    private ForTest subObject;

    private List<ForTest> collection;

    private List<ForTest> minorCollection;

    @ChangeDetect
    public int getA() {
      return a;
    }

    public void setA(int a) {
      this.a = a;
    }

    public int getB() {
      return b;
    }

    public void setB(int b) {
      this.b = b;
    }

    @ChangeDetect(compareNestedObject = true)
    public ForTest getSubObject() {
      return subObject;
    }

    public void setSubObject(ForTest subObject) {
      this.subObject = subObject;
    }

    @ChangeDetect(compareCollection = true)
    public List<ForTest> getCollection() {
      return collection;
    }

    public void setCollection(List<ForTest> collection) {
      this.collection = collection;
    }

    @ChangeDetect(compareCollection = true, minor = true)
    public List<ForTest> getMinorCollection() {
      return minorCollection;
    }

    public void setMinorCollection(List<ForTest> minorCollection) {
      this.minorCollection = minorCollection;
    }

    @Override
    public String idForChangeDetection() {
      return String.valueOf(a);
    }
  }

  enum MODELS {
    SPORT_SEGEMENT("SportSegment0.json", "SportSegment1.json");

    private final String source1;
    private final String source2;

    MODELS(String fileName1, String fileName2) {
      try {
        Path resource = Paths.get(ClassLoader.getSystemResource(fileName1).toURI());
        this.source1 = new String(Files.readAllBytes(resource));
        Path resource1 = Paths.get(ClassLoader.getSystemResource(fileName2).toURI());
        this.source2 = new String(Files.readAllBytes(resource1));

      } catch (IOException | URISyntaxException e) {
        throw new RuntimeException(e);
      }
    }

    public String getSource1() {
      return source1;
    }

    public String getSource2() {
      return source2;
    }
  }

  @Test
  public void compareSportSegment_onMarketChanges_Detected() {
    Gson gson = JsonFacade.GSON;
    SportSegment segment1 = gson.fromJson(MODELS.SPORT_SEGEMENT.getSource1(), SportSegment.class);
    SportSegment segment2 = gson.fromJson(MODELS.SPORT_SEGEMENT.getSource2(), SportSegment.class);
    Assert.assertFalse(ChangeDetector.changeDetected(segment1, segment2));
  }
}
