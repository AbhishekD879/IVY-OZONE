package com.ladbrokescoral.oxyegn.test.utils;

import com.google.gson.Gson;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Type;
import java.nio.charset.StandardCharsets;
import java.util.Objects;

public class Utils {

  public static <T> T fromFile(Gson gson, String name, Type type) {
    InputStream stream = Utils.class.getClassLoader().getResourceAsStream(name);
    return gson.fromJson(new InputStreamReader(stream, StandardCharsets.UTF_8), type);
  }

  public static String fromResource(String path, ClassLoader classLoader) throws IOException {
    InputStreamReader reader =
        new InputStreamReader(Objects.requireNonNull(classLoader.getResourceAsStream(path)));
    char[] buffer = new char[4096];
    StringBuilder sb = new StringBuilder();
    for (int len; (len = reader.read(buffer)) > 0; ) {
      sb.append(buffer, 0, len);
    }
    return sb.toString();
  }
}
