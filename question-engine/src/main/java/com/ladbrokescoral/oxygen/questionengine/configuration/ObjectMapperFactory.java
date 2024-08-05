package com.ladbrokescoral.oxygen.questionengine.configuration;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.experimental.UtilityClass;

@UtilityClass
public class ObjectMapperFactory {

  /**
   * Define any Jackson configs you want to become global to the project.
   */
  public static ObjectMapper getInstance() {
    return new ObjectMapper()
        .findAndRegisterModules()
        .setDefaultPropertyInclusion(JsonInclude.Include.NON_NULL);
  }
}
