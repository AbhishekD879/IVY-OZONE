package com.ladbrokescoral.oxygen.betpackmp.kafka.filter;

import static com.ladbrokescoral.oxygen.betpackmp.constants.BetPackConstants.ACTIVE_BET_PACK_IDS;
import static com.ladbrokescoral.oxygen.betpackmp.util.DateUtils.scrub;
import static com.ladbrokescoral.oxygen.betpackmp.validator.BetPackValidator.validateActiveBetPack;

import com.ladbrokescoral.oxygen.betpackmp.model.PafExtractorPromotion;
import com.ladbrokescoral.oxygen.betpackmp.model.Promotion;
import com.ladbrokescoral.oxygen.betpackmp.redis.ActiveBetPacks;
import com.ladbrokescoral.oxygen.betpackmp.redis.BetPackRedisService;
import com.ladbrokescoral.oxygen.betpackmp.redis.PafBetPack;
import com.ladbrokescoral.oxygen.betpackmp.redis.PafBetPackRepository;
import com.ladbrokescoral.oxygen.betpackmp.service.CmsService;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.atomic.AtomicReference;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.listener.adapter.RecordFilterStrategy;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

/*
 * To filter df kafka messages
 */
@Component
public class BetPackDFPafKafkaConsumerFilter
    implements RecordFilterStrategy<String, PafExtractorPromotion> {

  private final BetPackRedisService betPackRedisRepoService;
  private final CmsService cmsService;
  private final PafBetPackRepository pafBetPackRepository;

  @Value("${df.brand}")
  private String dfBrand;

  @Value("${cms.brand}")
  private String cmsBand;

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  public BetPackDFPafKafkaConsumerFilter(
      CmsService cmsService,
      BetPackRedisService betPackRedisRepoService,
      PafBetPackRepository pafBetPackRepository) {
    this.pafBetPackRepository = pafBetPackRepository;
    this.cmsService = cmsService;
    this.betPackRedisRepoService = betPackRedisRepoService;
  }

  @Override
  public boolean filter(ConsumerRecord<String, PafExtractorPromotion> rec) {
    PafExtractorPromotion pafExtractorPromotion = rec.value();
    AtomicReference<ActiveBetPacks> activeBetPacks =
        new AtomicReference<>(betPackRedisRepoService.getActiveBetPacks(ACTIVE_BET_PACK_IDS));
    if ((Objects.nonNull(activeBetPacks.get())
            && CollectionUtils.isEmpty(activeBetPacks.get().getActiveBetPacksIds()))
        || Objects.isNull(activeBetPacks.get())) {
      cmsService
          .getActiveBetPackIds(cmsBand)
          .doOnNext(
              (List<String> activeBetPackIds) -> {
                if (!CollectionUtils.isEmpty(activeBetPackIds)) {
                  activeBetPacks.set(new ActiveBetPacks(activeBetPackIds));
                  ASYNC_LOGGER.info(
                      ">>> BetPackDFPafKafkaConsumerFilter : activeBetPackIds:{}",
                      scrub(activeBetPackIds.toString()));
                  betPackRedisRepoService.save(activeBetPacks.get());
                }
              })
          .doOnError(
              ex ->
                  ASYNC_LOGGER.error(
                      "Error on cms get active pack ids request with exception  [{}]",
                      ex.getMessage()))
          .filter(
              activeBetPackIds ->
                  validateActiveBetPack(pafExtractorPromotion, activeBetPackIds, dfBrand))
          .subscribe();
    }
    boolean isValid =
        validateActiveBetPack(
            pafExtractorPromotion, activeBetPacks.get().getActiveBetPacksIds(), dfBrand);
    ASYNC_LOGGER.info(
        ">>> BetPackDFPafKafkaConsumerFilter : filter :{} and {}",
        pafExtractorPromotion.getPayload().getCampaignRef(),
        isValid);
    if (isValid) {
      Promotion promotion = pafExtractorPromotion.getPayload();
      String id =
          promotion.getCampaignRef() + promotion.getCustomerRef() + promotion.getClaimedDate();
      if (pafBetPackRepository.findById(id).isEmpty()) {
        PafBetPack pafBetPack = new PafBetPack();
        pafBetPack.setId(id);
        pafBetPackRepository.save(pafBetPack);
        ASYNC_LOGGER.info(
            ">>> BetPackDFPafKafkaConsumerFilter : filter :{} first time {}",
            pafExtractorPromotion.getPayload().getCampaignRef(),
            false);
        return false;
      } else {
        ASYNC_LOGGER.info(
            ">>> BetPackDFPafKafkaConsumerFilter : filter :{} 2nd time onwards {}",
            pafExtractorPromotion.getPayload().getCampaignRef(),
            true);
        return true;
      }
    }
    ASYNC_LOGGER.info(
        ">>> BetPackDFPafKafkaConsumerFilter : filter :{} not valid {}",
        pafExtractorPromotion.getPayload().getCampaignRef(),
        true);
    return true;
  }
}
