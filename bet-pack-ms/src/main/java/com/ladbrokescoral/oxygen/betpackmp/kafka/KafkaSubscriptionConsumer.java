package com.ladbrokescoral.oxygen.betpackmp.kafka;

import com.ladbrokescoral.oxygen.betpackmp.exception.BetPackMarketPlaceException;
import com.ladbrokescoral.oxygen.betpackmp.service.BetPackService;
import org.apache.commons.lang.StringUtils;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.KafkaListener;

/*
 This class is responsible to receive bet pack subscription messages
*/
@Configuration
public class KafkaSubscriptionConsumer {

  private final BetPackService betPackService;

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Autowired
  public KafkaSubscriptionConsumer(BetPackService betPackService) {
    this.betPackService = betPackService;
  }

  @KafkaListener(
      topics = "${topic.bet-pack-subscription}",
      containerFactory = "internalBetPackKafkaFactory")
  public void consume(ConsumerRecord<String, String> consumerRecord) {
    try {
      String betPackId = consumerRecord.key();
      ASYNC_LOGGER.trace("Subscribe on bet pack : {} and cache subscription", betPackId);
      if (StringUtils.isNotBlank(betPackId)) {
        betPackService.processBetPacks(consumerRecord.key());
      }
    } catch (Exception ex) {
      ASYNC_LOGGER.error("Caught error while processing subscription {}", consumerRecord.key(), ex);
      throw new BetPackMarketPlaceException("Caught error while processing subscription ");
    }
  }
}
