package com.coral.oxygen.edp.model.mapping.converter;

public interface Converter<S, T> {
  T convert(S entity);
}
