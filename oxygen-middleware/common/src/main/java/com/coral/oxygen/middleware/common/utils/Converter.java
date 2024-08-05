package com.coral.oxygen.middleware.common.utils;

public interface Converter<F, T> {
  T convert(F entity);
}
