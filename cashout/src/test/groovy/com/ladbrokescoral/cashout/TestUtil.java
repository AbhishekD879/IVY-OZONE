package com.ladbrokescoral.cashout;

import static org.junit.jupiter.api.Assertions.fail;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.CollectionType;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.List;
import org.apache.commons.io.IOUtils;

public class TestUtil {
  private static final ObjectMapper MAPPER = new ObjectMapper();

  static {
    MAPPER.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
    MAPPER.registerModule(new JavaTimeModule());
    MAPPER.setSerializationInclusion(JsonInclude.Include.NON_EMPTY);
  }

  public static String readFromFile(String path) {
    try {
      return IOUtils.toString(TestUtil.class.getResource(path), StandardCharsets.UTF_8);
    } catch (Exception e) {
      fail("Failed to read resource by resource path=" + path);
      throw new IllegalStateException(e);
    }
  }

  public static InputStream readStreamFromFile(String path) {
    try {
      return TestUtil.class.getResourceAsStream(path);
    } catch (Exception e) {
      fail("Failed to read resource by path=" + path);
      throw new IllegalStateException(e);
    }
  }

  public static <T> T deserializeWithJackson(String pathToResource, Class<T> clazz) {
    try {
      return MAPPER.readValue(readFromFile(pathToResource), clazz);
    } catch (IOException e) {
      fail(deserializeErrMessage(pathToResource, e));
      return null;
    }
  }

  private static String deserializeErrMessage(String pathToResource, IOException e) {
    return "Failed to deserializeWithJackson " + pathToResource + ". Reason: " + e;
  }

  public static <T> T deserializeWithJacksonToType(
      String pathToResource, TypeReference<T> typeReference) {
    try {
      return MAPPER.readValue(readFromFile(pathToResource), typeReference);
    } catch (IOException e) {
      fail(deserializeErrMessage(pathToResource, e));
      return null;
    }
  }

  public static String serializeWithJackson(Object object) {
    try {
      return MAPPER.writeValueAsString(object);
    } catch (JsonProcessingException e) {
      fail("Failed to serializeWithJackson " + object + ". Reason: " + e);
      return null;
    }
  }

  public static <T> T serializeWithJackson(String data, Class<T> clazz) {
    try {
      return MAPPER.readValue(data, clazz);
    } catch (JsonProcessingException e) {
      fail("Failed to serializeWithJackson " + data + ". Reason: " + e);
      return null;
    }
  }

  public static <T> List<T> deserializeListWithJackson(String pathToResource, Class<T> clazz) {
    try {
      CollectionType javaType = MAPPER.getTypeFactory().constructCollectionType(List.class, clazz);
      return MAPPER.readValue(readFromFile(pathToResource), javaType);
    } catch (IOException e) {
      fail(deserializeErrMessage(pathToResource, e));
      return null;
    }
  }

  public static byte[] convertObjectToJsonBytes(Object object) throws IOException {
    return MAPPER.writeValueAsBytes(object);
  }
}
