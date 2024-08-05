package com.ladbrokescoral.oxygen.trendingbets.siteserv.converter;

import java.util.Collection;
import java.util.List;

public abstract class BaseConverter<T, R> {

  public final List<R> convert(Collection<T> sourceList) {

    return sourceList.stream().map(this::convert).toList();
  }

  public final R convert(T source) {
    R result = createTarget();
    return populateResult(source, result);
  }

  protected abstract R createTarget();

  protected abstract R populateResult(T dbEntity, R result);
}
