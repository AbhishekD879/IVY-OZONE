package com.coral.oxygen.middleware.ms.liveserv.impl.kafka;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.scheduling.annotation.AsyncResult;

@RunWith(MockitoJUnitRunner.class)
public class KafkaIncidentsPublisherTest {

  private static final String TOPIC = "test.incidents.1";
  private static final String key = "124235";
  @Mock KafkaTemplate<String, String> kafkaTemplate;

  @Mock AsyncResult asyncResult;

  KafkaIncidentsPublisher kafkaIncidentsPublisher;

  @Before
  public void init() {
    kafkaIncidentsPublisher = new KafkaIncidentsPublisher(kafkaTemplate, TOPIC);
    when(kafkaTemplate.send(any(), any(), any())).thenReturn(asyncResult);
  }

  @Test
  public void testSendNotification() {
    String data =
        "{\"incident\":{\"eventId\":\"fake11a5-53bb-42ad-8f4c-7a8fa40ab9fa\",\"correlationId\":\"04ed57c3-ac16-49c2-bd50-960a570240fe\",\"seqId\":null,\"type\":{\"code\":601,\"description\":\"VAR\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2021-12-30T12:30:26.527Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":601,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"OPTA\"}}";
    kafkaIncidentsPublisher.publish(key, data);
    verify(kafkaTemplate, times(1)).send(TOPIC, key, data);
  }
}
