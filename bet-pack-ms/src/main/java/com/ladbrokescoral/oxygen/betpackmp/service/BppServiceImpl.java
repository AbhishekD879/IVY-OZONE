package com.ladbrokescoral.oxygen.betpackmp.service;

import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetGetOffersResponse;
import com.coral.bpp.api.service.BppApiAsync;
import com.google.gson.Gson;
import java.util.Objects;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

/*
 This class is for processing bpp calls
*/
@Service
public class BppServiceImpl implements BppService {

  private final BppApiAsync bppApiAsync;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  public BppServiceImpl(BppApiAsync bppApiAsync) {
    this.bppApiAsync = bppApiAsync;
  }

  @Override
  public Mono<FreebetGetOffersResponse> freeBetGetOffers(String freeBetOfferId) {
    ASYNC_LOGGER.info("BppServiceImpl::bpp freeBetGetOffers::{}", freeBetOfferId);
    return bppApiAsync
        .freebetGetOffers(freeBetOfferId, "Y", "Y", "PURCHASE")
        .filter(Objects::nonNull)
        .doOnNext(
            e ->
                ASYNC_LOGGER.info(
                    "freebetGetOffers freeBetOfferId {} , response : {}",
                    freeBetOfferId,
                    new Gson().toJson(e)));
  }
}
