package com.coral.oxygen.edp.liveserv;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

/** Created by Aliaksei Yarotski on 11/7/17. */
@Component
@Slf4j
public class OxyJsonMapper {

  private final ObjectMapper mapper;

  public OxyJsonMapper(ObjectMapper mapper) {
    this.mapper = mapper;
  }

  public String write(Object object) {
    try {
      return mapper.writeValueAsString(object);
    } catch (JsonProcessingException e) {
      log.error("BaseObject serialization failed ", e);
      return null;
    }
  }

  public <T> T read(String source, Class<T> targetType) {
    try {
      return mapper.readValue(source, targetType);
    } catch (IOException e) {
      log.error("BasaObject mapping exception in reader.", e);
      return null;
    }
  }
}
