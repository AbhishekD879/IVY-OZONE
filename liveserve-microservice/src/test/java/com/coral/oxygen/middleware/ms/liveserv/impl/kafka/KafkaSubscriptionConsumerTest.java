package com.coral.oxygen.middleware.ms.liveserv.impl.kafka;

import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.impl.redis.RedisCacheService;
import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class KafkaSubscriptionConsumerTest {

  @Mock private LiveServService liveServService;
  @Mock private RedisCacheService redisCacheService;
  @Mock private MasterSlaveExecutor masterSlaveExecutor;

  private KafkaSubscriptionConsumer kafkaSubscriptionConsumer;

  private static final String CHANNEL = "channel";

  @Before
  public void init() {
    kafkaSubscriptionConsumer =
        new KafkaSubscriptionConsumer(liveServService, redisCacheService, masterSlaveExecutor);
  }

  @Test
  public void masterConsumeMessageTest() {
    doAnswer(
            invocation -> {
              Runnable task = (Runnable) invocation.getArguments()[0];
              task.run();
              return null;
            })
        .when(masterSlaveExecutor)
        .executeIfMaster(any(Runnable.class), any(Runnable.class));

    kafkaSubscriptionConsumer.consume(
        new ConsumerRecord<String, String>("topic", 0, 0, CHANNEL, null));
    verify(liveServService, times(1)).subscribe(CHANNEL);
    verify(redisCacheService, times(1)).cacheSubscription(CHANNEL);
    verify(redisCacheService, times(1)).getAllSubscription();
  }

  @Test
  public void slaveConsumeMessageTest() {
    doAnswer(
            invocation -> {
              Runnable task = (Runnable) invocation.getArguments()[1];
              task.run();
              return null;
            })
        .when(masterSlaveExecutor)
        .executeIfMaster(any(Runnable.class), any(Runnable.class));

    kafkaSubscriptionConsumer.consume(
        new ConsumerRecord<String, String>("topic", 0, 0, CHANNEL, null));
    verify(liveServService, times(0)).subscribe(CHANNEL);
    verify(redisCacheService, times(0)).cacheSubscription(CHANNEL);
    verify(redisCacheService, times(0)).getAllSubscription();
  }
}
