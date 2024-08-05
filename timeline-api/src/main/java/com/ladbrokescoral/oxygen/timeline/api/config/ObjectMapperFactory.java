package com.ladbrokescoral.oxygen.timeline.api.config;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import lombok.experimental.UtilityClass;

@UtilityClass
public class ObjectMapperFactory {

  /** Define any Jackson configs you want to become global to the project. */
  public static ObjectMapper getInstance() {
    return new ObjectMapper()
        .findAndRegisterModules()
        .configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false)
        .setDefaultPropertyInclusion(JsonInclude.Include.NON_NULL);
  }
}
