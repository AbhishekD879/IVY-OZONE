package com.ladbrokescoral.oxygen.trendingbets.utils;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.CollectionType;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import lombok.SneakyThrows;
import org.junit.Assert;

public class TestUtils {
  private static final ObjectMapper MAPPER = new ObjectMapper();

  static {
    MAPPER.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
  }

  @SneakyThrows
  public static String getResourse(String pathToBody) {
    return new String(
        Files.readAllBytes(
            Paths.get(ClassLoader.getSystemClassLoader().getResource(pathToBody).toURI())));
  }

  public static <T> T deserialize(String pathToResource, Class<T> clazz) {
    try {
      return MAPPER.readValue(getResourse(pathToResource), clazz);
    } catch (IOException e) {
      Assert.fail("Failed to deserializeList " + pathToResource + ". Reason: " + e);
      return null;
    }
  }

  public static <T> List<T> deserializeList(String pathToResource, Class<T> clazz) {
    try {
      CollectionType javaType = MAPPER.getTypeFactory().constructCollectionType(List.class, clazz);
      return MAPPER.readValue(getResourse(pathToResource), javaType);
    } catch (IOException e) {
      Assert.fail("Failed to deserializeList " + pathToResource + ". Reason: " + e);
      return null;
    }
  }
}
