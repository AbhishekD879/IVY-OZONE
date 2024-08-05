package com.ladbrokescoral.cashout.service.updates;

import static org.mockito.Mockito.times;

import com.ladbrokescoral.cashout.config.InternalKafkaTopics;
import com.ladbrokescoral.cashout.model.response.EventDto;
import com.ladbrokescoral.cashout.model.response.UpdateEventResponse;
import java.math.BigInteger;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaTemplate;

@ExtendWith(MockitoExtension.class)
class EventUpdatePublisherTest {
  @Mock private KafkaTemplate<String, Object> kafkaTemplate;
  @InjectMocks private EventUpdatePublisher eventUpdatePublisher;

  @Test
  void eventUpdateRequest() {
    BigInteger eventId = BigInteger.valueOf(776598);
    String token = "AUidu4cYsT9VJa6KYgBtRH0mE5XJ9XqJoiRxMu9Qc-R1CcgxcQSUwR5IPGINxZgjgVJSfffTHSxwc";
    EventDto eventDto = new EventDto(String.valueOf(eventId), true);
    UpdateEventResponse eventResponse = new UpdateEventResponse(eventDto);
    eventUpdatePublisher.eventUpdateRequest(token, eventId);
    String topicName = InternalKafkaTopics.EVENT_UPDATES.getTopicName();
    Mockito.verify(kafkaTemplate, times(0)).send(token, topicName, eventResponse);
  }
}
