package com.coral.oxygen.middleware.common.utils;

import lombok.experimental.UtilityClass;

@UtilityClass
public class Utils {

  public static String trimWithEmpty(String string) {
    return string.replace("|", "");
  }
}
