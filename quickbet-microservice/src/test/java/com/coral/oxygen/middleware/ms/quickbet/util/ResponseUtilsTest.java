package com.coral.oxygen.middleware.ms.quickbet.util;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import org.junit.jupiter.api.Test;

class ResponseUtilsTest {

  @Test
  void testConstructor() throws Exception {
    Constructor<ResponseUtils> constructor = ResponseUtils.class.getDeclaredConstructor();
    constructor.setAccessible(true);
    org.assertj.core.api.Assertions.assertThatExceptionOfType(InvocationTargetException.class)
        .isThrownBy(constructor::newInstance);
  }
}
