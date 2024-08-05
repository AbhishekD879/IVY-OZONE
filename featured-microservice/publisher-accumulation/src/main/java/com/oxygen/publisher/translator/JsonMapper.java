package com.oxygen.publisher.translator;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/** Created by Aliaksei Yarotski on 11/7/17. */
public class JsonMapper {

  private static final transient Logger LOGGER = LoggerFactory.getLogger(JsonMapper.class);

  private final ObjectMapper mapper;

  public JsonMapper(ObjectMapper mapper) {
    this.mapper = mapper;
  }

  public String write(Object object) {
    try {
      return mapper.writeValueAsString(object);
    } catch (JsonProcessingException e) {
      LOGGER.error("BaseObject serialization faile_d ", e);
      return null;
    }
  }

  public <T> T read(String source, Class<T> targetType) {
    try {
      return mapper.readValue(source, targetType);
    } catch (IOException e) {
      LOGGER.error("BasaObject mapping exception in reader.", e);
      return null;
    }
  }
}
