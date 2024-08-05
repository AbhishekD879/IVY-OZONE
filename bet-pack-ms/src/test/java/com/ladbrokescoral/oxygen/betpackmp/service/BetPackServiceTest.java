package com.ladbrokescoral.oxygen.betpackmp.service;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetGetOffersResponse;
import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetGetOffersResponseModel;
import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetGetOffersResult;
import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetOffer;
import com.ladbrokescoral.oxygen.betpackmp.kafka.KafkaBetPacksPublisher;
import com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack.BetPackRedisOperations;
import java.util.Arrays;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import reactor.core.publisher.Mono;

@ExtendWith(MockitoExtension.class)
class BetPackServiceTest implements WithAssertions {

  @Mock private BppService bppService;

  @Mock private KafkaBetPacksPublisher kafkaBetPackPublisher;

  @Mock private BetPackRedisOperations betPackRedisOperations;

  @InjectMocks private BetPackService betPackService;

  private final String betPackId = "798798";

  @Test
  void processBetPacksSuccess() {
    FreebetGetOffersResponse responseMono = new FreebetGetOffersResponse();
    responseMono.setResponse(new FreebetGetOffersResult());
    responseMono.getResult().setRespFreebetGetOffers(new FreebetGetOffersResponseModel());
    FreebetOffer offer = new FreebetOffer();
    offer.setFreebetOfferId("7878");
    offer.setDescription("description");
    responseMono.getResult().getRespFreebetGetOffers().setFreebetOffer(Arrays.asList(offer));
    when(bppService.freeBetGetOffers(betPackId)).thenReturn(Mono.just(responseMono));
    doNothing().when(betPackRedisOperations).saveLastMessage(any());
    betPackService.processBetPacks(betPackId);
    verify(bppService, times(1)).freeBetGetOffers(betPackId);
    assertNotNull(responseMono.getResult());
    assertNotNull(responseMono.getResult().getRespFreebetGetOffers());
  }

  @Test
  void processBetPacksFailure() {
    FreebetGetOffersResponse responseMono = new FreebetGetOffersResponse();
    when(bppService.freeBetGetOffers(betPackId)).thenReturn(Mono.just(responseMono));
    betPackService.processBetPacks(betPackId);
    verify(bppService, times(1)).freeBetGetOffers(betPackId);
    assertNull(responseMono.getResult());
  }

  @Test
  void processBetPacksFailureTest() {
    when(bppService.freeBetGetOffers(betPackId)).thenReturn(Mono.empty());
    Assertions.assertDoesNotThrow(() -> betPackService.processBetPacks(betPackId));
    verify(bppService, times(1)).freeBetGetOffers(betPackId);
  }

  @Test
  void processBetPacksFailure_2() {
    FreebetGetOffersResponse responseMono = new FreebetGetOffersResponse();
    responseMono.setResponse(new FreebetGetOffersResult());
    when(bppService.freeBetGetOffers(betPackId)).thenReturn(Mono.just(responseMono));
    betPackService.processBetPacks(betPackId);
    verify(bppService, times(1)).freeBetGetOffers(betPackId);
    assertNotNull(responseMono.getResult());
  }

  @Test
  void processBetPacksFailure_3() {
    FreebetGetOffersResponse responseMono = new FreebetGetOffersResponse();
    responseMono.setResponse(new FreebetGetOffersResult());
    responseMono.getResult().setRespFreebetGetOffers(new FreebetGetOffersResponseModel());
    when(bppService.freeBetGetOffers(betPackId)).thenReturn(Mono.just(responseMono));
    betPackService.processBetPacks(betPackId);
    verify(bppService, times(1)).freeBetGetOffers(betPackId);
    assertNotNull(responseMono.getResult().getRespFreebetGetOffers());
  }

  @Test
  void processBetPacksFailure_4() {
    FreebetOffer freeBetOffers = null;
    FreebetGetOffersResponse responseMono = new FreebetGetOffersResponse();
    responseMono.setResponse(new FreebetGetOffersResult());
    responseMono.getResult().setRespFreebetGetOffers(new FreebetGetOffersResponseModel());
    responseMono
        .getResult()
        .getRespFreebetGetOffers()
        .setFreebetOffer(Arrays.asList(freeBetOffers));
    when(bppService.freeBetGetOffers(betPackId)).thenReturn(Mono.just(responseMono));
    betPackService.processBetPacks(betPackId);
    verify(bppService, times(1)).freeBetGetOffers(betPackId);
    assertNotNull(responseMono.getResult().getRespFreebetGetOffers().getFreebetOffer());
  }

  @Test
  void publishMessageTest() {
    FreebetOffer freebetOffer = new FreebetOffer();
    freebetOffer.setFreebetOfferId("7675");
    Assertions.assertDoesNotThrow(() -> betPackService.publishMessage(freebetOffer));
  }

  @Test
  void processBetPacksDoOnError() {
    when(bppService.freeBetGetOffers(betPackId)).thenReturn(Mono.error(Exception::new));
    verify(bppService, times(0)).freeBetGetOffers(betPackId);
    Assertions.assertDoesNotThrow(() -> betPackService.processBetPacks(betPackId));
  }
}
