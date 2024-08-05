package com.ladbrokescoral.oxygen.bigcompetition;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.CollectionType;
import java.io.IOException;
import java.nio.charset.Charset;
import java.util.List;
import org.apache.commons.io.IOUtils;
import org.junit.Assert;

public class TestUtil {
  private static final ObjectMapper MAPPER = new ObjectMapper();

  static {
    MAPPER.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
  }

  private static String readFromFile(String path) {
    try {
      return IOUtils.toString(TestUtil.class.getResource(path), Charset.forName("UTF-8"));
    } catch (Exception e) {
      Assert.fail("Failed to read resource by path=" + path);
      throw new IllegalStateException(e);
    }
  }

  public static <T> T deserializeWithJackson(String pathToResource, Class<T> clazz) {
    try {
      return MAPPER.readValue(readFromFile(pathToResource), clazz);
    } catch (IOException e) {
      Assert.fail("Failed to deserializeWithJackson " + pathToResource + ". Reason: " + e);
      return null;
    }
  }

  public static <T> T deserializeWithJacksonToType(
      String pathToResource, TypeReference<T> typeReference) {
    try {
      return MAPPER.readValue(readFromFile(pathToResource), typeReference);
    } catch (IOException e) {
      Assert.fail("Failed to deserializeWithJackson " + pathToResource + ". Reason: " + e);
      return null;
    }
  }

  public static String serializeWithJackson(Object object) {
    try {
      return MAPPER.writeValueAsString(object);
    } catch (JsonProcessingException e) {
      Assert.fail("Failed to serializeWithJackson " + object + ". Reason: " + e);
      return null;
    }
  }

  public static <T> List<T> deserializeListWithJackson(String pathToResource, Class<T> clazz) {
    try {
      CollectionType javaType = MAPPER.getTypeFactory().constructCollectionType(List.class, clazz);
      return MAPPER.readValue(readFromFile(pathToResource), javaType);
    } catch (IOException e) {
      Assert.fail("Failed to deserializeListWithJackson " + pathToResource + ". Reason: " + e);
      return null;
    }
  }
}
