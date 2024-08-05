package com.oxygen.publisher.model;

import java.util.ArrayList;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

public class TypeSegmentTest {

  TypeSegment typeSegment = new TypeSegment();
  List<ModuleDataItem> events = new ArrayList<>();

  @Before
  public void setUp() {
    events.add(new ModuleDataItem());
  }

  @Test
  public void cloneWithEmptyTypesCheck() {
    typeSegment.toString();
    TypeSegment typeSeg = typeSegment.cloneWithEmptyTypes();
    Assert.assertNotNull(typeSeg);
  }

  @Test
  public void cloneWithEmptyHRTypesCheck() {
    typeSegment.setEvents(events);
    TypeSegment typeSeg = typeSegment.cloneWithEmptyHRTypes();
    Assert.assertNotNull(typeSeg.getEvents());
  }
}
