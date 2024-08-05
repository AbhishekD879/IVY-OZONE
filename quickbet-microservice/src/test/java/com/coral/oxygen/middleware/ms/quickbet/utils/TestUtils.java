package com.coral.oxygen.middleware.ms.quickbet.utils;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.CollectionType;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import io.vavr.gson.VavrGson;
import io.vavr.jackson.datatype.VavrModule;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;
import org.apache.commons.io.IOUtils;
import org.assertj.core.api.Fail;

/**
 * @author volodymyr.masliy
 */
public class TestUtils {
  private static final ObjectMapper MAPPER = new ObjectMapper();

  public static final Gson GSON;

  static {
    MAPPER.registerModule(new VavrModule());
    MAPPER.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);

    GsonBuilder gsonBuilder = new GsonBuilder();
    VavrGson.registerAll(gsonBuilder);
    GSON = gsonBuilder.create();
  }

  public static String getResourceByPath(String pathToBody) {
    InputStream resource = TestUtils.class.getClassLoader().getResourceAsStream(pathToBody);
    if (resource == null) {
      Fail.fail("File not found: " + pathToBody);
    }
    try {
      return IOUtils.toString(resource, "UTF-8").replaceAll("\\n", "");
    } catch (IOException e) {
      Fail.fail("Failed to read file's contents: " + pathToBody + ". Reason: " + e);
      return pathToBody;
    }
  }

  public static <T> T deserializeWithJackson(String pathToResource, Class<T> clazz) {
    try {
      return MAPPER.readValue(getResourceByPath(pathToResource), clazz);
    } catch (IOException e) {
      Fail.fail("Failed to deserializeWithJackson " + pathToResource + ". Reason: " + e);
      return null;
    }
  }

  public static <T> T deserializeWithGson(String path, Class<T> clazz) {
    try {
      return GSON.fromJson(getResourceByPath(path), clazz);
    } catch (Exception e) {
      Fail.fail("Failed to deserializeWithGson " + path + ". Reason: " + e);
      return null;
    }
  }

  public static <T> List<T> deserializeListWithJackson(String pathToResource, Class<T> clazz) {
    try {
      CollectionType javaType = MAPPER.getTypeFactory().constructCollectionType(List.class, clazz);
      return MAPPER.readValue(getResourceByPath(pathToResource), javaType);
    } catch (IOException e) {
      Fail.fail("Failed to deserializeListWithJackson " + pathToResource + ". Reason: " + e);
      return null;
    }
  }

  public static byte[] convertObjectToJsonBytes(Object object) throws IOException {
    return MAPPER.writeValueAsBytes(object);
  }
}
