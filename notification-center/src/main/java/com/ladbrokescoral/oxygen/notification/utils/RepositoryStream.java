package com.ladbrokescoral.oxygen.notification.utils;

import java.util.stream.Stream;
import java.util.stream.StreamSupport;

public class RepositoryStream {

  public static <T> Stream<T> parallelStream(Iterable<T> iterable) {
    return StreamSupport.stream(iterable.spliterator(), true);
  }
}
