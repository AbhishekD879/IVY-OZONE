package com.ladbrokescoral.cashout.config;

import static org.junit.Assert.assertNotNull;

import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import com.ladbrokescoral.cashout.service.updates.BetDetailRequestCtx;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import reactor.kafka.receiver.ReceiverOptions;

@RunWith(MockitoJUnitRunner.class)
class ReactiveKafkaConsumerConfigTest {

  private ReactiveKafkaConsumerConfig reactiveKafkaConsumerConfig;
  @Mock private ReceiverOptions<String, BetDetailRequestCtx> receiverOptions;
  @Mock private ReceiverOptions<String, CashoutRequest> cashoutreReceiverOptions;
  @Mock private ReceiverOptions<String, UpdateDto> updateDtoReceiverOptions;
  @Mock private ReceiverOptions<String, Throwable> throwableReceiverOptions;

  @BeforeEach
  public void init() {
    reactiveKafkaConsumerConfig = new ReactiveKafkaConsumerConfig();
    receiverOptions = ReceiverOptions.create();
    cashoutreReceiverOptions = ReceiverOptions.create();
    updateDtoReceiverOptions = ReceiverOptions.create();
    throwableReceiverOptions = ReceiverOptions.create();
  }

  @Test
  void testkafkaReceiverOptions() {
    InternalKafkaProperties properties = new InternalKafkaProperties();
    KafkaProperties props = new KafkaProperties();
    properties.setKafka(props);
    assertNotNull(reactiveKafkaConsumerConfig.kafkaReceiverOptions(properties));
  }

  @Test
  void testReactiveKafkaConsumerTemplate() {
    assertNotNull(reactiveKafkaConsumerConfig.reactiveKafkaConsumerTemplate(receiverOptions));
  }

  @Test
  void testBetDetailKafkaReceiverOptions() {
    InternalKafkaProperties properties = new InternalKafkaProperties();
    KafkaProperties props = new KafkaProperties();
    properties.setKafka(props);
    assertNotNull(reactiveKafkaConsumerConfig.betDetailKafkaReceiverOptions(properties));
  }

  @Test
  void testBetDetailreactiveKafkaConsumerTemplate() {
    assertNotNull(
        reactiveKafkaConsumerConfig.betDetailreactiveKafkaConsumerTemplate(
            cashoutreReceiverOptions));
  }

  @Test
  void testBetUpdatesKafkaReceiverOptions() {
    InternalKafkaProperties properties = new InternalKafkaProperties();
    KafkaProperties props = new KafkaProperties();
    properties.setKafka(props);
    assertNotNull(reactiveKafkaConsumerConfig.betUpdatesKafkaReceiverOptions(properties));
  }

  @Test
  void testBetUpdatesReactiveKafkaConsumerTemplate() {
    assertNotNull(
        reactiveKafkaConsumerConfig.betUpdatesReactiveKafkaConsumerTemplate(
            updateDtoReceiverOptions));
  }

  @Test
  void testBetUpdatesErrorKafkaReceiverOptions() {
    InternalKafkaProperties properties = new InternalKafkaProperties();
    KafkaProperties props = new KafkaProperties();
    properties.setKafka(props);
    assertNotNull(reactiveKafkaConsumerConfig.betUpdatesErrorKafkaReceiverOptions(properties));
  }

  @Test
  void testBetUpdatesErrorReactiveKafkaConsumerTemplate() {
    assertNotNull(
        reactiveKafkaConsumerConfig.betUpdatesErrorReactiveKafkaConsumerTemplate(
            throwableReceiverOptions));
  }
}
