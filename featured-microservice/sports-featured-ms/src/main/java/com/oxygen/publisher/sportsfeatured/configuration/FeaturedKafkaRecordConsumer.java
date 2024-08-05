package com.oxygen.publisher.sportsfeatured.configuration;

import com.newrelic.api.agent.Trace;
import com.oxygen.publisher.service.KafkaTopic;
import com.oxygen.publisher.sportsfeatured.model.PageCacheUpdate;
import com.oxygen.publisher.sportsfeatured.model.PageRawIndex;
import com.oxygen.publisher.sportsfeatured.service.SportsChainFactory;
import com.oxygen.publisher.updates.AbstractKafkaNotificationConsumer;
import java.util.Objects;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.KafkaListener;

// @KafkaListener requires @Configuration annotation on class
@Configuration
@Slf4j
@RequiredArgsConstructor
public class FeaturedKafkaRecordConsumer extends AbstractKafkaNotificationConsumer {

  protected final KafkaTopic kafkaTopic;

  @Trace(metricName = "Incoming live update from Kafka", dispatcher = true)
  @KafkaListener(
      topics = "${kafka.topics.prefix}__${kafka.live.update.topic.name}",
      containerFactory = "kafkaLiveUpdateListenerContainerFactory")
  public void onLiveUpdate(ConsumerRecord<String, String> data) {
    process(
        data,
        record ->
            SportsChainFactory.getFeaturedChainFactory()
                .processLiveUpdate(
                    Objects.requireNonNull(record.key()), Objects.requireNonNull(record.value())));
  }

  @Trace(metricName = "Incoming FEATURED_STRUCTURE_CHANGED", dispatcher = true)
  @KafkaListener(
      topics = "#{kafkaTopic.keyFor('FEATURED_STRUCTURE_CHANGED')}",
      containerFactory = "kafkaModelUpdateListenerContainerFactory")
  public void onStructureChange(ConsumerRecord<String, String> data) {
    log.info("new FEATURED_STRUCTURE_CHANGED -> {} ", data);
    process(
        data,
        record ->
            SportsChainFactory.getFeaturedChainFactory()
                .structureChanged(
                    new PageCacheUpdate(PageRawIndex.GenerationKey.fromString(record.value())))
                .start(record.value()));
  }

  @Trace(metricName = "Incoming FEATURED_MODULE_CONTENT_CHANGED", dispatcher = true)
  @KafkaListener(
      topics = "#{kafkaTopic.keyFor('FEATURED_MODULE_CONTENT_CHANGED')}",
      containerFactory = "kafkaModelUpdateListenerContainerFactory")
  public void onModuleChange(ConsumerRecord<String, String> data) {
    log.info("new FEATURED_MODULE_CONTENT_CHANGED -> {} ", data);
    process(
        data,
        record -> {
          String[] compositeKey = data.value().split("::");
          SportsChainFactory.getFeaturedChainFactory().moduleContentChanged().start(compositeKey);
        });
  }

  @Trace(metricName = "Incoming FEATURED_MODULE_CONTENT_CHANGED_MINOR", dispatcher = true)
  @KafkaListener(
      topics = "#{kafkaTopic.keyFor('FEATURED_MODULE_CONTENT_CHANGED_MINOR')}",
      containerFactory = "kafkaModelUpdateListenerContainerFactory")
  public void onModuleMinorChange(ConsumerRecord<String, String> data) {
    log.info("new FEATURED_MODULE_CONTENT_CHANGED_MINOR -> {}", data);
    String[] compositeKey = data.value().split("::");
    process(
        data,
        record ->
            SportsChainFactory.getFeaturedChainFactory()
                .moduleContentMinorChanged()
                .start(compositeKey));
  }

  @Trace(metricName = "Incoming SPORTS_FEATURED_PAGE_DELETED", dispatcher = true)
  @KafkaListener(
      topics = "#{kafkaTopic.keyFor('SPORTS_FEATURED_PAGE_DELETED')}",
      containerFactory = "kafkaModelUpdateListenerContainerFactory")
  public void onSportsFeaturedPageDeleted(ConsumerRecord<String, String> data) {
    process(
        data,
        record -> {
          log.info("new SPORTS_FEATURED_PAGE_DELETED -> {} ", data);
          PageRawIndex pageIndex = PageRawIndex.fromGenerationId(record.value());
          SportsChainFactory.getFeaturedChainFactory()
              .deleteSportPage(record.value())
              .start(pageIndex);
        });
  }

  @Trace(metricName = "Incoming SPORTS_FEATURED_PAGE_ADDED", dispatcher = true)
  @KafkaListener(
      topics = "#{kafkaTopic.keyFor('SPORTS_FEATURED_PAGE_ADDED')}",
      containerFactory = "kafkaModelUpdateListenerContainerFactory")
  public void onSportsFeaturedPageAdded(ConsumerRecord<String, String> data) {
    process(
        data,
        record -> {
          log.info("new SPORTS_FEATURED_PAGE_ADDED -> {} ", data);
          PageRawIndex pageIndex = PageRawIndex.fromGenerationId(record.value());
          SportsChainFactory.getFeaturedChainFactory()
              .addSportPage(record.value())
              .start(pageIndex);
        });
  }
}
