package com.coral.oxygen.edp;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.CollectionType;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import lombok.SneakyThrows;
import org.junit.Assert;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class TestUtil {
  private static final ObjectMapper MAPPER = new ObjectMapper();
  private static final List<String> virtualRacingIds;

  static {
    virtualRacingIds = new ArrayList<>();
    virtualRacingIds.add("285");
    virtualRacingIds.add("286");
    virtualRacingIds.add("288");
    virtualRacingIds.add("289");
    virtualRacingIds.add("290");

    MAPPER.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
  }

  public static List<String> virtualRacingIds() {
    return virtualRacingIds;
  }

  @SneakyThrows
  private static String readFromFile(String path) {
    // TODO: JDK 11 - InputStream::readAllBytes()
    return new String(Files.readAllBytes(Paths.get(TestUtil.class.getResource(path).toURI())));
  }

  public static <T> List<T> deserializeListWithJackson(String pathToResource, Class<T> clazz) {
    try {
      CollectionType javaType = MAPPER.getTypeFactory().constructCollectionType(List.class, clazz);
      return MAPPER.readValue(readFromFile(pathToResource), javaType);
    } catch (IOException e) {
      Assert.fail("Failed to deserializeListWithJackson " + pathToResource + ". Reason: " + e);
      return Collections.emptyList();
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

  public static <T> T deserializeFromFile(String resourcePath, Class<T> valueType)
      throws IOException {
    InputStream jsonStream = TestUtil.class.getClassLoader().getResourceAsStream(resourcePath);
    return MAPPER.readValue(jsonStream, valueType);
  }
}
