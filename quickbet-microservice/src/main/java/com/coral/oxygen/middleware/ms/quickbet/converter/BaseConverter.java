package com.coral.oxygen.middleware.ms.quickbet.converter;

import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

public abstract class BaseConverter<T, R> {

  public final List<R> convert(Collection<T> sourceList) {
    if (sourceList == null) {
      return Collections.emptyList();
    }
    return sourceList.stream().map(this::convert).collect(Collectors.toList());
  }

  public final R convert(T source) {
    if (source != null) {
      R result = createTarget();
      return populateResult(source, result);
    }
    return null;
  }

  protected abstract R createTarget();

  protected abstract R populateResult(T dbEntity, R result);
}
