package com.ladbrokescoral.oxygen.cms.util;

import java.util.List;
import java.util.Map;

public class NestedObject {

  String string;
  List<String> stringList;
  Map<String, String> stringMap;

  public NestedObject() {
    super();
  }

  public String getString() {
    return string;
  }

  public void setString(String string) {
    this.string = string;
  }

  public List<String> getStringList() {
    return stringList;
  }

  public void setStringList(List<String> stringList) {
    this.stringList = stringList;
  }

  public Map<String, String> getStringMap() {
    return stringMap;
  }

  public void setStringMap(Map<String, String> stringMap) {
    this.stringMap = stringMap;
  }
}
