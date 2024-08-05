package com.coral.oxygen.middleware.ms.quickbet.util;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import org.springframework.util.Assert;

public class OxiCodes {
  private static final Set<String> oxiCodesForAuthErrors =
      new HashSet<>(Arrays.asList("106", "100", "104", "136", "111", "112", "115", "116"));

  private OxiCodes() {}

  public static boolean isAuthErrorCode(String code) {
    Assert.notNull(code, "Auth error code cannot be null");
    return oxiCodesForAuthErrors.contains(code.toLowerCase().trim());
  }
}
