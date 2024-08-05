package com.ladbrokescoral.oxygen.cms.kafka;

import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelineConfigDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelineMessageDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelinePostDto;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.util.concurrent.ListenableFuture;
import org.springframework.util.concurrent.SettableListenableFuture;

@ExtendWith(MockitoExtension.class)
class TimelineKafkaPublisherTest {

  @Mock private KafkaTemplate<String, TimelineMessageDto> kafkaTemplate;

  @Mock private KafkaTemplate<String, TimelineConfigDto> kafkaConfigTemplate;

  @Mock private KafkaTemplate<String, TimelineMessageDto> ladsTimelineKafkaTemplate;

  @Mock private KafkaTemplate<String, TimelineConfigDto> ladsTimelineKafkaConfigTemplate;

  private TimelineKafkaPublisher timelineKafkaPublisher;

  @BeforeEach
  public void init() {
    this.timelineKafkaPublisher =
        new TimelineKafkaPublisher(
            kafkaTemplate,
            kafkaConfigTemplate,
            ladsTimelineKafkaTemplate,
            ladsTimelineKafkaConfigTemplate);
  }

  @Test
  void testPublishTimelineConfigCoral() {
    TimelineConfigDto timelineConfigDto = new TimelineConfigDto();
    timelineConfigDto.setBrand("bma");
    ListenableFuture<SendResult<String, TimelineConfigDto>> listenableFuture =
        getConfigFuture(timelineConfigDto);
    Mockito.doReturn(listenableFuture).when(kafkaConfigTemplate).send(Mockito.any(), Mockito.any());
    this.timelineKafkaPublisher.publishTimelineConfigMessage("bma", timelineConfigDto);
    Mockito.verify(kafkaConfigTemplate, Mockito.times(1)).send(Mockito.any(), Mockito.any());
  }

  @Test
  void testPublishTimelineConfigLadbrokes() {
    TimelineConfigDto timelineConfigDto = new TimelineConfigDto();
    timelineConfigDto.setBrand("ladbrokes");
    ListenableFuture<SendResult<String, TimelineConfigDto>> future =
        getConfigFuture(timelineConfigDto);
    Mockito.doReturn(future)
        .when(ladsTimelineKafkaConfigTemplate)
        .send(Mockito.any(), Mockito.any());
    this.timelineKafkaPublisher.publishTimelineConfigMessage("ladbrokes", timelineConfigDto);
    Mockito.verify(ladsTimelineKafkaConfigTemplate, Mockito.times(1))
        .send(Mockito.any(), Mockito.any());
  }

  @Test
  void testPublishTimelineMessageCoral() {

    TimelineMessageDto messageDto = new TimelinePostDto();

    messageDto.setBrand("bma");
    messageDto.setId("11");

    ListenableFuture<SendResult<String, TimelineMessageDto>> future = getMessageFuture(messageDto);

    Mockito.doReturn(future).when(kafkaTemplate).send(Mockito.any(), Mockito.any());

    this.timelineKafkaPublisher.publishTimelineMessage("bma", messageDto);

    Mockito.verify(kafkaTemplate, Mockito.times(1)).send(Mockito.any(), Mockito.any());
  }

  @Test
  void testPublishTimelineMessageLadbrokes() {

    TimelineMessageDto messageDto = new TimelinePostDto();
    messageDto.setBrand("ladbrokes");
    messageDto.setId("22");

    ListenableFuture<SendResult<String, TimelineMessageDto>> future = getMessageFuture(messageDto);
    Mockito.doReturn(future).when(ladsTimelineKafkaTemplate).send(Mockito.any(), Mockito.any());
    this.timelineKafkaPublisher.publishTimelineMessage("ladbrokes", messageDto);
    Mockito.verify(ladsTimelineKafkaTemplate, Mockito.times(1)).send(Mockito.any(), Mockito.any());
  }

