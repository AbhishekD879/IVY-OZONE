package com.oxygen.publisher.sportsfeatured.model;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

public class PageRawIndexTest {

  @Test
  public void createIndex() {
    assertEquals("sport::0", PageRawIndex.forSport(0).toString());
    assertEquals("sport::10", PageRawIndex.forSport(10).toString());
    assertEquals("eventhub::5", PageRawIndex.forHub("h5").toString());
    assertEquals("eventhub::5", PageRawIndex.fromPageId("h5").toString());
    assertEquals("sport::5", PageRawIndex.fromPageId("5").toString());
  }

  @Test
  public void createIndexFromGenerationId() {
    assertEquals("sport::0", PageRawIndex.fromGenerationId("sport::0::469444").toString());
    assertEquals("sport::16", PageRawIndex.fromGenerationId("sport::16::469444").toString());
    assertEquals("eventhub::5", PageRawIndex.fromGenerationId("eventhub::h5::469444").toString());
  }

  @Test
  public void socketTest() {
    assertEquals("sport::16", PageRawIndex.fromGenerationId("sport::16::469444").toString());
  }
}
