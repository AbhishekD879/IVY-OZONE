package com.ladbrokescoral.cashout.service.updates;

import static org.assertj.core.api.Assertions.assertThat;
import static org.awaitility.Awaitility.await;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.argThat;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.after;
import static org.mockito.Mockito.inOrder;
import static org.mockito.Mockito.timeout;

import com.ladbrokescoral.cashout.api.client.RemoteCashoutApi;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutBet;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutLeg;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutOfferRequest;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutPart;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutPrice;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest.CashoutRequestBuilder;
import com.ladbrokescoral.cashout.api.client.entity.response.CashoutOffer;
import com.ladbrokescoral.cashout.config.CashoutOfferBufferingProperties;
import com.ladbrokescoral.cashout.model.response.CashoutData;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import java.io.IOException;
import java.net.SocketTimeoutException;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.assertj.core.data.Index;
import org.junit.Ignore;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.mockito.InOrder;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import reactor.core.publisher.Flux;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class AsyncCashoutOfferServiceImplTest {

  private AsyncCashoutOfferService service;
  private BetUpdatesTopic betUpdatesTopic;
  private RemoteCashoutApi remoteCashoutApi;
  private Function<CashoutOffer, UpdateDto> offerToBetUpdate;

  @Captor ArgumentCaptor<String> keyCaptor;

  @Captor ArgumentCaptor<UpdateDto> updateCaptor;

  private static void updateHasActivation(UpdateDto updateDto) {
    assertEquals(Boolean.TRUE, updateDto.getCashoutData().getShouldActivate());
  }

  @BeforeEach
  public void setUp() throws Exception {
    remoteCashoutApi = Mockito.mock(RemoteCashoutApi.class);
    // mockCashoutApi();
    offerToBetUpdate =
        offer -> UpdateDto.builder().cashoutData(CashoutData.builder().build()).build();
    this.betUpdatesTopic = Mockito.mock(BetUpdatesTopic.class);
    CashoutOfferBufferingProperties props = new CashoutOfferBufferingProperties();
    props.setWindowTime(Duration.ofMillis(100));
    props.setMaxSize(5);
    props.setMaxTime(Duration.ofMillis(100));
    this.service =
        new AsyncCashoutOfferServiceImpl(
            props, remoteCashoutApi, offerToBetUpdate, betUpdatesTopic, 1, "BUFFER");
  }

  @Test
  void cashoutUpdateIsSent() {
    CashoutRequest cashoutReq =
        CashoutRequest.builder()
            .cashoutOfferRequests(Collections.singletonList(createCashoutOffer("123", "SGL")))
            .build();
    Mockito.when(remoteCashoutApi.getCashoutOffers(any()))
        .thenReturn(Flux.just(CashoutOffer.builder().cashoutOfferReqRef("123").build()));

    service.acceptCashoutOfferRequest(cashoutReq);

    Mockito.verify(betUpdatesTopic, Mockito.timeout(1_000)).sendBetUpdate(eq("123"), any());
  }

  @Test
  void twoActivationRequestsMerged() {
    mockCashoutApi();
    CashoutRequest cashoutReq =
        CashoutRequest.builder()
            .cashoutOfferRequests(Collections.singletonList(createCashoutOffer("123", "SGL")))
            .shouldActivate(true)
            .build();

    CashoutRequest cashoutReq2 =
        CashoutRequest.builder()
            .cashoutOfferRequests(Collections.singletonList(createCashoutOffer("321", "SGL")))
            .shouldActivate(true)
            .build();

    service.acceptCashoutOfferRequest(cashoutReq);
    service.acceptCashoutOfferRequest(cashoutReq2);

    Mockito.verify(betUpdatesTopic, Mockito.timeout(1_000).times(2))
        .sendBetUpdate(keyCaptor.capture(), updateCaptor.capture());

    assertThat(keyCaptor.getAllValues()).containsExactly("123", "321");
    assertThat(updateCaptor.getAllValues())
        .allSatisfy(AsyncCashoutOfferServiceImplTest::updateHasActivation);
  }

  // @Test
  void theMoreThen256WhenCashoutApiHasDelay() {
    CashoutOfferBufferingProperties props = new CashoutOfferBufferingProperties();
    props.setWindowTime(Duration.ofMillis(100));
    props.setMaxSize(1);
    props.setMaxTime(Duration.ofMinutes(5));

    Mockito.when(remoteCashoutApi.getCashoutOffers(any()))
        .thenReturn(
            Flux.defer(
                () ->
                    Flux.just(CashoutOffer.builder().build())
                        .delaySequence(Duration.ofSeconds(1))));

    AsyncCashoutOfferServiceImpl service =
        new AsyncCashoutOfferServiceImpl(
            props, remoteCashoutApi, offerToBetUpdate, betUpdatesTopic, 1, "BUFFER");

    sendFewCashoutRequests(service, 500);

    Mockito.verify(remoteCashoutApi, timeout(500).times(500)).getCashoutOffers(any());
  }

  @Test
  void whenMultipleBetSelectionsAreUpdatedFrequentlyWithinNTimeFrameThenOnlyOneIsSent() {
    mockCashoutApi();
    CashoutOfferBufferingProperties props = new CashoutOfferBufferingProperties();
    props.setWindowTime(Duration.ofMillis(100));
    props.setMaxSize(1);
    props.setMaxTime(Duration.ofMinutes(5));

    BiFunction<String, String, CashoutLeg> leg =
        (a, b) ->
            CashoutLeg.builder()
                .part(
                    CashoutPart.builder()
                        .spotPrice(CashoutPrice.builder().num(a).den(b).build())
                        .build())
                .build();

    CashoutRequest req1 =
        CashoutRequest.builder()
            .cashoutOfferRequests(
                Collections.singletonList(
                    CashoutOfferRequest.builder()
                        .cashoutOfferReqRef("123")
                        .bet(
                            CashoutBet.builder()
                                .betType("TBL")
                                .leg(leg.apply("10", "10"))
                                .leg(leg.apply("2", "2"))
                                .leg(leg.apply("3", "3"))
                                .build())
                        .build()))
            .build();

    CashoutRequest req2 =
        CashoutRequest.builder()
            .cashoutOfferRequests(
                Collections.singletonList(
                    CashoutOfferRequest.builder()
                        .cashoutOfferReqRef("123")
                        .bet(
                            CashoutBet.builder()
                                .betType("TBL")
                                .leg(leg.apply("10", "10"))
                                .leg(leg.apply("20", "20"))
                                .leg(leg.apply("3", "3"))
                                .build())
                        .build()))
            .build();

    CashoutRequest req3 =
        CashoutRequest.builder()
            .cashoutOfferRequests(
                Collections.singletonList(
                    CashoutOfferRequest.builder()
                        .cashoutOfferReqRef("123")
                        .bet(
                            CashoutBet.builder()
                                .betType("TBL")
                                .leg(leg.apply("10", "10"))
                                .leg(leg.apply("20", "20"))
                                .leg(leg.apply("30", "30"))
                                .build())
                        .build()))
            .build();

    service.acceptCashoutOfferRequest(req1);
    service.acceptCashoutOfferRequest(req2);
    service.acceptCashoutOfferRequest(req3);

    Mockito.verify(remoteCashoutApi, timeout(500).times(1))
        .getCashoutOffers(
            argThat(
                req -> {
                  if (req.getCashoutOfferRequests().size() > 1) {
                    return false;
                  }

                  CashoutOfferRequest offerRequest = req.getCashoutOfferRequests().get(0);
                  List<CashoutPrice> prices =
                      offerRequest.getBet().getLegs().stream()
                          .flatMap(l -> l.getParts().stream())
                          .map(CashoutPart::getSpotPrice)
                          .collect(Collectors.toList());
                  return prices.size() == 3
                      && prices.get(0).getNum().equals("10")
                      && prices.get(0).getDen().equals("10")
                      && prices.get(1).getNum().equals("20")
                      && prices.get(1).getDen().equals("20")
                      && prices.get(2).getNum().equals("30")
                      && prices.get(2).getDen().equals("30");
                }));
  }

  @Test
  void cashoutOfferUpdatesAreSentInTheSameOrderTheyWereReceieved() {
    mockCashoutApi();
    sendFewCashoutRequests(service, 5);

    InOrder inOrder = inOrder(betUpdatesTopic);
    inOrder
        .verify(betUpdatesTopic, Mockito.timeout(500))
        .sendBetUpdate(eq("0"), any(UpdateDto.class));
    inOrder
        .verify(betUpdatesTopic, Mockito.timeout(500))
        .sendBetUpdate(eq("1"), any(UpdateDto.class));
    inOrder
        .verify(betUpdatesTopic, Mockito.timeout(500))
        .sendBetUpdate(eq("2"), any(UpdateDto.class));
    inOrder
        .verify(betUpdatesTopic, Mockito.timeout(500))
        .sendBetUpdate(eq("3"), any(UpdateDto.class));
    inOrder
        .verify(betUpdatesTopic, Mockito.timeout(500))
        .sendBetUpdate(eq("4"), any(UpdateDto.class));
  }

  @Test
  void whenAtLeastOneCashoutOfferRequestContainsActivationThenWholeGroupIsActivation() {
    mockCashoutApi();
    for (int i = 1; i <= 5; i++) {
      CashoutRequestBuilder builder =
          CashoutRequest.builder()
              .cashoutOfferRequests(
                  Collections.singletonList(
                      createCashoutOffer("123", "SGL", String.valueOf(i), "2")));
      if (i == 3) {
        builder.shouldActivate(true);
      }
      service.acceptCashoutOfferRequest(builder.build());
    }

    Mockito.verify(betUpdatesTopic, timeout(500))
        .sendBetUpdate(keyCaptor.capture(), updateCaptor.capture());

    assertThat(updateCaptor.getAllValues().size()).isEqualTo(1);
    assertThat(updateCaptor.getValue())
        .satisfies(AsyncCashoutOfferServiceImplTest::updateHasActivation);
  }

  @Test
  void cashoutOfferWithActivationAreNotMerged() {
    mockCashoutApi();
    service.acceptCashoutOfferRequest(
        CashoutRequest.builder()
            .cashoutOfferRequests(Collections.singletonList(createCashoutOffer("1", "SGL")))
            .shouldActivate(true)
            .build());

    service.acceptCashoutOfferRequest(
        CashoutRequest.builder()
            .cashoutOfferRequests(Collections.singletonList(createCashoutOffer("2", "SGL")))
            .build());

    service.acceptCashoutOfferRequest(
        CashoutRequest.builder()
            .cashoutOfferRequests(Collections.singletonList(createCashoutOffer("3", "SGL")))
            .build());

    Mockito.verify(remoteCashoutApi, timeout(500).times(2)).getCashoutOffers(any());

    Mockito.verify(betUpdatesTopic, timeout(500).times(3))
        .sendBetUpdate(keyCaptor.capture(), updateCaptor.capture());

    assertThat(keyCaptor.getAllValues()).containsExactly("1", "2", "3");
    assertThat(updateCaptor.getAllValues()).hasSize(3);
    assertThat(updateCaptor.getAllValues())
        .satisfies(AsyncCashoutOfferServiceImplTest::updateHasActivation, Index.atIndex(0));
    assertThat(updateCaptor.getAllValues())
        .satisfies(
            updateDto -> assertNull(updateDto.getCashoutData().getShouldActivate()),
            Index.atIndex(1));
    assertThat(updateCaptor.getAllValues())
        .satisfies(
            updateDto -> assertNull(updateDto.getCashoutData().getShouldActivate()),
            Index.atIndex(2));
  }

  @Test
  void groupSizeCouldBePerType() {
    CashoutOfferBufferingProperties props = new CashoutOfferBufferingProperties();
    props.setWindowTime(Duration.ofMillis(100));
    props.setMaxSize(1);
    props.setGroups(Collections.singletonMap("SGL", 5));
    props.setMaxTime(Duration.ofMinutes(5));

    AsyncCashoutOfferServiceImpl service =
        new AsyncCashoutOfferServiceImpl(
            props, remoteCashoutApi, offerToBetUpdate, betUpdatesTopic, 1, "BUFFER");

    Mockito.when(remoteCashoutApi.getCashoutOffers(any()))
        .thenReturn(Flux.just(CashoutOffer.builder().cashoutOfferReqRef("123").build()));

    sendFewCashoutRequests(service, 5);

    Mockito.verify(remoteCashoutApi, timeout(500).times(1)).getCashoutOffers(any());
  }

  private void sendFewCashoutRequests(AsyncCashoutOfferService service, int requestCount) {
    for (int i = 0; i < requestCount; i++) {
      service.acceptCashoutOfferRequest(
          CashoutRequest.builder()
              .cashoutOfferRequests(
                  Collections.singletonList(createCashoutOffer(String.valueOf(i), "SGL")))
              .build());
    }
  }

  @Test
  @Ignore
  void differentTypeOfBetsAreBufferedSeparately() {
    Mockito.when(remoteCashoutApi.getCashoutOffers(any()))
        .thenReturn(Flux.just(CashoutOffer.builder().cashoutOfferReqRef("123").build()));

    for (int i = 0; i < 5; i++) {
      service.acceptCashoutOfferRequest(
          CashoutRequest.builder()
              .cashoutOfferRequests(
                  Collections.singletonList(createCashoutOffer(String.valueOf(i), "SGL")))
              .build());
      service.acceptCashoutOfferRequest(
          CashoutRequest.builder()
              .cashoutOfferRequests(
                  Collections.singletonList(createCashoutOffer(String.valueOf(i), "DBL")))
              .build());
    }

    Mockito.verify(remoteCashoutApi, timeout(500).times(1))
        .getCashoutOffers(
            argThat(
                req ->
                    req.getCashoutOfferRequests().size() == 5
                        && req.getCashoutOfferRequests()
                            .iterator()
                            .next()
                            .getBet()
                            .getBetType()
                            .equals("SGL")));
    Mockito.verify(remoteCashoutApi, timeout(500).times(1))
        .getCashoutOffers(
            argThat(
                req ->
                    req.getCashoutOfferRequests().size() == 5
                        && req.getCashoutOfferRequests()
                            .iterator()
                            .next()
                            .getBet()
                            .getBetType()
                            .equals("DBL")));
  }

  @Test
  void testExceptionsNotCancellingFlux() {
    CashoutOfferBufferingProperties props = new CashoutOfferBufferingProperties();
    props.setWindowTime(Duration.ofMillis(100));
    props.setMaxSize(1);
    props.setMaxTime(Duration.ofMinutes(5));
    AsyncCashoutOfferServiceImpl service =
        new AsyncCashoutOfferServiceImpl(
            props, remoteCashoutApi, offerToBetUpdate, betUpdatesTopic, 1, "BUFFER");

    mockToReturnSocketExceptionFirstAndThenContinueNormally();

    int numOfRequestsToSend = 10;

    sendFewCashoutRequests(service, numOfRequestsToSend);

    Mockito.verify(betUpdatesTopic, timeout(500).times(9)).sendBetUpdate(any(), any());

    await()
        .pollDelay(Duration.ofSeconds(2))
        .timeout(Duration.ofSeconds(3))
        .until(service::getDisposable, disp -> !disp.isDisposed());

    await()
        .pollDelay(Duration.ofSeconds(2))
        .timeout(Duration.ofSeconds(3))
        .until(service::getSink, sink -> !sink.isCancelled());
  }

  private void mockCashoutApi() {
    Mockito.when(remoteCashoutApi.getCashoutOffers(any(CashoutRequest.class)))
        .thenAnswer(
            invocation -> {
              CashoutRequest request = invocation.getArgument(0);
              List<CashoutOffer> offersList = new ArrayList<>();
              for (CashoutOfferRequest offerRequest : request.getCashoutOfferRequests()) {
                offersList.add(
                    CashoutOffer.builder()
                        .cashoutValue(2.0)
                        .cashoutOfferReqRef(offerRequest.getCashoutOfferReqRef())
                        .build());
              }
              return Flux.fromIterable(offersList);
            });
  }

  private void mockToReturnSocketExceptionFirstAndThenContinueNormally() {
    Mockito.when(remoteCashoutApi.getCashoutOffers(any(CashoutRequest.class)))
        .thenAnswer(
            invocation -> {
              CashoutRequest request = invocation.getArgument(0);
              String betId =
                  request.getCashoutOfferRequests().iterator().next().getCashoutOfferReqRef();
              if (betId.equals("0")) {
                return Flux.error(new SocketTimeoutException("timeout"));
              } else {
                return Flux.just(
                    CashoutOffer.builder().cashoutOfferReqRef(betId).cashoutValue(2.2d).build());
              }
            });
  }

  @Test
  void onlyUniqueRequestsAreSent() {
    CashoutRequest req1 =
        CashoutRequest.builder()
            .cashoutOfferRequests(Collections.singletonList(createCashoutOffer("123", "SGL")))
            .build();

    Mockito.when(remoteCashoutApi.getCashoutOffers(any()))
        .thenReturn(Flux.just(CashoutOffer.builder().cashoutOfferReqRef("123").build()));

    service.acceptCashoutOfferRequest(req1);
    service.acceptCashoutOfferRequest(req1);

    Mockito.verify(remoteCashoutApi, Mockito.timeout(500).times(1)).getCashoutOffers(any());
    Mockito.verify(betUpdatesTopic, Mockito.timeout(500)).sendBetUpdate(eq("123"), any());
  }

  @Test
  void noDuplicatesWithinWindowTime() {
    Mockito.when(remoteCashoutApi.getCashoutOffers(any())).thenReturn(Flux.empty());

    sendFewCashoutRequests(service, 5);
    sendFewCashoutRequests(service, 5);

    // adding delay between second batch of requests, so that it comes in separate "window"

    Executors.newScheduledThreadPool(1)
        .schedule(
            () -> {
              sendFewCashoutRequests(service, 5);
              sendFewCashoutRequests(service, 5);
            },
            200,
            TimeUnit.MILLISECONDS);

    // expecting to requests because there will be two batches because of windowing
    Mockito.verify(remoteCashoutApi, after(500).atLeast(2)).getCashoutOffers(any());
  }

  @Test
  void ioExceptionsAreNotSentToKafka() {
    IOException ioException = new IOException();
    Mockito.when(remoteCashoutApi.getCashoutOffers(any())).thenReturn(Flux.error(ioException));

    service.acceptCashoutOfferRequest(
        CashoutRequest.builder()
            .cashoutOfferRequests(Collections.singletonList(createCashoutOffer("123", "SGL")))
            .build());

    Mockito.verify(betUpdatesTopic, after(500).never()).sendBetUpdateError("123", ioException);
  }

  @Test
  void fewCashoutOfferRequestsAreMergedIntoOne() {
    Mockito.when(remoteCashoutApi.getCashoutOffers(any()))
        .thenReturn(Flux.just(CashoutOffer.builder().cashoutOfferReqRef("123").build()));

    CashoutRequest req1 =
        CashoutRequest.builder()
            .cashoutOfferRequests(
                Arrays.asList(createCashoutOffer("123", "SGL"), createCashoutOffer("456", "SGL")))
            .build();

    CashoutRequest req2 =
        CashoutRequest.builder()
            .cashoutOfferRequests(Collections.singletonList(createCashoutOffer("567", "SGL")))
            .build();

    CashoutRequest req3 =
        CashoutRequest.builder()
            .cashoutOfferRequests(Collections.singletonList(createCashoutOffer("890", "SGL")))
            .build();

    service.acceptCashoutOfferRequest(req1);
    service.acceptCashoutOfferRequest(req2);
    service.acceptCashoutOfferRequest(req3);
    Mockito.verify(remoteCashoutApi, Mockito.timeout(500).times(1))
        .getCashoutOffers(
            CashoutRequest.builder()
                .cashoutOfferRequests(
                    Arrays.asList(
                        createCashoutOffer("123", "SGL"),
                        createCashoutOffer("456", "SGL"),
                        createCashoutOffer("567", "SGL"),
                        createCashoutOffer("890", "SGL")))
                .build());
  }

  @Test
  void cashoutOffersOfSameTypeAreGrouped() {
    Mockito.when(remoteCashoutApi.getCashoutOffers(any()))
        .thenReturn(Flux.just(CashoutOffer.builder().cashoutOfferReqRef("123").build()));

    CashoutRequest req1 =
        CashoutRequest.builder()
            .cashoutOfferRequests(Collections.singletonList(createCashoutOffer("123", "SGL")))
            .build();

    CashoutRequest req2 =
        CashoutRequest.builder()
            .cashoutOfferRequests(Collections.singletonList(createCashoutOffer("567", "DBL")))
            .build();

    CashoutRequest req3 =
        CashoutRequest.builder()
            .cashoutOfferRequests(Collections.singletonList(createCashoutOffer("890", "ACC5")))
            .build();

    service.acceptCashoutOfferRequest(req1);
    service.acceptCashoutOfferRequest(req2);
    service.acceptCashoutOfferRequest(req3);
    Mockito.verify(remoteCashoutApi, Mockito.timeout(500).times(3)).getCashoutOffers(any());
  }

  private CashoutOfferRequest createCashoutOffer(String cashoutOfferReqRef, String betType) {
    return createCashoutOffer(cashoutOfferReqRef, betType, "2", "1");
  }

  private CashoutOfferRequest createCashoutOffer(
      String cashoutOfferReqRef, String betType, String priceNum, String priceDen) {
    return CashoutOfferRequest.builder()
        .cashoutOfferReqRef(cashoutOfferReqRef)
        .bet(createBet(betType, priceNum, priceDen))
        .build();
  }

  private CashoutBet createBet(String betType, String priceNum, String priceDen) {
    return CashoutBet.builder()
        .betType(betType)
        .stakeAmount("1.0")
        .leg(
            CashoutLeg.builder()
                .legNo("1")
                .part(
                    CashoutPart.builder()
                        .partNo("1")
                        .type("2.0")
                        .ladder("STABLE")
                        .result("-")
                        .strikePrice(CashoutPrice.builder().den("1").num("10").build())
                        .spotPrice(CashoutPrice.builder().num(priceNum).den(priceDen).build())
                        .build())
                .build())
        .build();
  }
}
