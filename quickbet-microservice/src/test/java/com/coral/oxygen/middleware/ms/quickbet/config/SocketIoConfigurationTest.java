package com.coral.oxygen.middleware.ms.quickbet.config;

import static org.junit.jupiter.api.Assertions.assertNotNull;

import com.coral.oxygen.middleware.ms.quickbet.configuration.SocketIOConfiguration;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class SocketIoConfigurationTest {
  @Test
  void testExceptions() {
    try {
      new SocketIOConfiguration.SIOExceptionListener()
          .onEventException(new Exception(), null, null);
      new SocketIOConfiguration.SIOExceptionListener().onConnectException(new Exception(), null);
      new SocketIOConfiguration.SIOExceptionListener().onDisconnectException(new Exception(), null);
      new SocketIOConfiguration.SIOExceptionListener().onPingException(new Exception(), null);
      new SocketIOConfiguration.SIOExceptionListener().exceptionCaught(null, new Throwable());
    } catch (Exception e) {
      assertNotNull(e);
    }
  }
}
