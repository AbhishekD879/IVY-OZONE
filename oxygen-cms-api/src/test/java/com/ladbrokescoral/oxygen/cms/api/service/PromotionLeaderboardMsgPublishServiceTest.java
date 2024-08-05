package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.PromoMessageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.util.concurrent.ListenableFuture;
import org.springframework.util.concurrent.SettableListenableFuture;

@ExtendWith(MockitoExtension.class)
class PromotionLeaderboardMsgPublishServiceTest {

  @Mock private KafkaTemplate<String, PromoMessageDto> promoLeaderboardKafkaTemplate;

  @Mock private KafkaTemplate<String, PromoMessageDto> promoLeaderboardCoralKafkaTemplate;

  private PromotionLeaderboardMsgPublishService msgPublishService;

  private static final String LADBROKES = "ladbrokes";
  private static final String BMA = "bma";

  @BeforeEach
  public void init() {
    this.msgPublishService =
        new PromotionLeaderboardMsgPublishService(
            promoLeaderboardKafkaTemplate, promoLeaderboardCoralKafkaTemplate);
  }

  @Test
  void publishDeleteLbrMessageTest() {
    Promotion promotion = createPromotion();
    promotion.setBrand(LADBROKES);
    PromoMessageDto promoMessageDto = new PromoMessageDto();
    promoMessageDto.setBrand(LADBROKES);
    ListenableFuture<SendResult<String, PromoMessageDto>> listenableFuture =
        getPromoMsgFuture(promoMessageDto);
    Mockito.doReturn(listenableFuture)
        .when(promoLeaderboardKafkaTemplate)
        .send(Mockito.any(), Mockito.any());

    msgPublishService.publishMessage("Delete", promotion, null);
    Mockito.verify(promoLeaderboardKafkaTemplate, Mockito.times(1))
        .send(Mockito.any(), Mockito.any());
  }

  @Test
  void publishEditOrCreateCoralMessageTest() {
    Promotion promotion = createPromotion();
    promotion.setBrand(BMA);
    PromoMessageDto promoMessageDto = new PromoMessageDto();
    promoMessageDto.setBrand(BMA);

    ListenableFuture<SendResult<String, PromoMessageDto>> listenableFuture =
        getPromoMsgFuture(promoMessageDto);
    Mockito.doReturn(listenableFuture)
        .when(promoLeaderboardCoralKafkaTemplate)
        .send(Mockito.any(), Mockito.any());

    msgPublishService.publishMessage("Edit", promotion, null);
    Mockito.verify(promoLeaderboardCoralKafkaTemplate, Mockito.times(1))
        .send(Mockito.any(), Mockito.any());
  }

  @Test
  void publishEditOrCreateCoralMessageTestWithException() {
    Promotion promotion = createPromotion();
    promotion.setBrand(BMA);
    PromoMessageDto promoMessageDto = new PromoMessageDto();
    promoMessageDto.setBrand(BMA);

    SettableListenableFuture<SendResult<String, PromoMessageDto>> listenableFuture =
        new SettableListenableFuture<>();
    listenableFuture.setException(new Exception());
    Mockito.doReturn(listenableFuture)
        .when(promoLeaderboardCoralKafkaTemplate)
        .send(Mockito.any(), Mockito.any());

    msgPublishService.publishMessage("Edit", promotion, null);
    Mockito.verify(promoLeaderboardCoralKafkaTemplate, Mockito.times(1))
        .send(Mockito.any(), Mockito.any());
  }

  private Promotion createPromotion() {
    Promotion promotion = new Promotion();
    promotion.setId("123");
    promotion.setPromoKey("456");
    return promotion;
  }

  private ListenableFuture<SendResult<String, PromoMessageDto>> getPromoMsgFuture(Object object) {
    SettableListenableFuture<SendResult<String, PromoMessageDto>> future =
        new SettableListenableFuture<>();
    RecordMetadata recordMetadata = new RecordMetadata(null, 1L, 2L, 3L, 4L, 1, 2);
    ProducerRecord<String, PromoMessageDto> producerRecord =
        new ProducerRecord<>("leaderboard", (PromoMessageDto) object);
    SendResult<String, PromoMessageDto> sendResult =
        new SendResult<>(producerRecord, recordMetadata);
    future.set(sendResult);
    return future;
  }
}
