package com.coral.oxygen.middleware.ms.liveserv.impl.kafka;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.impl.redis.RedisCacheService;
import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import com.newrelic.api.agent.NewRelic;
import java.util.List;
import java.util.Objects;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.KafkaListener;

@Configuration
@Slf4j
public class KafkaSubscriptionConsumer {

  private static final String CUSTOM_KAFKA_SUBSCRIPTION_COUNTER_NAME = "Custom/Kafka/Subscription";
  private final LiveServService liveServService;
  private final RedisCacheService redisCacheService;
  private final MasterSlaveExecutor masterSlaveExecutor;

  private boolean isMaster;

  @Autowired
  public KafkaSubscriptionConsumer(
      LiveServService liveServService,
      RedisCacheService redisCacheService,
      MasterSlaveExecutor masterSlaveExecutor) {
    this.liveServService = liveServService;
    this.redisCacheService = redisCacheService;
    this.masterSlaveExecutor = masterSlaveExecutor;
    this.isMaster = false;
  }

  @KafkaListener(
      topics = "${topic.subscription}",
      containerFactory = "kafkaSubscriptionListenerContainerFactory")
  public void consume(ConsumerRecord<String, String> record) {
    try {
      masterSlaveExecutor.executeIfMaster(
          () -> {
            NewRelic.incrementCounter(CUSTOM_KAFKA_SUBSCRIPTION_COUNTER_NAME);
            log.trace("Subscribe on channel: {} and cache subscription", record.key());
            liveServService.subscribe(record.key());
            redisCacheService.cacheSubscription(record.key());

            // if slave became master - resubscribe all events
            if (!isMaster) {
              resubscribeAll();
            }
          },
          () -> {
            log.info("SLAVE");
            isMaster = false;
          });
    } catch (Exception ex) {
      log.error("Caught error while processing subscription ", ex);
    }
  }

  private void resubscribeAll() {
    List<String> allSubscription = redisCacheService.getAllSubscription();
    log.info("Became master, resubscribing to {} channels", allSubscription);
    allSubscription.stream().filter(Objects::nonNull).forEach(liveServService::subscribe);
    log.info("Master resubscribed to all channels");
    isMaster = true;
  }
}
