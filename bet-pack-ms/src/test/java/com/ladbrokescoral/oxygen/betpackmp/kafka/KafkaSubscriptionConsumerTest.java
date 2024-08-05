package com.ladbrokescoral.oxygen.betpackmp.kafka;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.betpackmp.exception.BetPackMarketPlaceException;
import com.ladbrokescoral.oxygen.betpackmp.service.BetPackService;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.record.TimestampType;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class KafkaSubscriptionConsumerTest implements WithAssertions {

  @Mock private BetPackService betPackService;

  @InjectMocks private KafkaSubscriptionConsumer kafkaSubscriptionConsumer;

  @BeforeEach
  public void init() {
    kafkaSubscriptionConsumer = new KafkaSubscriptionConsumer(betPackService);
  }

  @Test
  void consumeWithValidBetPackId() {
    ConsumerRecord<String, String> consumerRecord = getRecord("someKey", "8787687");
    kafkaSubscriptionConsumer.consume(consumerRecord);
    verify(betPackService, times(1)).processBetPacks(consumerRecord.key());
    Assertions.assertDoesNotThrow(() -> kafkaSubscriptionConsumer.consume(consumerRecord));
  }

  @Test
  void consumeWithInValidBetPackId() {
    ConsumerRecord<String, String> consumerRecord = getRecord(null, "876");
    kafkaSubscriptionConsumer.consume(consumerRecord);
    verify(betPackService, times(0)).processBetPacks(consumerRecord.key());
    Assertions.assertDoesNotThrow(() -> kafkaSubscriptionConsumer.consume(consumerRecord));
  }

  @Test()
  void consumeWithException() {
    assertThrows(
        Exception.class,
        () -> kafkaSubscriptionConsumer.consume(null),
        "Expected consume() to throw");
  }

  @Test()
  void consumeWithExceptionTest() {
    ConsumerRecord<String, String> consumerRecord = getRecord("someKey", "876");
    doThrow(BetPackMarketPlaceException.class).when(betPackService).processBetPacks("someKey");
    BetPackMarketPlaceException thrown =
        assertThrows(
            BetPackMarketPlaceException.class,
            () -> kafkaSubscriptionConsumer.consume(consumerRecord),
            "Expected doThing() to throw, but it didn't");
    assertTrue(thrown.getMessage().contains("subscription"));
  }

  private ConsumerRecord<String, String> getRecord(String key, String betPackId) {
    return new ConsumerRecord<>(
        "test.scoreboards.1",
        0,
        0,
        123,
        TimestampType.NO_TIMESTAMP_TYPE,
        123,
        1,
        1,
        key,
        betPackId);
  }
}
