package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.HashMap;
import java.util.Map;

/** ConfigurationMapDto */
public class ConfigurationMapDto {

  private Map<String, Map<String, String>> configurationMap;

  public ConfigurationMapDto() {
    configurationMap = new HashMap<>();
  }

  public ConfigurationMapDto put(String key0, String key1, String value) {
    if (!configurationMap.containsKey(key0)) {
      configurationMap.put(key0, new HashMap<>());
    }

    configurationMap.get(key0).put(key1, value);

    return this;
  }
}
