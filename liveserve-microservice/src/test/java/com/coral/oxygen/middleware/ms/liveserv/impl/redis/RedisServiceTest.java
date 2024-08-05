package com.coral.oxygen.middleware.ms.liveserv.impl.redis;

import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.ms.liveserv.ChannelUnsubcribeEvent;
import com.coral.oxygen.middleware.ms.liveserv.model.CachedChannel;
import java.util.Collections;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class RedisServiceTest {

  @Mock private SubscriptionCache subscriptionCache;

  private RedisCacheService redisCacheService;

  private static final String CHANNEL = "channel";

  @Before
  public void init() {
    redisCacheService = new RedisCacheService(subscriptionCache);
  }

  @Test
  public void cacheSubscriptionTest() {
    redisCacheService.cacheSubscription(anyString());
    verify(subscriptionCache, times(1)).save(any());
  }

  @Test
  public void channelUnsubscribeTest() {
    ChannelUnsubcribeEvent event = new ChannelUnsubcribeEvent("source", CHANNEL);
    redisCacheService.onChannelUnsubscribe(event);
    verify(subscriptionCache, times(1)).deleteById(eq(CHANNEL));
  }

  @Test
  public void getAllSubscriptionTest() {
    CachedChannel cachedChannel = new CachedChannel(CHANNEL);
    when(subscriptionCache.findAll()).thenReturn(Collections.singletonList(cachedChannel));

    List<String> channels = redisCacheService.getAllSubscription();
    Assert.assertEquals(CHANNEL, channels.get(0));
  }
}
