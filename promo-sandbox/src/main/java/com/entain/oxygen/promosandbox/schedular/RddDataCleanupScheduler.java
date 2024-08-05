package com.entain.oxygen.promosandbox.schedular;

import com.entain.oxygen.promosandbox.model.PromoConfig;
import com.entain.oxygen.promosandbox.service.CacheManagerService;
import com.entain.oxygen.promosandbox.service.HouseKeepingService;
import com.entain.oxygen.promosandbox.service.PromoConfigService;
import com.entain.oxygen.promosandbox.utils.PromoLbUtil;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class RddDataCleanupScheduler {

  private final PromoConfigService promoConfigService;

  private final HouseKeepingService houseKeepingService;

  private final CacheManagerService cacheManagerService;

  @Value("${cms.brand}")
  private String brand;

  @Value(("${update.promo.config.delay.scheduler}"))
  private long updateSchedulerTime;

  public static final long THOUSAND = 1000;

  @Autowired
  public RddDataCleanupScheduler(
      PromoConfigService promoConfigService,
      HouseKeepingService houseKeepingService,
      CacheManagerService cacheManagerService) {
    this.promoConfigService = promoConfigService;
    this.houseKeepingService = houseKeepingService;
    this.cacheManagerService = cacheManagerService;
  }

  @Scheduled(cron = "${dataCleanup.scheduler.cron}", zone = "${time.zone}")
  public void dataCleanupJob() {
    try {
      cacheManagerService.clearCache();
      List<PromoConfig> promotions =
          promoConfigService.findAllByBrandAndDataCleanupStatus(brand, false);
      if (!promotions.isEmpty()) {
        log.debug("Total No of promotion fetch from mongoDB : {} ", promotions.size());
        List<PromoConfig> expirePromotions =
            promotions.stream()
                .filter(
                    promoConfig ->
                        promoConfig.getEndDate().getEpochSecond() < Instant.now().getEpochSecond())
                .collect(Collectors.toList());
        log.info(
            "Eligible promotions for data cleanup : {} ",
            expirePromotions.stream()
                .map(PromoConfig::getPromotionId)
                .collect(Collectors.toList()));
        Map<String, Boolean> promoLbConfigMap = new HashMap<>();
        expirePromotions.forEach(
            (PromoConfig promoConfig) -> {
              boolean status =
                  houseKeepingService.dropSparkTempTable(
                      promoConfig.getPromotionId(), promoConfig.getLeaderboardId());
              promoLbConfigMap.put(
                  PromoLbUtil.computePrimaryKey(
                      promoConfig.getPromotionId(), promoConfig.getLeaderboardId()),
                  status);
            });
        registeredPromoUpdateDelayScheduler(promoLbConfigMap);
      } else {
        log.info("No promotions Eligible for data cleanup");
      }
    } catch (Exception ex) {
      log.error("error in RddDataCleanupScheduler : {}", ex.getMessage());
    }
  }

  private void registeredPromoUpdateDelayScheduler(Map<String, Boolean> promoLbConfigMap) {
    Timer timer = new Timer();
    TimerTask promoUpdateDelayScheduler =
        new TimerTask() {
          @Override
          public void run() {
            promoLbConfigMap.forEach(promoConfigService::updatePromoIsDataCleanupStatus);
          }
        };
    timer.schedule(promoUpdateDelayScheduler, updateSchedulerTime * THOUSAND); // MILLISECONDS
  }
}
