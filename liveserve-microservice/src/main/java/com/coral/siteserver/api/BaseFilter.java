package com.coral.siteserver.api;

import java.util.List;

/** Created by idomshchikov on 11/2/16. */
public interface BaseFilter {
  String SEPARATOR = ":";

  List<String> getQueryMap();
}
