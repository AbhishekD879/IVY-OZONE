package com.ladbrokescoral.oxygen.cms.api;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.CollectionType;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import lombok.SneakyThrows;
import lombok.experimental.UtilityClass;

@UtilityClass
public class TestUtil {

  // FIXME: CRITICAL: we should use not custom mapper
  // Use Spring for Autowire or @JsonTest
  private static final ObjectMapper MAPPER = new ObjectMapper();

  static {
    MAPPER.findAndRegisterModules();
    MAPPER.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
  }

  @SneakyThrows
  public static InputStream readFromFile(String path) {
    return TestUtil.class.getResourceAsStream(path);
  }

  @SneakyThrows
  public static byte[] readFromFileAsBytes(String path) {
    // TODO: JDK 11 - InputStream::readAllBytes()
    return Files.readAllBytes(Paths.get(TestUtil.class.getResource(path).toURI()));
  }

  public static <T> T deserializeWithJackson(String pathToResource, Class<T> clazz)
      throws IOException {
    return MAPPER.readValue(readFromFile(pathToResource), clazz);
  }

  public static <T> T deserializeWithJacksonToType(
      String pathToResource, TypeReference<T> typeReference) throws IOException {
    return MAPPER.readValue(readFromFile(pathToResource), typeReference);
  }

  public static String serializeWithJackson(Object object) throws JsonProcessingException {
    return MAPPER.writeValueAsString(object);
  }

  public static <T> List<T> deserializeListWithJackson(String pathToResource, Class<T> clazz)
      throws IOException {
    CollectionType javaType = MAPPER.getTypeFactory().constructCollectionType(List.class, clazz);
    return MAPPER.readValue(readFromFile(pathToResource), javaType);
  }

  public static byte[] convertObjectToJsonBytes(Object object) throws IOException {
    return MAPPER.writeValueAsBytes(object);
  }
}
