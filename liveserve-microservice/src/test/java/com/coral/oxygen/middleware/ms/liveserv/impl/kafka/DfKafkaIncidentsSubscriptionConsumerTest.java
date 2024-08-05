package com.coral.oxygen.middleware.ms.liveserv.impl.kafka;

import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import com.coral.oxygen.middleware.ms.liveserv.impl.incidents.IncProviderValidator;
import com.coral.oxygen.middleware.ms.liveserv.impl.incidents.IncidentsCodeValidator;
import com.coral.oxygen.middleware.ms.liveserv.impl.incidents.IncidentsValidator;
import com.coral.oxygen.middleware.ms.liveserv.impl.incidents.Validator;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.record.TimestampType;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class DfKafkaIncidentsSubscriptionConsumerTest {

  private DfKafkaIncidentsSubscriptionConsumer consumer;
  @Mock KafkaIncidentsPublisher publisher;
  private Validator incidentValidator;

  public static final String EVENT_ID = "123123";
  public static final String SPORTCATEGORY = "SOCCER";
  public static final String varData =
      "{\"incident\":{\"eventId\":\"fake593f-d146-4092-ad46-8bdf192b6ebb\",\"correlationId\":\"7645316d-ddc8-42c9-ac4e-e6668704a5f6\",\"seqId\":132,\"type\":{\"code\":201,\"PASS\":\"VAR\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2022-01-03T12:43:40.342Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":601,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"BWIN\"}}";
  public static final String providerData =
      "{\"incident\":{\"eventId\":\"fake593f-d146-4092-ad46-8bdf192b6ebb\",\"correlationId\":\"7645316d-ddc8-42c9-ac4e-e6668704a5f6\",\"seqId\":132,\"type\":{\"code\":127,\"description\":\"DUMMY\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2022-01-03T12:43:40.342Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":127,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"OPTA\"}}";
  private List<Integer> codes =
      Arrays.asList(
          601, 201, 202, 203, 204, 205, 206, 207, 402, 403, 208, 220, 211, 213, 219, 210, 214, 301,
          302, 401, 500, 502, 501, 215, 216, 217, 221, 218);

  @BeforeEach
  public void setUp() {
    IncidentsValidator incidentsValidator = new IncidentsValidator(codes);
    IncProviderValidator providerValidator = new IncProviderValidator(null);
    this.incidentValidator = new IncidentsCodeValidator(providerValidator, codes);
    consumer = new DfKafkaIncidentsSubscriptionConsumer(publisher, incidentsValidator);
  }

  @Test
  void newIncidentTest() {
    String data =
        "{\"incident\":{\"eventId\":\"fake593f-d146-4092-ad46-8bdf192b6ebb\",\"correlationId\":\"7645316d-ddc8-42c9-ac4e-e6668704a5f6\",\"seqId\":117,\"type\":{\"code\":601,\"description\":\"VAR\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2022-01-03T12:43:40.342Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":601,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"OPTA\"}}";
    ConsumerRecord<String, String> consumerRecord = getRecord(data);
    consumer.consume(Optional.of(EVENT_ID), SPORTCATEGORY, consumerRecord);
    verify(publisher, times(1)).publish(EVENT_ID, data);
  }

  @Test
  void emptyEventKeyTest() {
    String data =
        "{\"incident\":{\"eventId\":\"fake593f-d146-4092-ad46-8bdf192b6ebb\",\"correlationId\":\"7645316d-ddc8-42c9-ac4e-e6668704a5f6\",\"seqId\":null,\"type\":{\"code\":601,\"description\":\"VAR\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2022-01-03T12:43:40.342Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":601,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"OPTA\"}}";
    ConsumerRecord<String, String> consumerRecord = getRecord(data);
    consumer.consume(Optional.empty(), SPORTCATEGORY, consumerRecord);
    verify(publisher, times(0)).publish(EVENT_ID, data);
  }

  @Test
  void sportNotSupportedTest() {
    String data =
        "{\"incident\":{\"eventId\":\"fake593f-d146-4092-ad46-8bdf192b6ebb\",\"correlationId\":\"7645316d-ddc8-42c9-ac4e-e6668704a5f6\",\"seqId\":null,\"type\":{\"code\":601,\"description\":\"VAR\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2022-01-03T12:43:40.342Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":601,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"OPTA\"}}";
    ConsumerRecord<String, String> consumerRecord = getRecord(data);
    consumer.consume(Optional.of(EVENT_ID), "basketball", consumerRecord);
    verify(publisher, times(0)).publish(EVENT_ID, data);
  }

  @ParameterizedTest
  @ValueSource(strings = {varData, providerData})
  void providerAndVARNotSupportedTest(String data) {
    System.out.println("In providerAndVARNotSupportedTest");
    ConsumerRecord<String, String> consumerRecord = getRecord(data);
    IncidentsValidator incidentsValidator = new IncidentsValidator(codes);
    consumer = new DfKafkaIncidentsSubscriptionConsumer(publisher, incidentsValidator);
    consumer.consume(Optional.of(EVENT_ID), SPORTCATEGORY, consumerRecord);
    publisher = Mockito.mock(KafkaIncidentsPublisher.class);
    verify(publisher, times(0)).publish(EVENT_ID, data);
  }

  private ConsumerRecord<String, String> getRecord(String value) {
    return new ConsumerRecord<>(
        "test.incidetns.1",
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
