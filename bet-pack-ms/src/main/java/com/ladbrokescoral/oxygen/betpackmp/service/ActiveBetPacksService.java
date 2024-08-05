package com.ladbrokescoral.oxygen.betpackmp.service;

import static com.ladbrokescoral.oxygen.betpackmp.util.DateUtils.scrub;

import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import com.ladbrokescoral.oxygen.betpackmp.redis.ActiveBetPacks;
import com.ladbrokescoral.oxygen.betpackmp.redis.BetPackRedisService;
import com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack.BetPackMessage;
import com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack.BetPackRedisOperations;
import java.util.List;
import java.util.Optional;
import javax.annotation.PostConstruct;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

/** To fetch the active bet pack ids form cms and get the offer data from bpp */
@Component
public class ActiveBetPacksService {

  private final BetPackRedisService betPackRedisRepoService;
  private final CmsService cmsService;
  private final BetPackService betPackService;
  private final BetPackRedisOperations betPackRedisOperations;
  private final MasterSlaveExecutor masterSlaveExecutor;

  @Value("${cms.brand}")
  private String cmsBand;

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  public ActiveBetPacksService(
      BetPackRedisService betPackRedisRepoService,
      CmsService cmsService,
      BetPackService betPackService,
      BetPackRedisOperations betPackRedisOperations,
      MasterSlaveExecutor masterSlaveExecutor) {
    this.betPackRedisRepoService = betPackRedisRepoService;
    this.cmsService = cmsService;
    this.betPackService = betPackService;
    this.betPackRedisOperations = betPackRedisOperations;
    this.masterSlaveExecutor = masterSlaveExecutor;
  }

  @PostConstruct
  public void loadActiveBetPacks() {
    masterSlaveExecutor.executeIfMaster(
        () -> {
          ASYNC_LOGGER.info("ActiveBetPacksService：loadActiveBetPacks");
          cmsService
              .getActiveBetPackIds(cmsBand)
              .doOnNext(
                  (List<String> activeBetPackIds) -> {
                    if (!CollectionUtils.isEmpty(activeBetPackIds)) {
                      ActiveBetPacks activeBetPacks = new ActiveBetPacks(activeBetPackIds);
                      ASYNC_LOGGER.info(
                          "ActiveBetPacksService: activeBetPackIds:{}",
                          scrub(activeBetPackIds.toString()));
                      betPackRedisRepoService.save(activeBetPacks);
                    }
                  })
              .doOnNext(
                  (List<String> activeBetPackIds) ->
                      activeBetPackIds.forEach(
                          (String activeBetPackId) -> {
                            ASYNC_LOGGER.info(
                                "ActiveBetPacksService : processing  activeBetPackId:{}",
                                scrub(activeBetPackId));
                            processBetPack(activeBetPackId);
                          }))
              .doOnError(
                  ex ->
                      ASYNC_LOGGER.error(
                          "Error on active bet pack ids request with exception  [{}]",
                          ex.getMessage()))
              .subscribe();
        },
        () -> ASYNC_LOGGER.info("SLAVE"));
  }

  private void processBetPack(String activeBetPackId) {
    Optional<BetPackMessage> message = betPackRedisOperations.getLastSavedMessage(activeBetPackId);
    if (message.isEmpty()) {
      betPackService.processBetPacks(activeBetPackId);
    }
  }
}
