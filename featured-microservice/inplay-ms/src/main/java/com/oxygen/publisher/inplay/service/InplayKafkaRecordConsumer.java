package com.oxygen.publisher.inplay.service;

import com.newrelic.api.agent.Trace;
import com.oxygen.publisher.service.KafkaTopic;
import com.oxygen.publisher.updates.AbstractKafkaNotificationConsumer;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.KafkaListener;

@Configuration
@Slf4j
@RequiredArgsConstructor
public class InplayKafkaRecordConsumer extends AbstractKafkaNotificationConsumer {

  protected final KafkaTopic kafkaTopic;

  @Trace(metricName = "Incoming live update from Kafka", dispatcher = true)
  @KafkaListener(
      topics = "${kafka.topics.prefix}__${kafka.live.update.topic.name}",
      containerFactory = "kafkaLiveUpdateListenerContainerFactory")
  public void onLiveUpdate(ConsumerRecord<String, String> data) {
    process(
        data,
        record ->
            InplayChainFactory.getInplayChainFactory()
                .processLiveUpdate(record.key(), record.value()));
  }

  @Trace(metricName = "Incoming IN_PLAY_STRUCTURE_CHANGED", dispatcher = true)
  @KafkaListener(
      topics = "#{kafkaTopic.keyFor('IN_PLAY_STRUCTURE_CHANGED')}",
      containerFactory = "kafkaModelUpdateListenerContainerFactory")
  public void onInplayDataChange(ConsumerRecord<String, String> data) {
    process(
        data,
        record -> {
          InplayChainFactory.getInplayChainFactory().inplayDataChanged().start(record.value());
        });
  }

  @Trace(metricName = "Incoming IN_PLAY_SPORTS_RIBBON_CHANGED", dispatcher = true)
  @KafkaListener(
      topics = "#{kafkaTopic.keyFor('IN_PLAY_SPORTS_RIBBON_CHANGED')}",
      containerFactory = "kafkaModelUpdateListenerContainerFactory")
  public void onSportsRibbonChange(ConsumerRecord<String, String> data) {
    process(
        data,
        record ->
            InplayChainFactory.getInplayChainFactory().sportsRibbonChanged().start(record.value()));
  }

  @Trace(metricName = "Incoming IN_PLAY_SPORT_SEGMENT_CHANGED", dispatcher = true)
  @KafkaListener(
      topics = "#{kafkaTopic.keyFor('IN_PLAY_SPORT_SEGMENT_CHANGED')}",
      containerFactory = "kafkaModelUpdateListenerContainerFactory")
  public void onSportSegmentsChange(ConsumerRecord<String, String> data) {
    process(
        data,
        record ->
            InplayChainFactory.getInplayChainFactory()
                .onSportSegmentsChanged()
                .start(record.value()));
  }

  @Trace(metricName = "Incoming IN_PLAY_SPORT_COMPETITION_CHANGED", dispatcher = true)
  @KafkaListener(
      topics = "#{kafkaTopic.keyFor('IN_PLAY_SPORT_COMPETITION_CHANGED')}",
      containerFactory = "kafkaModelUpdateListenerContainerFactory")
  public void onSportCompetitionChange(ConsumerRecord<String, String> data) {
    process(
        data,
        record ->
            InplayChainFactory.getInplayChainFactory()
                .processCompetitionChanges()
                .start(record.value()));
  }

  /**
   * Listener for virtual sports
   *
   * @param data
   */
  @Trace(metricName = "Incoming VIRTUAL_SPORTS_RIBBON_CHANGED", dispatcher = true)
  @KafkaListener(
      topics = "#{kafkaTopic.keyFor('VIRTUAL_SPORTS_RIBBON_CHANGED')}",
      containerFactory = "kafkaModelUpdateListenerContainerFactory")
  public void onVirtualSportsRibbonChange(ConsumerRecord<String, String> data) {
    process(
        data,
        rec ->
            InplayChainFactory.getInplayChainFactory()
                .virtualSportsRibbonChanged()
                .start(rec.value()));
  }
}
