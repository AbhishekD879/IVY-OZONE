package com.coral.oxygen.middleware.featured.utils;

import com.coral.oxygen.middleware.common.service.ModuleAdapter;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.CollectionType;
import com.google.gson.reflect.TypeToken;
import java.io.IOException;
import java.lang.reflect.Type;
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
    // TODO: JDK 11 - InputStream::readAllBytes()
    return new String(
        Files.readAllBytes(
            Paths.get(ClassLoader.getSystemClassLoader().getResource(pathToBody).toURI())));
  }

  public static <T> T deserializeWithGson(String resourceName, Class<T> clazz) {
    String featuredModelJson = TestUtils.getResourse(resourceName);
    return ModuleAdapter.FEATURED_GSON.fromJson(featuredModelJson, clazz);
  }

  public static <T> List<T> deserializeListWithGson(String resourceName, Class<T> clazz) {
    String eventJson = TestUtils.getResourse(resourceName);
    Type listType = new TypeToken<List<T>>() {}.getType();
    return ModuleAdapter.FEATURED_GSON.fromJson(eventJson, listType);
  }

  public static <T> List<T> deserializeListWithJackson(String pathToResource, Class<T> clazz) {
    try {
      CollectionType javaType = MAPPER.getTypeFactory().constructCollectionType(List.class, clazz);
      return MAPPER.readValue(getResourse(pathToResource), javaType);
    } catch (IOException e) {
      Assert.fail("Failed to deserializeListWithJackson " + pathToResource + ". Reason: " + e);
      return null;
    }
  }
}
