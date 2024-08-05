package com.coral.oxygen.middleware.ms.quickbet.config;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.client.Call;
import com.coral.oxygen.middleware.ms.liveserv.impl.MessageHandlerMultiplexer;
import com.coral.oxygen.middleware.ms.liveserv.impl.SiteServEventIdResolver;
import com.coral.oxygen.middleware.ms.quickbet.configuration.EventHandlingExecutorServiceConfiguration;
import com.coral.oxygen.middleware.ms.quickbet.configuration.LiveServConfiguration;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import java.lang.reflect.Field;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.scheduling.concurrent.ThreadPoolTaskScheduler;

class LiveServConfigurationTest {

  private LiveServConfiguration liveServConfiguration;
  private EventHandlingExecutorServiceConfiguration eventHandlingExecutorServiceConfiguration;

  @BeforeEach
  public void init() throws NoSuchFieldException, IllegalAccessException {

    liveServConfiguration = new LiveServConfiguration();
    eventHandlingExecutorServiceConfiguration = new EventHandlingExecutorServiceConfiguration();
    Field poolSize = EventHandlingExecutorServiceConfiguration.class.getDeclaredField("poolSize");
    poolSize.setAccessible(true);
    poolSize.set(eventHandlingExecutorServiceConfiguration, 5);
  }

  @Test
  void testSiteServApi() {
    SiteServEventIdResolver siteServEventIdResolver = null;
    SiteServerApi siteServerApi = Mockito.mock(SiteServerApi.class);
    siteServEventIdResolver = liveServConfiguration.siteServEventIdResolver(siteServerApi);
    Assertions.assertNotNull(siteServEventIdResolver);
  }

  @Test
  void testMessageHandlerMultiplexer() {
    MessageHandler messageHandler = Mockito.mock(MessageHandler.class);
    MessageHandlerMultiplexer messageHandlerMultiplexer = null;
    messageHandlerMultiplexer = liveServConfiguration.messageHandlerMultiplexer(messageHandler);
    Assertions.assertNotNull(messageHandlerMultiplexer);
  }

  @Test
  void testCallLiveServ() throws NoSuchAlgorithmException, KeyManagementException {
    Call call = null;
    call = liveServConfiguration.call("https://push-tst.coral.co.uk", 2, 100, 2, 3, 4, 3);
    Assertions.assertNotNull(call);
  }

  @Test
  void testLiveServService() {
    Call call = Mockito.mock(Call.class);
    MessageHandlerMultiplexer messageHandlerMultiplexer =
        Mockito.mock(MessageHandlerMultiplexer.class);
    SiteServEventIdResolver siteServEventIdResolver = Mockito.mock(SiteServEventIdResolver.class);
    ThreadPoolTaskScheduler threadPoolTaskScheduler =
        eventHandlingExecutorServiceConfiguration.threadPoolTaskScheduler();
    LiveServService liveServService = null;
    liveServService =
        liveServConfiguration.liveServService(
            call,
            messageHandlerMultiplexer,
            siteServEventIdResolver,
            threadPoolTaskScheduler,
            2,
            2,
            100);
    Assertions.assertNotNull(liveServService);
  }
}
