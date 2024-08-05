package com.entain.oxygen.util;

import com.google.gson.Gson;
import com.google.json.JsonSanitizer;
import lombok.experimental.UtilityClass;

@UtilityClass
public class JsonUtil {

  private static Gson gson = new Gson();

  public static <T> T fromJson(String json, Class<T> classOfT) {
    return gson.fromJson(JsonSanitizer.sanitize(json), classOfT);
  }
}
