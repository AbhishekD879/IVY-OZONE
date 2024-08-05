package com.entain.oxygen.util;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.io.*;
import java.lang.reflect.Type;
import java.util.List;
import lombok.experimental.UtilityClass;
import lombok.extern.slf4j.Slf4j;

@UtilityClass
@Slf4j
public class TestUtil {

  public static <T> List<T> readJsonArrayFromFile(String filePath, Class<T> elementType) {
    List<T> resultList = null;

    try (Reader reader =
        new InputStreamReader(TestUtil.class.getClassLoader().getResourceAsStream(filePath))) {

      Type listType = TypeToken.getParameterized(List.class, elementType).getType();

      resultList = new Gson().fromJson(reader, listType);
    } catch (IOException e) {
      log.debug("Exception occurred: {}", e.getMessage());
    }

    return resultList;
  }
}
