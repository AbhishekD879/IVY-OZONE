package com.ladbrokescoral.oxygen.betpackmp.service;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.when;

import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetGetOffersResponse;
import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetGetOffersResult;
import com.coral.bpp.api.service.BppApiAsync;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import reactor.core.publisher.Mono;

@ExtendWith(MockitoExtension.class)
class BppServiceImplTest implements WithAssertions {

  @Mock private BppApiAsync bppApiAsync;

  @InjectMocks private BppServiceImpl bppServiceImpl;

  private final String freeBetOfferId = "576576576";

  @BeforeEach
  public void init() {
    bppServiceImpl = new BppServiceImpl(bppApiAsync);
  }

  @Test
  void freeBetGetOffersTest() {
    FreebetGetOffersResponse response = new FreebetGetOffersResponse();
    response.setResponse(new FreebetGetOffersResult());
    when(bppApiAsync.freebetGetOffers(freeBetOfferId, "Y", "Y", "PURCHASE"))
        .thenReturn(Mono.just(response));
    Mono<FreebetGetOffersResponse> responseMono = bppServiceImpl.freeBetGetOffers(freeBetOfferId);
    assertNotNull(responseMono);
  }
}
