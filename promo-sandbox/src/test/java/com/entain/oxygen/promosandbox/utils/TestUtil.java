package com.entain.oxygen.promosandbox.utils;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.io.InputStream;
import lombok.SneakyThrows;

public class TestUtil {
  private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper().findAndRegisterModules();

  public static <T> T deepCopy(T objects, TypeReference<T> type) throws IOException {
    return OBJECT_MAPPER.readValue(OBJECT_MAPPER.writeValueAsString(objects), type);
  }

  public static <T> T deserializeWithJackson(String pathToResource, Class<T> clazz)
      throws IOException {
    return OBJECT_MAPPER.readValue(readFromFile(pathToResource), clazz);
  }

  public static byte[] convertObjectToJsonBytes(Object object) throws IOException {
    return OBJECT_MAPPER.writeValueAsBytes(object);
  }

  @SneakyThrows
  public static InputStream readFromFile(String path) {
    return TestUtil.class.getResourceAsStream(path);
  }
}
