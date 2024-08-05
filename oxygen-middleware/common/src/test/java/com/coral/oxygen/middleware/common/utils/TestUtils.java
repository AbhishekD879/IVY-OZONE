package com.coral.oxygen.middleware.common.utils;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

class TestUtils {

  @Test
  void testTrimWithEmpty() {
    String response = Utils.trimWithEmpty("|Tennis|");
    Assertions.assertEquals("Tennis", response);
  }
}
