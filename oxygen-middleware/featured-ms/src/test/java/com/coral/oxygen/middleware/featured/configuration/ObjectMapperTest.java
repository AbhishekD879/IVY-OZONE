package com.coral.oxygen.middleware.featured.configuration;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import org.junit.Assert;
import org.junit.Test;

public class ObjectMapperTest {

  ObjectMapper objectMapper;
  ObjectWriter objectWriter;

  @Test
  public void testObjectMapper() {
    ObjectMapperConfig config = new ObjectMapperConfig();
    Assert.assertTrue(config.objectMapper() instanceof ObjectMapper);
  }

  @Test
  public void testObjectWriter() {
    ObjectMapperConfig config = new ObjectMapperConfig();
    Assert.assertTrue(config.objectWriter() instanceof ObjectWriter);
  }
}
