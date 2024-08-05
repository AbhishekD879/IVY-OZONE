package com.oxygen.publisher.model;

import org.junit.Before;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;

public class ModuleDataItemTest {

  ModuleDataItem moduleDataItem = new ModuleDataItem();

  @Before
  public void setUp() {
    moduleDataItem.setId(123);
  }

  @Test
  public void cloneWithEmptyHREventTypesCheck() {
    ModuleDataItem response = moduleDataItem.cloneWithEmptyHREventTypes();
    Assertions.assertEquals(123, response.getId());
  }

  @Test
  public void hashcodeEqualsTest() {
    moduleDataItem.setId(123);
    moduleDataItem.equals(moduleDataItem);
    moduleDataItem.hashCode();
    moduleDataItem.getPrimaryMarkets();
    Assertions.assertNull(moduleDataItem.getPrimaryMarkets());
  }

  @Test
  public void EmptyEqualsTest() {
    ModuleDataItem dataItem = null;
    moduleDataItem.equals(dataItem);
    Assertions.assertNull(dataItem);
  }

  @Test
  public void NotEqualsTest() {
    ModuleDataItem dataItem = new ModuleDataItem();
    dataItem.setId(123);
    moduleDataItem.equals(dataItem);
    Assertions.assertEquals(moduleDataItem.getId(), dataItem.getId());
  }

  @Test
  public void EqualsTest() {
    ModuleDataItem dataItem = new ModuleDataItem();
    dataItem.setCategoryId("21");
    moduleDataItem.setCategoryId("12");
    boolean flag = moduleDataItem.equals(dataItem);
    Assertions.assertEquals(false, flag);
  }
}
