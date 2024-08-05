package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.PromoMessageDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromoMsgLbConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.stereotype.Component;
import org.springframework.util.concurrent.ListenableFutureCallback;
import org.springframework.validation.annotation.Validated;

@Slf4j
@Component
@Validated
public class PromotionLeaderboardMsgPublishService {

  @Value(value = "${ladbrokes.kafka.topic.leaderboard-promo}")
  private String leaderboardPromoTopic;

  @Value(value = "${coral.kafka.topic.leaderboard-promo-coral}")
  private String leaderboardPromoCoralTopic;

  private final KafkaTemplate<String, PromoMessageDto> promoLeaderboardKafkaTemplate;
  private final KafkaTemplate<String, PromoMessageDto> promoLeaderboardCoralKafkaTemplate;

  @Autowired
  public PromotionLeaderboardMsgPublishService(
      KafkaTemplate<String, PromoMessageDto> promoLeaderboardKafkaTemplate,
      KafkaTemplate<String, PromoMessageDto> promoLeaderboardCoralKafkaTemplate) {
    this.promoLeaderboardKafkaTemplate = promoLeaderboardKafkaTemplate;
    this.promoLeaderboardCoralKafkaTemplate = promoLeaderboardCoralKafkaTemplate;
  }

  public void publishMessage(
      String action, Promotion promotion, List<PromoMsgLbConfigDto> messageDtoList) {
    PromoMessageDto promoMessageDto = new PromoMessageDto();
    promoMessageDto.setAction(action);
    promoMessageDto.setPromotionId(promotion.getId());
    promoMessageDto.setBrand(promotion.getBrand());
    promoMessageDto.setPromoLbConfigs(messageDtoList);
    if (!action.equals(PromoLbKafkaAction.DELETE.getValue())) {
      promoMessageDto.setStartDate(promotion.getValidityPeriodStart());
      promoMessageDto.setEndDate(promotion.getValidityPeriodEnd());
    }
    publishMessageToKafka(promotion, promoMessageDto);
  }

  private void publishMessageToKafka(Promotion promotion, PromoMessageDto promoMessageDto) {
    log.debug(
        "Publishing message to Kafka topic: {} for promotionId: {}",
        getTopicByBrand(promotion.getBrand()),
        promotion.getId());
    getKafkaTemplateByBrand(promotion.getBrand())
        .send(getTopicByBrand(promotion.getBrand()), promoMessageDto)
        .addCallback(
            new ListenableFutureCallback<SendResult<String, PromoMessageDto>>() {
              @Override
              public void onSuccess(SendResult<String, PromoMessageDto> result) {
                log.info(
                    "Leaderboard message publish successfully: {} , in topic: {}",
                    promoMessageDto,
                    getTopicByBrand(promotion.getBrand()));
              }

              @Override
              public void onFailure(Throwable ex) {
                log.error(
                    "Error while publishing Leaderboard kafka message: {},error: {}, in topic: {}",
                    promoMessageDto,
                    ex.getMessage(),
                    getTopicByBrand(promotion.getBrand()));
              }
            });
  }

  private String getTopicByBrand(String brand) {
    return brand.equalsIgnoreCase(Brand.BMA) ? leaderboardPromoCoralTopic : leaderboardPromoTopic;
  }

  private KafkaTemplate<String, PromoMessageDto> getKafkaTemplateByBrand(String brand) {
    return brand.equalsIgnoreCase(Brand.BMA)
        ? promoLeaderboardCoralKafkaTemplate
        : promoLeaderboardKafkaTemplate;
  }
}
