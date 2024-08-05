package com.coral.oxygen.middleware.ms.liveserv.utils;

import com.newrelic.api.agent.NewRelic;
import java.text.MessageFormat;

/** Created by azayats on 19.01.17. */
public final class StringUtils {

  private StringUtils() {}

  public static final int EVENT_ID_LENGTH = 10;
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

  // method tries to cut excessive `0` placeholders, if fails - throws an exception
  public static String tryTrimChannelPrefix(String channelId) {
    String channelPrefix = channelId.substring(0, channelId.length() - EVENT_ID_LENGTH);
    if (channelPrefix.matches("0*")) {
      return channelId.substring(channelId.length() - EVENT_ID_LENGTH);
    }

    NewRelic.noticeError(
        MessageFormat.format("channel id %s exceeds %s digit limit", channelId, EVENT_ID_LENGTH));
    throw new IllegalArgumentException(channelId + " channelId length must be 10");
  }
}
