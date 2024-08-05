package com.coral.siteserver.api;

import java.util.List;

@FunctionalInterface
public interface Call<T, H> {

  List<T> get(List<H> lists);
}
