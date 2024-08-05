package com.ladbrokescoral.oxygen.betpackmp.service;

import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetGetOffersResponse;
import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetGetOffersResponseModel;
import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetGetOffersResult;
import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetOffer;
import com.ladbrokescoral.oxygen.betpackmp.kafka.KafkaBetPacksPublisher;
import com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack.BetPackMessage;
import com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack.BetPackRedisOperations;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

/*
  This class is responsible for calling bpp for offer details and publishing messages to live updates topic
*/

@Service
public class BetPackService {

  private final BppService bppService;
  private final KafkaBetPacksPublisher kafkaBetPackPublisher;
  private final BetPackRedisOperations betPackRedisOperations;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  protected BetPackService(
      BppService bppService,
      KafkaBetPacksPublisher kafkaBetPackPublisher,
      BetPackRedisOperations betPackRedisOperations) {
    this.bppService = bppService;
    this.kafkaBetPackPublisher = kafkaBetPackPublisher;
    this.betPackRedisOperations = betPackRedisOperations;
  }

  public void processBetPacks(String betPackId) {

    bppService
        .freeBetGetOffers(betPackId)
        .doOnSuccess(
            (FreebetGetOffersResponse freeBetGetOffersResponse) -> {
              if (isValidResponse(freeBetGetOffersResponse)) {
                FreebetOffer freebetOffer =
                    freeBetGetOffersResponse
                        .getResult()
                        .getRespFreebetGetOffers()
                        .getFreebetOffer()
                        .get(0);
                kafkaBetPackPublisher.publish(betPackId, freebetOffer);
                betPackRedisOperations.saveLastMessage(new BetPackMessage(betPackId, freebetOffer));
              }
            })
        .doOnError(
            ex ->
                ASYNC_LOGGER.error(
                    "Error on free bet get offers request with exception  [{}]", ex.getMessage()))
        .subscribe();
  }

  private boolean isValidResponse(FreebetGetOffersResponse freeBetGetOffersResponse) {

    if (isResulted(freeBetGetOffersResponse)) {
      FreebetGetOffersResult freebetGetOffersResult = freeBetGetOffersResponse.getResult();
      FreebetGetOffersResponseModel freebetGetOffersResponseModel =
          freebetGetOffersResult.getRespFreebetGetOffers();
      return null != freebetGetOffersResponseModel
          && !CollectionUtils.isEmpty(freebetGetOffersResponseModel.getFreebetOffer())
          && null != freebetGetOffersResponseModel.getFreebetOffer().get(0);
    }
    return false;
  }

  private boolean isResulted(FreebetGetOffersResponse freeBetGetOffersResponse) {
    return null != freeBetGetOffersResponse && null != freeBetGetOffersResponse.getResult();
  }

  public void publishMessage(FreebetOffer freebetOffer) {
    kafkaBetPackPublisher.publish(freebetOffer.getFreebetOfferId(), freebetOffer);
  }
}
