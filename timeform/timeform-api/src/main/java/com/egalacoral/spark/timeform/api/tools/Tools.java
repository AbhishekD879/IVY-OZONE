package com.egalacoral.spark.timeform.api.tools;

import java.text.SimpleDateFormat;
import java.util.TimeZone;
import java.util.stream.Stream;

public class Tools {

  public static <T> Stream<T> arrayToStream(T[] arr) {
    if (arr == null) {
      return Stream.empty();
    }
    return Stream.of(arr);
  }

  public static SimpleDateFormat simpleDateFormat(String pattern) {
    SimpleDateFormat simpleDateFormat = new SimpleDateFormat(pattern);
    simpleDateFormat.setTimeZone(TimeZone.getTimeZone("Europe/London"));
    return simpleDateFormat;
  }
}
