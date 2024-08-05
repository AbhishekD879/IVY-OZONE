package com.ladbrokescoral.cashout.util;

import lombok.experimental.UtilityClass;
import org.apache.commons.lang3.StringUtils;

@UtilityClass
public class StringUtil {

  public static String ifNotEmptyOrNull(String value) {
    return StringUtils.isNotEmpty(value) ? value : null;
  }

  public static String ifNotEmptyOrDefault(String value, String defaultValue) {
    return StringUtils.isNotEmpty(value) ? value : defaultValue;
  }
}
