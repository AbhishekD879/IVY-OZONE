package com.ladbrokescoral.oxygen.configuration;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

class ObjectMapperTest {

  @Test
  void testObjectMapper() {
    ObjectMapperConfig config = new ObjectMapperConfig();
    Assertions.assertTrue(config.objectMapper() instanceof ObjectMapper);
  }
}
