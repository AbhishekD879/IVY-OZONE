package com.egalacoral.spark.timeform.tools;

import java.util.function.Function;
import java.util.stream.Stream;

public class Tools {

  public static <T> Stream<T> emptyStream() {
    return Stream.empty();
  }

  public static <T> Function<T, T> identity() {
    return t -> t;
  }
}
