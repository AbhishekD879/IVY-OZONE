package com.entain.oxygen.promosandbox.utils;

import com.google.gson.Gson;
import lombok.experimental.UtilityClass;

@UtilityClass
public class JsonUtil {

  private static Gson gson = new Gson();

  public static String toJson(Object object) {
    return gson.toJson(object);
  }
}
