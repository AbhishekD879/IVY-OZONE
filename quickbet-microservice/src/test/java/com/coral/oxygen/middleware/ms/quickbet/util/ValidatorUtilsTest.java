package com.coral.oxygen.middleware.ms.quickbet.util;

import static org.assertj.core.api.Assertions.assertThatExceptionOfType;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import org.junit.jupiter.api.Test;

class ValidatorUtilsTest {

  @Test
  void testConstructor() throws Exception {
    Constructor<ValidatorUtils> constructor = ValidatorUtils.class.getDeclaredConstructor();
    constructor.setAccessible(true);
    assertThatExceptionOfType(InvocationTargetException.class).isThrownBy(constructor::newInstance);
  }
}
