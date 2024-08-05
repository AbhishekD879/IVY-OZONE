package com.ladbrokescoral.oxygen.notification.entities.dto;

import java.util.Collections;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public enum Platform {
  IOS("ios"),
  ANDROID("android"),
  HELIUM_IOS("helium_ios"),
  HELIUM_ANDROID("helium_android");

  private String name;

  private static final Map<String, Platform> ENUM_MAP;

  Platform(String name) {
    this.name = name;
  }

  public String getName() {
    return this.name;
  }

  static {
    Map<String, Platform> map = new ConcurrentHashMap<String, Platform>();
    for (Platform instance : Platform.values()) {
      map.put(instance.getName(), instance);
    }
    ENUM_MAP = Collections.unmodifiableMap(map);
  }

  public static Platform get(String name) {
    return ENUM_MAP.get(name);
  }
}
