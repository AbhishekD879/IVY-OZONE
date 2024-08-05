package com.ladbrokescoral.oxygen.cms.util;

import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.Set;
import org.spockframework.util.CollectionUtil;

public class CollectionUtilX extends CollectionUtil {

  public static <T> Set<T> setOf(T... elements) {
    if (elements.length == 0) {
      return Collections.emptySet();
    } else if (elements.length == 1) {
      return Collections.singleton(elements[0]);
    }
    return new HashSet<>(Arrays.asList(elements));
  }

  public static <T> Set<T> unionSet(Collection<T>... collections) {
    Set<T> union = new HashSet<>();
    for (Collection<T> collection : collections) {
      union.addAll(collection);
    }
    return union;
  }
}
