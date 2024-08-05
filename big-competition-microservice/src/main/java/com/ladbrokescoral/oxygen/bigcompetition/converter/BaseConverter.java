package com.ladbrokescoral.oxygen.bigcompetition.converter;

import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

@FunctionalInterface
public interface BaseConverter<S, D> {

  default List<D> convert(Collection<S> sourceList) {
    if (sourceList == null) {
      return Collections.emptyList();
    }
    return sourceList.stream()
        .map(this::convert)
        .filter(Objects::nonNull)
        .collect(Collectors.toList());
  }

  default D convert(S source) {
    if (source != null) {
      return map(source);
    }
    return null;
  }

  D map(S source);
}
