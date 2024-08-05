package com.ladbrokescoral.cashout.util;

import static org.junit.jupiter.api.Assertions.fail;

import java.nio.charset.StandardCharsets;
import org.apache.commons.io.IOUtils;

public class TestUtil {
  public static String readFromFile(String path) {
    try {
      return IOUtils.toString(TestUtil.class.getResource(path), StandardCharsets.UTF_8);
    } catch (Exception e) {
      fail("Failed to read resource by path=" + path);
      throw new IllegalStateException(e);
    }
  }
}
