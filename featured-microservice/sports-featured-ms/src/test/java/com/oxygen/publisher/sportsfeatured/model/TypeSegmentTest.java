package com.oxygen.publisher.sportsfeatured.model;

import com.oxygen.publisher.model.ModuleDataItem;
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.TypeSegment;
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
    String typeSeg = typeSegment.toString();
    Assert.assertNotNull(typeSeg);
  }
}
