package com.entain.oxygen.kafka;

import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import com.entain.oxygen.service.RtmsKafkaPublisherService;
import lombok.SneakyThrows;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.record.TimestampType;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class DfKafkaConsumerTest {
  @InjectMocks DfKafkaConsumer dfConsumer;
  @Mock private RtmsKafkaPublisherService dfScoreboardService;

  @SneakyThrows
  @Test
  void consumeUpdateTest() {
    dfConsumer.consumeUpdate(getRecord("45"));
    verify(dfScoreboardService, times(1)).processMessage(Mockito.any());
  }

  private ConsumerRecord<String, String> getRecord(String value) {
    return new ConsumerRecord<>(
        "df-fanzone-player-preferences",
        0,
        0,
        123,
        TimestampType.NO_TIMESTAMP_TYPE,
        123,
        1,
        1,
        "dfsdgsdgfddsere::test::rtms",
        value);
  }
}
