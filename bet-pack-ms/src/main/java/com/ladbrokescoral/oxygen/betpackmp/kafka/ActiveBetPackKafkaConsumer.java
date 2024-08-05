package com.ladbrokescoral.oxygen.betpackmp.kafka;

import static com.ladbrokescoral.oxygen.betpackmp.constants.BetPackConstants.ACTIVE_BET_PACK_IDS;

import com.ladbrokescoral.oxygen.betpackmp.redis.ActiveBetPacks;
import com.ladbrokescoral.oxygen.betpackmp.redis.BetPackRedisService;
import java.util.List;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.util.CollectionUtils;

/** Has to consume active bet pack ids from cms and store it in redis */
@Configuration
public class ActiveBetPackKafkaConsumer {

  private final BetPackRedisService betPackRedisService;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  public ActiveBetPackKafkaConsumer(BetPackRedisService betPackRedisService) {
    this.betPackRedisService = betPackRedisService;
  }

  @KafkaListener(
      topics = "${topic.active-bet-packs}",
      containerFactory = "internalCmsActiveBetPacksKafkaFactory")
  public void consume(ConsumerRecord<String, List<String>> consumerRecord) {
    if (null != consumerRecord.value()) {
      List<String> savedActiveBetPackIds =
          betPackRedisService.getActiveBetPacks(ACTIVE_BET_PACK_IDS).getActiveBetPacksIds();
      List<String> activeBetPackIds = consumerRecord.value();
      if (!CollectionUtils.isEmpty(savedActiveBetPackIds)
          && !CollectionUtils.isEmpty(activeBetPackIds)
          && !(savedActiveBetPackIds.size() == activeBetPackIds.size()
              && savedActiveBetPackIds.containsAll(activeBetPackIds))) {
        ActiveBetPacks activeBetPacks = new ActiveBetPacks(activeBetPackIds);
        betPackRedisService.put(activeBetPacks);
      } else {
        ASYNC_LOGGER.info("ActiveBetPackKafkaConsumer :: received null or empty bet pack ids");
      }
    }
  }
}
