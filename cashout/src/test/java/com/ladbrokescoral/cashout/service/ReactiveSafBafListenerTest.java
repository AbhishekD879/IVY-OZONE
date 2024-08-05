package com.ladbrokescoral.cashout.service;

import static org.mockito.Mockito.times;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.cashout.model.safbaf.Event;
import com.ladbrokescoral.cashout.model.safbaf.Meta;
import com.ladbrokescoral.cashout.model.safbaf.betslip.Betslip;
import com.ladbrokescoral.cashout.util.TestUtil;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.header.Header;
import org.apache.kafka.common.header.Headers;
import org.apache.kafka.common.header.internals.RecordHeaders;
import org.apache.kafka.common.record.TimestampType;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.kafka.core.reactive.ReactiveKafkaConsumerTemplate;
import org.springframework.messaging.SubscribableChannel;
import reactor.core.publisher.Flux;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class ReactiveSafBafListenerTest {

  @InjectMocks private ReactiveSafBafListener reactiveSafBafListener;
  @Mock private ReactiveKafkaConsumerTemplate<String, String> safUpdatesListenerTemplate;
  @Mock private SubscribableChannel messageChannel;
  @Mock private TopicContentConverter converter;

  @Test
  void testConsumesafUpdate_error() throws Exception {
    when(safUpdatesListenerTemplate.receiveAutoAck()).thenReturn(Flux.error(new Throwable()));
    reactiveSafBafListener.run();
    Mockito.verify(converter, times(0)).convertSafUpdateToPojo(Mockito.any());
  }

  @Test
  void testTestConsumeSafUpdate() throws Exception {
    List<Header> headers = new ArrayList<>();
    Headers header = new RecordHeaders(headers);
    String message = TestUtil.readFromFile("/com/ladbrokescoral/cashout/service/selection.json");
    ConsumerRecord<String, String> record =
        new ConsumerRecord<>(
            "saf-update",
            0,
            0,
            123,
            TimestampType.NO_TIMESTAMP_TYPE,
            123L,
            1,
            1,
            "saf-update",
            message,
            header);
    Meta meta = new Meta();
    meta.setMessageTimestamp("123");
    meta.setOperation("add");
    Betslip betslip = new Betslip();
    betslip.setBetChannel("betchannel");
    betslip.setMeta(meta);

    Event event = new Event();
    event.setEventKey(BigInteger.valueOf(123));
    event.setIsEventStarted("true");
    event.setMeta(meta);
    when(safUpdatesListenerTemplate.receiveAutoAck()).thenReturn(Flux.just(record));
    when(converter.convertBetslipUpdateToPojo(Mockito.any())).thenReturn(Optional.of(betslip));
    when(converter.convertSafUpdateToPojo(Mockito.any())).thenReturn(Optional.of(event));
    reactiveSafBafListener.processBafUpdate(record);
    reactiveSafBafListener.processSafUpdate(record);
    reactiveSafBafListener.processIfNotNull(null, message, null);
    Mockito.verify(converter).convertSafUpdateToPojo(Mockito.any());
  }

  @Test
  void testProcessBafUpdateValue_Null() {
    List<Header> headers = new ArrayList<>();
    Headers header = new RecordHeaders(headers);
    ConsumerRecord<String, String> record =
        new ConsumerRecord<>(
            "saf-update",
            0,
            0,
            123,
            TimestampType.NO_TIMESTAMP_TYPE,
            123L,
            1,
            1,
            "saf-update",
            null,
            header);
    reactiveSafBafListener.processSafUpdate(record);
    Mockito.verify(converter, times(0)).convertSafUpdateToPojo(Mockito.any());
  }

  @Test
  void testProcessBafUpdate_EmptyEntity() {
    List<Header> headers = new ArrayList<>();
    Headers header = new RecordHeaders(headers);
    ConsumerRecord<String, String> record =
        new ConsumerRecord<>(
            "saf-update",
            0,
            0,
            123,
            TimestampType.NO_TIMESTAMP_TYPE,
            123L,
            1,
            1,
            "saf-update",
            "",
            header);
    when(converter.convertSafUpdateToPojo(Mockito.any())).thenReturn(Optional.empty());
    reactiveSafBafListener.processSafUpdate(record);
    Mockito.verify(converter).convertSafUpdateToPojo(Mockito.any());
  }

  @Test
  void testProcessBafUpdate() {
    List<Header> headers = new ArrayList<>();
    Headers header = new RecordHeaders(headers);
    ConsumerRecord<String, String> record =
        new ConsumerRecord<>(
            "saf-update",
            0,
            0,
            123,
            TimestampType.NO_TIMESTAMP_TYPE,
            123L,
            1,
            1,
            "saf-update",
            "",
            header);
    Meta meta1 = new Meta();
    meta1.setMessageTimestamp("123");
    meta1.setOperation("update");
    Event event1 = new Event();
    event1.setEventKey(BigInteger.valueOf(123));
    event1.setIsEventStarted("true");
    event1.setMeta(meta1);
    when(converter.convertSafUpdateToPojo(Mockito.any())).thenReturn(Optional.of(event1));
    reactiveSafBafListener.processSafUpdate(record);
    Mockito.verify(converter).convertSafUpdateToPojo(Mockito.any());
  }
}
