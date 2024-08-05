package com.coral.oxygen.middleware.ms.liveserv.impl.kafka;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.ms.liveserv.impl.redis.ScoreboardCache;
import com.coral.oxygen.middleware.ms.liveserv.model.scoreboard.ScoreboardEvent;
import java.util.Optional;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.record.TimestampType;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class InternalDfKafkaConsumerTest {
  private static final String EVENT_ID = "123123";

  @Mock private ScoreboardCache cache;
  @Mock private KafkaScoreboardsPublisher publisher;
  @InjectMocks private InternalDfKafkaConsumer consumer;

  @Test
  public void newEventTest() {
    String data =
        "{\"football\" : {\"provider\" : \"opta\", \"sequenceId\" : 1, \"period\" : \"1h\"}}";
    ConsumerRecord<String, String> consumerRecord = getRecord(EVENT_ID, data);
    consumer.consume(consumerRecord);

    String expectedUpdate =
        "{\"provider\":\"opta\",\"sequenceId\":1,\"period\":\"1h\",\"obEventId\":\""
            + EVENT_ID
            + "\"}";
    verify(publisher, times(1)).publish(eq(EVENT_ID), eq(expectedUpdate));
    verify(cache, times(1)).save(any(ScoreboardEvent.class));
  }

  @Test
  public void eventUpdateTest() {
    String dataFromKafka =
        "{\"football\" : {\"provider\" : \"opta\", \"sequenceId\" : 14, \"period\" : \"1h\"}}";
    String dbData =
        "{\"football\" : {\"provider\" : \"opta\", \"sequenceId\" : 12, \"period\" : \"1h\"}}";

    when(cache.findById(EVENT_ID)).thenReturn(Optional.of(new ScoreboardEvent(EVENT_ID, dbData)));

    consumer.consume(getRecord(EVENT_ID, dataFromKafka));
    verify(cache, times(1)).save(any());
    verify(publisher, times(1)).publish(eq(EVENT_ID), anyString());
  }

  @Test
  public void oldSequenceIdTest() {
    String dataFromKafka =
        "{\"football\" : {\"provider\" : \"opta\", \"sequenceId\" : 12, \"period\" : \"1h\"}}";
    String dbData =
        "{\"football\" : {\"provider\" : \"opta\", \"sequenceId\" : 15, \"period\" : \"1h\"}}";

    when(cache.findById(EVENT_ID)).thenReturn(Optional.of(new ScoreboardEvent(EVENT_ID, dbData)));

    consumer.consume(getRecord(EVENT_ID, dataFromKafka));

    verify(cache, times(0)).save(any());
    verifyNoInteractions(publisher);
  }

  @Test
  public void sportNotSupportedTest() {
    String data =
        "{\"not_football\" : {\"provider\" : \"opta\", \"sequenceId\" : 1, \"period\" : \"1h\"}}";
    ConsumerRecord<String, String> consumerRecord = getRecord(EVENT_ID, data);
    consumer.consume(consumerRecord);

    verify(publisher, times(0)).publish(any(String.class), any(String.class));
  }

  private ConsumerRecord<String, String> getRecord(String key, String value) {
    return new ConsumerRecord<>(
        "test.scoreboards.1", 0, 0, 123, TimestampType.NO_TIMESTAMP_TYPE, 123, 1, 1, key, value);
  }
}
