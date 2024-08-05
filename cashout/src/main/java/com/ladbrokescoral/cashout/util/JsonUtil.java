package com.ladbrokescoral.cashout.util;

import com.google.gson.Gson;
import com.google.json.JsonSanitizer;
import lombok.experimental.UtilityClass;

@UtilityClass
public class JsonUtil {

  private static Gson gson = new Gson();

  public static String toJson(Object object) {
    return gson.toJson(object);
  }

  public static <T> T fromJson(String json, Class<T> classOfT) {
    // FIXME: We must validate the json received to be sure it contais
    // exactly the expected content before setting it to Model Object.
    // TODO: Implement an validator that checks the json with
    // a patterns of fields/format expected OR use FasterXML/jackson
    return gson.fromJson(JsonSanitizer.sanitize(json), classOfT);
  }
}
