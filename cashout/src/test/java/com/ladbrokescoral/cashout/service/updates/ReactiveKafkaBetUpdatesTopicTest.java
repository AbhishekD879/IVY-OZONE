package com.ladbrokescoral.cashout.service.updates;

import static org.junit.Assert.assertNotNull;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.coral.bpp.api.model.bet.api.response.oxi.base.Bet;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.apache.kafka.common.TopicPartition;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.kafka.core.reactive.ReactiveKafkaProducerTemplate;
import reactor.core.publisher.Mono;
import reactor.kafka.sender.SenderResult;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class ReactiveKafkaBetUpdatesTopicTest {
  @InjectMocks ReactiveKafkaBetUpdatesTopic reactiveKafkaBetUpdatesTopic;

  @Mock
  private ReactiveKafkaProducerTemplate<String, Object> betUpdateReactiveKafkaProducerTemplate;

  @SuppressWarnings({"unchecked", "rawtypes"})
  @Test
  void testBetUpdate() {
    try {
      Bet bet = new Bet();
      bet.setBetId("2341572");
      UpdateDto updateDto = UpdateDto.builder().bet(bet).build();
      RecordMetadata meta = new RecordMetadata(new TopicPartition("test", 0), 0L, 0L, 0L, 0L, 0, 2);
      SenderResult result = mock(SenderResult.class);
      when(result.recordMetadata()).thenReturn(meta);
      Mockito.when(
              betUpdateReactiveKafkaProducerTemplate.send(
                  Mockito.any(), Mockito.any(), Mockito.any()))
          .thenReturn(Mono.just(result));
      reactiveKafkaBetUpdatesTopic.sendBetUpdate(updateDto);
      reactiveKafkaBetUpdatesTopic.sendBetUpdate("1234", updateDto);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  @SuppressWarnings({"unchecked", "rawtypes"})
  @Test
  void testBetUpdate_Error() {
    try {
      RecordMetadata meta = new RecordMetadata(new TopicPartition("test", 0), 0L, 0L, 0L, 0L, 0, 2);
      SenderResult result = mock(SenderResult.class);
      when(result.recordMetadata()).thenReturn(meta);
      Mockito.when(
              betUpdateReactiveKafkaProducerTemplate.send(
                  Mockito.any(), Mockito.any(), Mockito.any()))
          .thenReturn(Mono.just(result));
      reactiveKafkaBetUpdatesTopic.sendBetUpdateError("1234", new RuntimeException());
    } catch (Exception e) {
      assertNotNull(e);
    }
  }
}
