package com.coral.oxygen.edp.model.mapping.converter;

import com.coral.oxygen.edp.exceptions.InitializationException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.io.InputStream;
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
      @Value("${common.ordinalToNumber.json}") Resource ordinalNumbersJson, ObjectMapper mapper) {
    try (InputStream ordinalNumbersInputStream = ordinalNumbersJson.getInputStream()) {
      TypeReference<Map<String, Integer>> typeReference =
          new TypeReference<Map<String, Integer>>() {};
      ordinalNumbersMap = mapper.readValue(ordinalNumbersInputStream, typeReference);
    } catch (IOException e) {
      throw new InitializationException("Error parsing ordinal numbers json file", e);
    }
  }

  @Override
  public Integer convert(String ordinal) {
    return ordinalNumbersMap.get(ordinal.toLowerCase());
  }
}
