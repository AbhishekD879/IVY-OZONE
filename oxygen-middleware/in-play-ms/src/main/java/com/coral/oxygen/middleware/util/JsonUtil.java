package com.coral.oxygen.middleware.util;

import com.google.gson.Gson;
import com.google.json.JsonSanitizer;
import lombok.experimental.UtilityClass;

@UtilityClass
public class JsonUtil {

  private static final Gson gson = new Gson();

  public static String toJson(Object object) {
    return gson.toJson(object);
  }

  public static <T> T fromJson(String json, Class<T> classOfT) {
    return gson.fromJson(JsonSanitizer.sanitize(json), classOfT);
  }
}
