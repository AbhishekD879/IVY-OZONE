package com.ladbrokescoral.oxygen.questionengine.configuration;

import com.fasterxml.jackson.databind.util.StdConverter;

import java.util.LinkedHashMap;
import java.util.Map;

public class LinkedHashMapConverter extends StdConverter<Map<?, ?>, Map<?, ?>> {

  @Override
  public Map<?, ?> convert(Map<?, ?> value) {
    return new LinkedHashMap<>(value);
  }
}
