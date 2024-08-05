package com.entain.oxygen.promosandbox.consumer;

import static org.junit.jupiter.api.Assertions.assertNotNull;

import com.entain.oxygen.promosandbox.dto.PromoMessageDto;
import com.entain.oxygen.promosandbox.handler.PromoConfigMessageHandler;
import com.entain.oxygen.promosandbox.kafka.consumer.PromoConfigConsumer;
import com.entain.oxygen.promosandbox.utils.TestUtil;
import com.google.gson.Gson;
import com.google.gson.JsonParseException;
import java.io.IOException;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.record.TimestampType;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(SpringExtension.class)
class PromoConfigConsumerTest {

  @Mock private PromoConfigMessageHandler promoConfigHandler;

  @InjectMocks private PromoConfigConsumer promoConfigConsumer;

  private static PromoMessageDto promoMessageDto;

  @BeforeAll
  static void setup() throws IOException {
    promoMessageDto = TestUtil.deserializeWithJackson("/promoMessage.json", PromoMessageDto.class);
  }

  @BeforeEach
  void beforeEachSetup() {
    ReflectionTestUtils.setField(
        promoConfigConsumer, "promoConfigMessageHandler", promoConfigHandler);
  }

  @Test
  void consumerIdSuccessTest() {
    Mockito.doNothing().when(promoConfigHandler).handleKafkaMessage(Mockito.any());
    assertNotNull(promoConfigConsumer);
    promoConfigConsumer.consumeRequest(getRecord(new Gson().toJson(promoMessageDto)));
  }

  @Test
  void consumerIdInvalidDataTest() {
    Mockito.doThrow(JsonParseException.class)
        .when(promoConfigHandler)
        .handleKafkaMessage(Mockito.any());
    assertNotNull(promoConfigConsumer);
    promoConfigConsumer.consumeRequest(getRecord("{promoId:23232}"));
  }

  private ConsumerRecord<String, String> getRecord(String value) {
    return new ConsumerRecord<>(
        "test.promosandbox.1",
        0,
        0,
        123,
        TimestampType.NO_TIMESTAMP_TYPE,
        123,
        1,
        1,
        "dfsdgsdgfddsere",
        value);
  }
}
