package com.gvc.oxygen.betreceipts.config;

import java.lang.reflect.Field;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class ProxyConfigTest implements WithAssertions {

  @InjectMocks private ProxyConfig proxyConfig;

  @Test
  void testGetBppClient() throws NoSuchFieldException, IllegalAccessException {
    Field field = ProxyConfig.class.getDeclaredField("host");
    field.setAccessible(true);
    field.set(proxyConfig, "10.10.0.1");
    Field portField = ProxyConfig.class.getDeclaredField("port");
    portField.setAccessible(true);
    portField.set(proxyConfig, "80");

    Assertions.assertDoesNotThrow(() -> proxyConfig.getBppHttpClient("pool1", 120, 10, 10, 10));
  }

  @Test
  void testGetBppClientForNonProxy() throws NoSuchFieldException, IllegalAccessException {
    Field field = ProxyConfig.class.getDeclaredField("host");
    field.setAccessible(true);
    field.set(proxyConfig, "10.10.0.1");
    Assertions.assertDoesNotThrow(() -> proxyConfig.getBppHttpClient("pool1", 120, 10, 10, 10));
  }
}
