package com.coral.oxygen.middleware.ms.liveserv.impl.kafka;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import com.coral.oxygen.middleware.ms.liveserv.impl.scoreboard.EventValidator;
import com.coral.oxygen.middleware.ms.liveserv.impl.scoreboard.FootballValidator;
import java.util.Optional;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.record.TimestampType;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class DfKafkaSubscriptionConsumerTest {

  public static final String EVENT_ID = "123123";

  @Mock private KafkaInternalDFScoreboardsPublisher publisher;
  private DfKafkaSubscriptionConsumer consumer;

  @Before
  public void init() {
    EventValidator eventValidator = new EventValidator(new FootballValidator());
    consumer = new DfKafkaSubscriptionConsumer(publisher, eventValidator);
  }

  @Test
  public void newEventTest() {
    String data =
        "{\"football\" : {\"provider\" : \"opta\", \"sequenceId\" : 1, \"period\" : \"1h\"}}";
    ConsumerRecord<String, String> consumerRecord = getRecord(data);
    consumer.consume(Optional.of(EVENT_ID), consumerRecord);

    verify(publisher, times(1)).publish(eq(EVENT_ID), eq(data));
  }

  @Test
  public void sportNotSupportedTest() {
    String data =
        "{\"not_football\" : {\"provider\" : \"opta\", \"sequenceId\" : 1, \"period\" : \"1h\"}}";
    ConsumerRecord<String, String> consumerRecord = getRecord(data);
    consumer.consume(Optional.of(EVENT_ID), consumerRecord);

    verify(publisher, times(0)).publish(any(String.class), any(String.class));
  }

  @Test
  public void preplayPeriodNotSupportedTest() {
    String data =
        "{\"football\" : {\"provider\" : \"opta\", \"sequenceId\" : 1, \"period\" : \"pre\"}}";
    ConsumerRecord<String, String> consumerRecord = getRecord(data);
    consumer.consume(Optional.of(EVENT_ID), consumerRecord);

    verify(publisher, times(0)).publish(any(String.class), any(String.class));
  }

  @Test
  public void providerNotSupportedTest() {
    String data =
        "{\"football\" : {\"provider\" : \"not-opta\", \"sequenceId\" : 1, \"period\" : \"1h\"}}";
    ConsumerRecord<String, String> consumerRecord = getRecord(data);
    consumer.consume(Optional.of(EVENT_ID), consumerRecord);

    verify(publisher, times(0)).publish(any(String.class), any(String.class));
  }

  private ConsumerRecord<String, String> getRecord(String value) {
    return new ConsumerRecord<>(
        "test.scoreboards.1",
        0,
        0,
        123,
        TimestampType.NO_TIMESTAMP_TYPE,
        123,
        1,
        1,
        "someKey",
        value);
  }
}
