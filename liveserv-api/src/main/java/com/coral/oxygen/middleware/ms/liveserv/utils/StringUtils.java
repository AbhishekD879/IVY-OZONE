package com.coral.oxygen.middleware.ms.liveserv.utils;

/** Created by azayats on 19.01.17. */
public final class StringUtils {

  private StringUtils() {}

  private static final char ZERO_CHAR = '0';
  private static final String ZERO_STRING = "0";

  public static String normalizeNumber(String input) {
    String trimmed = input.trim();
    if (!validateDigits(trimmed)) {
      throw new IllegalArgumentException("Not a number: " + input);
    }
    int leadingZerosCount = 0;
    boolean leadingZerosMode = true;
    for (int i = 0; i < trimmed.length(); i++) {
      char c = trimmed.charAt(i);
      if (leadingZerosMode && c == ZERO_CHAR) {
        leadingZerosCount++;
      } else {
        leadingZerosMode = false;
      }
    }
    String result = trimmed.substring(leadingZerosCount);
    if (result.isEmpty() && leadingZerosCount > 0) {
      result = ZERO_STRING;
    }
    if (result.isEmpty()) {
      throw new IllegalArgumentException("Empty - Not a number: '" + input + "'");
    }
    return result;
  }

  public static boolean validateDigits(String input) {
    for (int i = 0; i < input.length(); i++) {
      char c = input.charAt(i);
      if (!Character.isDigit(c)) {
        return false;
      }
    }
    return true;
  }

  public static String addLeadingZeros(String numberStr, int finalLength) {
    if (!validateDigits(numberStr)) {
      throw new IllegalArgumentException("Not a number: " + numberStr);
    }
    if (numberStr.length() > finalLength) {
      throw new IllegalArgumentException("'" + numberStr + "' is longer than " + finalLength);
    }
    if (numberStr.length() == finalLength) {
      return numberStr;
    }
    StringBuilder builder = new StringBuilder();
    int zerosNum = finalLength - numberStr.length();
    for (int i = 0; i < zerosNum; i++) {
      builder.append(ZERO_CHAR);
    }
    builder.append(numberStr);
    return builder.toString();
  }
}
