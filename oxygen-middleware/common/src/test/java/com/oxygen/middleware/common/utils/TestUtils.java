package com.oxygen.middleware.common.utils;

import com.coral.oxygen.middleware.JsonFacade;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.CollectionType;
import com.google.gson.Gson;
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

  private static Gson mGson = JsonFacade.NO_ESCAPING_GSON;

  public static Gson getGson(final boolean logWarning) {
    return mGson;
  }

  public static <T> T parseRequest(final String json, final Class<T> classOfT) {
    return TestUtils.getGson(false).fromJson(json, classOfT);
  }

  public static <T> T parseFile(final String fileName, final Class<T> classOfT) {
    return parseRequest(getResourse(fileName), classOfT);
  }

  @SneakyThrows
  public static String getResourse(String pathToBody) {
    // TODO: JDK 11 - InputStream::readAllBytes()
    return new String(
        Files.readAllBytes(
            Paths.get(ClassLoader.getSystemClassLoader().getResource(pathToBody).toURI())));
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
