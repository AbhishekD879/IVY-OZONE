package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.stream.Stream;

public enum PageType {
  sport(Integer.class, ""),
  eventhub(String.class, "h"),
  home(String.class, ""),
  edp(String.class, ""),
  customized(String.class, "c");

  private Class<?> idType;
  private String prefix;

  private PageType(Class<?> type, String prefix) {
    this.idType = type;
    this.prefix = prefix;
  }

  public String getPrefix() {
    return prefix;
  }

  public Class<?> getIdType() {
    return idType;
  }

  public static Stream<PageType> stream() {
    return Stream.of(PageType.values());
  }
}
