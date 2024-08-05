package com.coral.oxygen.middleware.common.utils;

import com.coral.oxygen.middleware.common.exceptions.InvalidConfigurationException;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Type;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Component;

@Component
public class OrdinalToNumberConverter implements Converter<String, Integer> {

  private Map<String, Integer> ordinalNumbersMap;

  @Autowired
  public OrdinalToNumberConverter(
      @Value("${common.ordinalToNumber.json}") Resource ordinalNumbersJson, Gson gson) {
    try (InputStreamReader ordinalNumberReader =
        new InputStreamReader(ordinalNumbersJson.getInputStream())) {
      Type type = new TypeToken<Map<String, Integer>>() {}.getType();
      ordinalNumbersMap = gson.fromJson(ordinalNumberReader, type);
    } catch (IOException e) {
      throw new InvalidConfigurationException("Error parsing ordinal numbers json file", e);
    }
  }

  @Override
  public Integer convert(String ordinal) {
    return ordinalNumbersMap.get(ordinal.toLowerCase());
  }
}
