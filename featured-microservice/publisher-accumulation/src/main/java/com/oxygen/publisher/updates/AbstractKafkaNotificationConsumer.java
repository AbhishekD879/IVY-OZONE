package com.oxygen.publisher.updates;

import com.newrelic.api.agent.NewRelic;
import com.oxygen.health.api.ReloadableService;
import java.util.function.Consumer;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;

@Slf4j
public abstract class AbstractKafkaNotificationConsumer implements ReloadableService {

  @Getter private volatile boolean isOnServe;

  @Override
  public void start() {
    isOnServe = true;
  }

  @Override
  public void evict() {
    isOnServe = false;
  }

  @Override
  public boolean isHealthy() {
    return isOnServe;
  }

  @Override
  public void onFail(Exception ex) {
    this.isOnServe = false;
  }

  public void process(
      ConsumerRecord<String, String> data, Consumer<ConsumerRecord<String, String>> onRecord) {
    try {
      log.debug("Processing Kafka record {}.", data.toString());
      onRecord.accept(data);
      isOnServe = true;
    } catch (RuntimeException e) {
      onFail(e);
      log.error("Failed to process Kafka record. ", e);
      NewRelic.noticeError(e);
    }
  }
}
