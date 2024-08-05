package com.ladbrokescoral.cashout.util;

import com.google.gson.Gson;
import java.io.IOException;
import java.lang.reflect.Type;
import java.net.URISyntaxException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class GsonUtil {
  private static final Gson gson = new Gson();

  public static <T> T fromJson(String fileName, Class<T> classOfT) {
    T target = null;
    try (Stream<String> lines =
        Files.lines(Paths.get(ClassLoader.getSystemResource(fileName).toURI()))) {
      String json = lines.collect(Collectors.joining());
      target = gson.fromJson(json, classOfT);
    } catch (IOException | URISyntaxException e) {
      throw new RuntimeException(e);
    }
    return target;
  }

  public static <T> T fromJson(String fileName, Type type) {
    T target = null;
    try (Stream<String> lines =
        Files.lines(Paths.get(ClassLoader.getSystemResource(fileName).toURI()))) {
      String json = lines.collect(Collectors.joining());
      target = gson.fromJson(json, type);
    } catch (IOException | URISyntaxException e) {
      throw new RuntimeException(e);
    }
    return target;
  }
}
