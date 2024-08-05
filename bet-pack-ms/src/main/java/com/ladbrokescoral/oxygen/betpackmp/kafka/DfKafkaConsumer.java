package com.ladbrokescoral.oxygen.betpackmp.kafka;

import com.ladbrokescoral.oxygen.betpackmp.model.PafExtractorPromotion;
import com.ladbrokescoral.oxygen.betpackmp.service.BetPackService;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

/*
  receive df promotional message and process the message
*/

@Component
public class DfKafkaConsumer {

  private final BetPackService betPackService;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  public DfKafkaConsumer(BetPackService betPackService) {
    this.betPackService = betPackService;
  }

  @KafkaListener(
      topics = "${df.paf.topic.name}",
      containerFactory = "filteredKafkaPafContainerFactory")
  public void consumePAFeed(ConsumerRecord<String, PafExtractorPromotion> promotionConsumerRecord) {
    PafExtractorPromotion extractorPromotionEvent = promotionConsumerRecord.value();
    ASYNC_LOGGER.info(
        "df-reward-streamer-paf key: {}, value:{} ",
        promotionConsumerRecord.key(),
        extractorPromotionEvent);
    betPackService.processBetPacks(extractorPromotionEvent.getPayload().getCampaignRef());
  }
}
