package com.ladbrokescoral.oxygen.betpackmp.scheduler;

import static com.ladbrokescoral.oxygen.betpackmp.constants.BetPackConstants.ACTIVE_BET_PACK_IDS;

import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetOffer;
import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import com.ladbrokescoral.oxygen.betpackmp.constants.BetPackConstants;
import com.ladbrokescoral.oxygen.betpackmp.kafka.KafkaBetPacksPublisher;
import com.ladbrokescoral.oxygen.betpackmp.redis.BetPackRedisService;
import com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack.BetPackLastMessageCache;
import com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack.BetPackMessage;
import com.ladbrokescoral.oxygen.betpackmp.util.DateUtils;
import java.util.List;
import java.util.Objects;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

@Component
public class BetPackScheduler {

  private final BetPackLastMessageCache betPackLastMessageCache;
  private final KafkaBetPacksPublisher kafkaBetPackPublisher;
  private final BetPackRedisService betPackRedisService;
  private final MasterSlaveExecutor masterSlaveExecutor;

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  public BetPackScheduler(
      BetPackLastMessageCache betPackLastMessageCache,
      KafkaBetPacksPublisher kafkaBetPackPublisher,
      BetPackRedisService betPackRedisService,
      MasterSlaveExecutor masterSlaveExecutor) {
    this.betPackLastMessageCache = betPackLastMessageCache;
    this.kafkaBetPackPublisher = kafkaBetPackPublisher;
    this.betPackRedisService = betPackRedisService;
    this.masterSlaveExecutor = masterSlaveExecutor;
  }

  @Scheduled(cron = "${bet-pack.cron.expression}")
  public void scheduleTaskUsingCronExpression() {
    masterSlaveExecutor.executeIfMaster(
        () -> {
          List<BetPackMessage> betPackMessages =
              (List)
                  betPackLastMessageCache.findAllById(
                      betPackRedisService
                          .getActiveBetPacks(ACTIVE_BET_PACK_IDS)
                          .getActiveBetPacksIds());
          if (!CollectionUtils.isEmpty(betPackMessages)) {
            for (BetPackMessage betPackMessage : betPackMessages) {
              FreebetOffer freebetOffer = betPackMessage.getMessage();
              if (Objects.nonNull(freebetOffer)) {
                Long d = DateUtils.minDiff(freebetOffer.getEndTime());
                ASYNC_LOGGER.info(
                    "BetPackScheduler offer {} with {} min {}:",
                    freebetOffer.getFreebetOfferId(),
                    d,
                    freebetOffer.getEndTime());
                processEligibleBetPacks(freebetOffer, d);
              }
            }
          }
        },
        () -> ASYNC_LOGGER.info("SLAVE"));
  }

  private void processEligibleBetPacks(FreebetOffer freebetOffer, Long d) {
    if (d <= BetPackConstants.ONE_EIGHTY) {
      kafkaBetPackPublisher.publish(freebetOffer.getFreebetOfferId(), freebetOffer);
      ASYNC_LOGGER.info("publishing {} as under {} min :", freebetOffer.getFreebetOfferId(), d);
    }
  }
}