  @Test
  void testPublishTimelineConfigCoralException() {
    TimelineConfigDto timelineConfigDto = new TimelineConfigDto();
    timelineConfigDto.setBrand("bma");
    SettableListenableFuture<SendResult<String, TimelineConfigDto>> future =
        new SettableListenableFuture<>();
    future.setException(new Exception());
    Mockito.doReturn(future).when(kafkaConfigTemplate).send(Mockito.any(), Mockito.any());
    this.timelineKafkaPublisher.publishTimelineConfigMessage("bma", timelineConfigDto);
    Mockito.verify(kafkaConfigTemplate, Mockito.times(1)).send(Mockito.any(), Mockito.any());
  }

  @Test
  void testPublishTimelineConfigLadsException() {
    TimelineConfigDto timelineConfigDto = new TimelineConfigDto();
    timelineConfigDto.setBrand("ladbrokes");
    SettableListenableFuture<SendResult<String, TimelineConfigDto>> future =
        new SettableListenableFuture<>();
    future.setException(new Exception());
    Mockito.doReturn(future)
        .when(ladsTimelineKafkaConfigTemplate)
        .send(Mockito.any(), Mockito.any());
    this.timelineKafkaPublisher.publishTimelineConfigMessage("ladbrokes", timelineConfigDto);
    Mockito.verify(ladsTimelineKafkaConfigTemplate, Mockito.times(1))
        .send(Mockito.any(), Mockito.any());
  }

  @Test
  void testPublishTimelineMessageCoralException() {

    TimelineMessageDto messageDto = new TimelinePostDto();
    messageDto.setId("11");
    messageDto.setBrand("bma");
    SettableListenableFuture<SendResult<String, TimelineMessageDto>> future =
        new SettableListenableFuture<>();
    future.setException(new Exception());
    Mockito.doReturn(future).when(kafkaTemplate).send(Mockito.any(), Mockito.any());
    this.timelineKafkaPublisher.publishTimelineMessage("bma", messageDto);
    Mockito.verify(kafkaTemplate, Mockito.times(1)).send(Mockito.any(), Mockito.any());
  }

  @Test
  void testPublishTimelineMessageLadbrokesException() {

    TimelineMessageDto messageDto = new TimelinePostDto();
    messageDto.setId("11");
    messageDto.setBrand("ladbrokes");
    SettableListenableFuture<SendResult<String, TimelineMessageDto>> future =
        new SettableListenableFuture<>();
    future.setException(new Exception());
    Mockito.doReturn(future).when(ladsTimelineKafkaTemplate).send(Mockito.any(), Mockito.any());
    this.timelineKafkaPublisher.publishTimelineMessage("ladbrokes", messageDto);
    Mockito.verify(ladsTimelineKafkaTemplate, Mockito.times(1)).send(Mockito.any(), Mockito.any());
  }

  private ListenableFuture<SendResult<String, TimelineConfigDto>> getConfigFuture(Object object) {

    SettableListenableFuture<SendResult<String, TimelineConfigDto>> future =
        new SettableListenableFuture<>();
    RecordMetadata recordMetadata = new RecordMetadata(null, 1L, 2L, 3L, 4L, 1, 2);
    ProducerRecord<String, TimelineConfigDto> producerRecord =
        new ProducerRecord<>("timeline", (TimelineConfigDto) object);
    SendResult<String, TimelineConfigDto> sendResult =
        new SendResult<>(producerRecord, recordMetadata);
    future.set(sendResult);
    return future;
  }

  private ListenableFuture<SendResult<String, TimelineMessageDto>> getMessageFuture(Object object) {

    SettableListenableFuture<SendResult<String, TimelineMessageDto>> future =
        new SettableListenableFuture<>();
    RecordMetadata recordMetadata = new RecordMetadata(null, 1L, 2L, 3L, 4L, 1, 2);
    ProducerRecord<String, TimelineMessageDto> producerRecord =
        new ProducerRecord<>("timeline", (TimelineMessageDto) object);
    SendResult<String, TimelineMessageDto> sendResult =
        new SendResult<>(producerRecord, recordMetadata);
    future.set(sendResult);
    return future;
  }
}
