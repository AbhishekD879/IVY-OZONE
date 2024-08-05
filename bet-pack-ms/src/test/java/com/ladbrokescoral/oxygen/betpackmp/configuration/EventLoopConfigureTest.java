package com.ladbrokescoral.oxygen.betpackmp.configuration;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Modifier;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class EventLoopConfigureTest implements WithAssertions {

  @Test
  void testConstructorIsPrivate() throws Exception {
    Constructor<EventLoopConfigure> constructor = EventLoopConfigure.class.getDeclaredConstructor();
    assertTrue(Modifier.isPrivate(constructor.getModifiers()));
    constructor.setAccessible(true);
    assertThrows(
        InvocationTargetException.class,
        () -> {
          constructor.newInstance();
        });
  }
}
