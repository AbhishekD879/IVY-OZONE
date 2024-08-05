package com.ladbrokescoral.oxygen.cms.util;

import java.util.List;
import java.util.Map;

public class TestObject {

  String test;
  List<String> stringList;
  List<NestedObject> nestedList;
  Map<String, String> stringMap;
  NestedObject nestedObject;
  int number;

  public String getTest() {
    return test;
  }

  public void setTest(String test) {
    this.test = test;
  }

  public List<String> getStringList() {
    return stringList;
  }

  public void setStringList(List<String> stringList) {
    this.stringList = stringList;
  }

  public List<NestedObject> getNestedList() {
    return nestedList;
  }

  public void setNestedList(List<NestedObject> nestedList) {
    this.nestedList = nestedList;
  }

  public Map<String, String> getStringMap() {
    return stringMap;
  }

  public void setStringMap(Map<String, String> stringMap) {
    this.stringMap = stringMap;
  }

  public NestedObject getNestedObject() {
    return nestedObject;
  }

  public void setNestedObject(NestedObject nestedObject) {
    this.nestedObject = nestedObject;
  }

  public int getNumber() {
    return number;
  }

  public void setNumber(int number) {
    this.number = number;
  }
}
