package com.ladbrokescoral.oxygen.cms.kafka;

import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelineConfigDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelineMessageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.stereotype.Component;
import org.springframework.util.concurrent.ListenableFutureCallback;

@Component
@RequiredArgsConstructor
@Slf4j
public class TimelineKafkaPublisher {

  @Value(value = "${coral.topic.timeline}")
  private String coralTimelineTopic;

  @Value(value = "${ladbrokes.topic.timeline}")
  private String ladsTimelineTopic;

  private final KafkaTemplate<String, TimelineMessageDto> kafkaTemplate;

  private final KafkaTemplate<String, TimelineConfigDto> kafkaConfigTemplate;

  private final KafkaTemplate<String, TimelineMessageDto> ladsTimelineKafkaTemplate;

  private final KafkaTemplate<String, TimelineConfigDto> ladsTimelineKafkaConfigTemplate;

  public void publishTimelineMessage(String brand, TimelineMessageDto messageDto) {

    KafkaTemplate<String, TimelineMessageDto> template =
        brand.equalsIgnoreCase(Brand.BMA) ? kafkaTemplate : ladsTimelineKafkaTemplate;
    String topic = brand.equalsIgnoreCase(Brand.BMA) ? coralTimelineTopic : ladsTimelineTopic;

    template
        .send(topic, messageDto)
        .addCallback(
            new ListenableFutureCallback<SendResult<String, TimelineMessageDto>>() {
              @Override
              public void onFailure(Throwable ex) {
                log.error(
                    "TimelineKafkaPublisher:: failed to send the timeline message = {} to the topic = {} with exception = {}",
                    messageDto,
                    topic,
                    ex.getMessage());
              }

              @Override
              public void onSuccess(SendResult<String, TimelineMessageDto> result) {
                log.info(
                    "TimelineKafkaPublisher:: sent timeline message = {} to the topic = {}",
                    result.getProducerRecord().value(),
                    result.getProducerRecord().topic());
              }
            });
  }

  public void publishTimelineConfigMessage(String brand, TimelineConfigDto configDto) {

    KafkaTemplate<String, TimelineConfigDto> template =
        brand.equalsIgnoreCase(Brand.BMA) ? kafkaConfigTemplate : ladsTimelineKafkaConfigTemplate;

    String topic = brand.equalsIgnoreCase(Brand.BMA) ? coralTimelineTopic : ladsTimelineTopic;

    template
        .send(topic, configDto)
        .addCallback(
            new ListenableFutureCallback<SendResult<String, TimelineConfigDto>>() {
              @Override
              public void onFailure(Throwable ex) {
                log.error(
                    "TimelineKafkaPublisher:: failed to send the timeline config message = {} to the topic = {} with exception = {}",
                    configDto,
                    topic,
                    ex.getMessage());
              }

              @Override
              public void onSuccess(SendResult<String, TimelineConfigDto> result) {
                log.info(
                    "TimelineKafkaPublisher:: sent timeline config message = {} to the topic = {}",
                    result.getProducerRecord().value(),
                    result.getProducerRecord().topic());
              }
            });
  }
}
