package com.ladbrokescoral.oxygen.betpackmp.service;

import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetGetOffersResponse;
import reactor.core.publisher.Mono;

public interface BppService {
  Mono<FreebetGetOffersResponse> freeBetGetOffers(String freeBetOfferId);
}
