package com.ladbrokescoral.oxygen.betpackmp.kafka;

import static com.ladbrokescoral.oxygen.betpackmp.constants.BetPackConstants.ACTIVE_BET_PACK_IDS;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.betpackmp.redis.ActiveBetPacks;
import com.ladbrokescoral.oxygen.betpackmp.redis.BetPackRedisService;
import java.util.*;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.record.TimestampType;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class ActiveBetPackKafkaConsumerTest implements WithAssertions {

  @Mock private BetPackRedisService service;
  @InjectMocks private ActiveBetPackKafkaConsumer consumer;

  @Test
  void consumeWithSameBetPackIds() {
    List<String> data = Arrays.asList("betPackId_1", "betPackId_2", "betPackId_3");
    ActiveBetPacks activeBetPacks = new ActiveBetPacks(data);
    ConsumerRecord<String, List<String>> consumerRecord = getRecord(data);
    when(service.getActiveBetPacks(ACTIVE_BET_PACK_IDS)).thenReturn(activeBetPacks);
    consumer.consume(consumerRecord);
    verify(service, times(0)).put(activeBetPacks);
    Assertions.assertDoesNotThrow(() -> consumer.consume(consumerRecord));
  }

  @Test
  void consumeWithDifferentSameBetPackIds() {
    List<String> data = Arrays.asList("betPackId_1", "betPackId_2", "betPackId_3");
    ActiveBetPacks activeBetPacks = new ActiveBetPacks(data);
    ConsumerRecord<String, List<String>> consumerRecord =
        getRecord(Arrays.asList("323", "564", "676"));
    when(service.getActiveBetPacks(ACTIVE_BET_PACK_IDS)).thenReturn(activeBetPacks);
    consumer.consume(consumerRecord);
    verify(service, times(1)).put(new ActiveBetPacks(consumerRecord.value()));
    Assertions.assertDoesNotThrow(() -> consumer.consume(consumerRecord));
  }

  @Test
  void consumeWithNullConsumerRecord() {
    ConsumerRecord<String, List<String>> consumerRecord = getRecord(null);
    consumer.consume(consumerRecord);
    Assertions.assertDoesNotThrow(() -> consumer.consume(consumerRecord));
  }

  @Test
  void consumeWithNullBetPackIds() {
    List<String> data = Collections.emptyList();
    ConsumerRecord<String, List<String>> consumerRecord = getRecord(data);
    when(service.getActiveBetPacks(ACTIVE_BET_PACK_IDS)).thenReturn(new ActiveBetPacks(data));
    consumer.consume(consumerRecord);
    verify(service, times(0)).put(new ActiveBetPacks(consumerRecord.value()));
    Assertions.assertDoesNotThrow(() -> consumer.consume(consumerRecord));
  }

  @Test
  void consumeWithNullConsumerRecordBetPackIds() {
    List<String> data = Collections.emptyList();
    ConsumerRecord<String, List<String>> consumerRecord = getRecord(data);
    when(service.getActiveBetPacks(ACTIVE_BET_PACK_IDS))
        .thenReturn(new ActiveBetPacks(Arrays.asList("7687")));
    consumer.consume(consumerRecord);
    verify(service, times(0)).put(new ActiveBetPacks(consumerRecord.value()));
    Assertions.assertDoesNotThrow(() -> consumer.consume(consumerRecord));
  }

  @Test
  void consumeWithDifferentSizeBetPackIds_1() {
    List<String> data = Arrays.asList("betPackId_1", "betPackId_2", "betPackId_3");
    ActiveBetPacks activeBetPacks = new ActiveBetPacks(data);
    ConsumerRecord<String, List<String>> consumerRecord =
        getRecord(Arrays.asList("betPackId_1", "betPackId_2"));
    when(service.getActiveBetPacks(ACTIVE_BET_PACK_IDS)).thenReturn(activeBetPacks);
    consumer.consume(consumerRecord);
    verify(service, times(1)).put(new ActiveBetPacks(consumerRecord.value()));
    Assertions.assertDoesNotThrow(() -> consumer.consume(consumerRecord));
  }

  @Test
  void consumeWithDifferentSizeBetPackIds_2() {
    List<String> data = Arrays.asList("betPackId_1", "betPackId_2");
    ActiveBetPacks activeBetPacks = new ActiveBetPacks(data);
    ConsumerRecord<String, List<String>> consumerRecord =
        getRecord(Arrays.asList("betPackId_1", "betPackId_2", "betPackId_3"));
    when(service.getActiveBetPacks(ACTIVE_BET_PACK_IDS)).thenReturn(activeBetPacks);
    consumer.consume(consumerRecord);
    verify(service, times(1)).put(new ActiveBetPacks(consumerRecord.value()));
    Assertions.assertDoesNotThrow(() -> consumer.consume(consumerRecord));
  }

  private ConsumerRecord<String, List<String>> getRecord(List<String> values) {
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
        values);
  }
}
