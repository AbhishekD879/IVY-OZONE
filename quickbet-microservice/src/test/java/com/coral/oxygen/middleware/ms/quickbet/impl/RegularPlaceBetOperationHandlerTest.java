package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.PLACE_BET_ERROR_RESPONSE_CODE;
import static com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest.SCORECAST_SELECTION_TYPE;
import static java.util.Collections.singletonList;
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

import com.coral.bpp.api.model.bet.api.response.UserDataResponse;
import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.BppComponent;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.FreeBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.LuckyDipBetPlacementRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.RegularPlaceBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputEvent;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputMarket;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputOutcome;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputPrice;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2.OddsBoostToken;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2.RegularSelectionResponse;
import com.coral.oxygen.middleware.ms.quickbet.converter.BetToReceiptResponseDtoConverter;
import com.coral.oxygen.middleware.ms.quickbet.utils.TestUtils;
import com.entain.oxygen.bettingapi.model.bet.api.common.IdRef;
import com.entain.oxygen.bettingapi.model.bet.api.common.Stake;
import com.entain.oxygen.bettingapi.model.bet.api.common.YesNo;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetsDto;
import com.entain.oxygen.bettingapi.model.bet.api.response.Bet;
import com.entain.oxygen.bettingapi.model.bet.api.response.BetError;
import com.entain.oxygen.bettingapi.model.bet.api.response.BetsResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.ErrorBody;
import com.entain.oxygen.bettingapi.model.bet.api.response.GeneralResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.Leg;
import com.entain.oxygen.bettingapi.model.bet.api.response.Payout;
import com.entain.oxygen.bettingapi.model.bet.api.response.Price;
import com.entain.oxygen.bettingapi.model.bet.api.response.SportsLeg;
import com.entain.oxygen.bettingapi.model.bet.api.response.oxi.base.ClaimedOffer;
import com.entain.oxygen.bettingapi.service.BettingService;
import io.vavr.control.Try;
import java.util.Collections;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class RegularPlaceBetOperationHandlerTest {

  @Mock private Session session;

  @Mock private BppComponent bppComponent;

  @Mock private BettingService bettingService;

  @Mock private NotConfirmedBetsHandler notConfirmedBetsHandler;

  @Mock private LuckDipPlaceBetOperationHandler luckDipPlaceBetOperationHandler;

  private RegularPlaceBetOperationHandler regularPlaceBetOperationHandler;

  @BeforeEach
  void setUp() {
    regularPlaceBetOperationHandler =
        new RegularPlaceBetOperationHandler(
            bppComponent,
            bettingService,
            new BetToReceiptResponseDtoConverter(),
            notConfirmedBetsHandler,
            mock(SelectionOperations.class),
            luckDipPlaceBetOperationHandler);

    UserDataResponse userData = new UserDataResponse();
    userData.setSportBookUserName("test");
    when(bppComponent.fetchUserData(any())).thenReturn(Try.success(userData));
  }

  @Test
  void testPlaceBetWhenThereIsNoSelectionInSession() {
    RegularPlaceBetRequest regularPlaceBetRequest = new RegularPlaceBetRequest();
    Session session = mock(Session.class);
    when(session.getRegularSelectionResponse()).thenReturn(null);
    regularPlaceBetOperationHandler.placeBet(session, regularPlaceBetRequest);

    RegularPlaceBetResponse.Data data = new RegularPlaceBetResponse.Data();
    data.setError(
        new RegularPlaceBetResponse.Error(
            Messages.INTERNAL_PLACE_BET_PROCESSING.code(),
            "Can't find selection data in remote bet slip for session " + session));
    RegularPlaceBetResponse response = new RegularPlaceBetResponse(data);

    verify(session).sendData(eq(Messages.PLACE_BET_ERROR_RESPONSE_CODE.code()), eq(response));
  }

  @Test
  void testPlaceBetWithOddsBoostFreebet() {
    RegularPlaceBetRequest request = new RegularPlaceBetRequest();
    request.setStake("1");
    request.setPrice("4/1");
    request.setToken("123");
    request.setWinType("WIN");
    request.setChannel("A");
    FreeBetRequest freebet = new FreeBetRequest();
    freebet.setOddsBoost(true);
    request.setFreebet(freebet);

    Session session = mock(Session.class);
    RegularSelectionResponse response = new RegularSelectionResponse();
    OddsBoostToken oddsBoost = new OddsBoostToken();
    oddsBoost.setEnhancedOddsPriceDen("1");
    oddsBoost.setEnhancedOddsPriceNum("5");
    oddsBoost.setId("12");
    response.setOddsBoost(oddsBoost);
    OutputEvent event = new OutputEvent();
    OutputMarket outputMarket = new OutputMarket();
    OutputOutcome outputOutcome = new OutputOutcome();
    outputOutcome.setId("123");
    outputMarket.setOutcomes(singletonList(outputOutcome));
    event.setMarkets(singletonList(outputMarket));
    response.setEvent(event);
    RegularSelectionRequest selectionRequest = new RegularSelectionRequest();
    selectionRequest.setSelectionType("simple");
    selectionRequest.setOutcomeIds(singletonList(123L));
    response.setRequest(selectionRequest);
    when(session.getRegularSelectionResponse()).thenReturn(response);

    regularPlaceBetOperationHandler.placeBet(session, request);

    verify(bettingService)
        .placeBet(
            anyString(),
            argThat(
                arg ->
                    arg.getChannel().equals("A")
                        && arg.getEnhancedPriceDen().equals(1)
                        && arg.getEnhancedPriceNum().equals(5)
                        && arg.getFreebet().getId().equals(12L)
                        && arg.getFreebet().getStake().equals("0")));
  }

  @Test
  void testPlaceScorecast() {
    RegularPlaceBetRequest regularPlaceBetRequest = new RegularPlaceBetRequest();
    regularPlaceBetRequest.setStake("1");
    regularPlaceBetRequest.setPrice("3/1");
    regularPlaceBetRequest.setToken("123");
    regularPlaceBetRequest.setWinType("WIN");

    Session session = mock(Session.class);
    SessionDto sessionDto =
        TestUtils.deserializeWithJackson("sessionDtoWithScorecast.json", SessionDto.class);
    RegularSelectionResponse selectionResponse = new RegularSelectionResponse();
    OutputEvent event = new OutputEvent();
    OutputMarket outputMarket = new OutputMarket();
    outputMarket.setOutcomes(
        sessionDto.getRegularSelectionRequest().getOutcomeIds().stream()
            .map(
                outcomeId -> {
                  OutputOutcome outputOutcome = new OutputOutcome();
                  outputOutcome.setId(String.valueOf(outcomeId));
                  return outputOutcome;
                })
            .collect(Collectors.toList()));
    event.setMarkets(singletonList(outputMarket));
    selectionResponse.setEvent(event);
    selectionResponse.setRequest(sessionDto.getRegularSelectionRequest());
    when(session.getRegularSelectionResponse()).thenReturn(selectionResponse);

    regularPlaceBetOperationHandler.placeBet(session, regularPlaceBetRequest);

    verify(bettingService)
        .placeBet(
            anyString(),
            argThat(
                arg ->
                    arg.getOutcomeCombiRef().equals("SCORECAST")
                        && arg.getPriceNum().equals(3)
                        && arg.getPriceDen().equals(1)
                        && arg.getWinPlaceRef().equals("WIN")
                        && arg.getAdditionalOutcomeRefs().size() == 1
                        && arg.getAdditionalOutcomeRefs().contains("222")));
  }

  @Test
  void placeBetWithOverask() {
    // preparation
    RegularPlaceBetRequest request = new RegularPlaceBetRequest();
    request.setToken(UUID.randomUUID().toString());
    request.setWinType("WIN");
    request.setStake("2");
    request.setPrice("2/1");

    RegularSelectionRequest selectionRequest = new RegularSelectionRequest();
    selectionRequest.setSelectionType(RegularSelectionRequest.SIMPLE_SELECTION_TYPE);
    Long outcomeId = 460051054L;
    selectionRequest.setOutcomeIds(singletonList(outcomeId));

    RegularSelectionResponse outcomeResponse = new RegularSelectionResponse();
    OutputEvent outputEvent = new OutputEvent();
    OutputMarket outputMarket = new OutputMarket();
    OutputOutcome outputOutcome = new OutputOutcome();
    outputMarket.setOutcomes(singletonList(outputOutcome));
    outputEvent.setMarkets(singletonList(outputMarket));
    outcomeResponse.setEvent(outputEvent);
    outcomeResponse.setRequest(selectionRequest);

    Bet bet = new Bet();
    bet.setIsReferred(YesNo.Y);
    BetsResponse betsResponse = new BetsResponse();
    betsResponse.setBet(singletonList(bet));
    GeneralResponse<BetsResponse> generalResponse = new GeneralResponse<>(betsResponse, null);

    when(session.getRegularSelectionResponse()).thenReturn(outcomeResponse);
    when(bettingService.placeBet(anyString(), any(BetsDto.class))).thenReturn(generalResponse);

    // acton
    regularPlaceBetOperationHandler.placeBet(session, request);

    // verification
    verify(notConfirmedBetsHandler)
        .handle(eq(session), argThat(arg -> arg.getResponse().equals(betsResponse)), anyString());
  }

  @Test
  void testPlaceBetWithFreeBetId() {

    RegularPlaceBetRequest request = createPlaceBetRequest();
    FreeBetRequest freeBetRequest = new FreeBetRequest();
    freeBetRequest.setId(12L);
    freeBetRequest.setStake("1/3");
    request.setFreebet(freeBetRequest);
    RegularSelectionResponse response = createPlaceBetResponse("simple");
    Bet bet = bet();
    BetsResponse betsResponse = new BetsResponse();
    betsResponse.setBet(singletonList(bet));
    GeneralResponse<BetsResponse> generalResponse = new GeneralResponse<>(betsResponse, null);
    Session session = mock(Session.class);

    when(session.getRegularSelectionResponse()).thenReturn(response);
    when(bettingService.placeBet(anyString(), any(BetsDto.class))).thenReturn(generalResponse);
    // action
    regularPlaceBetOperationHandler.placeBet(session, request);
    // verification
    verify(bettingService, atLeastOnce()).placeBet(anyString(), any(BetsDto.class));
  }

  @Test
  void testPlaceBetWithHandicap() {
    RegularPlaceBetRequest request = new RegularPlaceBetRequest();
    request.setWinType("WIN");
    request.setStake("1");
    request.setPrice("3/1");
    request.setHandicap("2.5");

    Session session = mock(Session.class);
    RegularSelectionResponse response = new RegularSelectionResponse();
    OutputEvent event = new OutputEvent();
    OutputMarket outputMarket = new OutputMarket();
    OutputOutcome outputOutcome = new OutputOutcome();
    outputOutcome.setId("123");
    outputMarket.setOutcomes(singletonList(outputOutcome));
    event.setMarkets(singletonList(outputMarket));
    response.setEvent(event);
    OutputPrice selectionPrice = new OutputPrice();
    selectionPrice.setHandicapValueDec("3.5");
    response.setSelectionPrice(selectionPrice);
    RegularSelectionRequest selectionRequest = new RegularSelectionRequest();
    selectionRequest.setSelectionType("simple");
    selectionRequest.setOutcomeIds(singletonList(123L));
    response.setRequest(selectionRequest);
    when(session.getRegularSelectionResponse()).thenReturn(response);

    regularPlaceBetOperationHandler.placeBet(session, request);

    verify(bettingService)
        .placeBet(
            any(),
            argThat(arg -> arg.getPriceNum().equals(3) && arg.getHandicapValueDec().equals("2.5")));
  }

  @Test
  void testThrowExceptionIfWinTypeIsEmpty() {
    // preparation
    when(session.getRegularSelectionResponse()).thenReturn(new RegularSelectionResponse());
    RegularPlaceBetRequest request = new RegularPlaceBetRequest();

    // acton
    regularPlaceBetOperationHandler.placeBet(session, request);

    // verification
    verify(bettingService, times(0)).placeBet(anyString(), any(BetsDto.class));
    verify(session).sendData(eq(PLACE_BET_ERROR_RESPONSE_CODE.code()), any());
  }

  @Test
  void testPlaceBetWithChannelWeb() {
    RegularPlaceBetRequest request = createPlaceBetRequest();

    Session session = mock(Session.class);
    RegularSelectionResponse response = createPlaceBetResponse("simple");
    when(session.getRegularSelectionResponse()).thenReturn(response);

    regularPlaceBetOperationHandler.placeBet(session, request);

    verify(bettingService)
        .placeBet(anyString(), argThat(arg -> arg.getClientUserAgent().equals("S|H|A0000000")));
  }

  @Test
  void shouldReturnErrorWhenPlaceBetResponseBodyContainsError() {
    // GIVEN
    RegularPlaceBetRequest request = createPlaceBetRequest();

    ErrorBody error = new ErrorBody();
    error.setStatus("status");
    error.setError("error");
    GeneralResponse<BetsResponse> generalResponse = new GeneralResponse<>(null, error);
    when(bettingService.placeBet(any(), any())).thenReturn(generalResponse);

    RegularSelectionResponse response = createPlaceBetResponse("simple");
    when(session.getRegularSelectionResponse()).thenReturn(response);

    // WHEN
    regularPlaceBetOperationHandler.placeBet(session, request);

    // THEN
    ArgumentCaptor<RegularPlaceBetResponse> captor =
        ArgumentCaptor.forClass(RegularPlaceBetResponse.class);
    verify(session).sendData(eq(PLACE_BET_ERROR_RESPONSE_CODE.code()), captor.capture());

    assertThat(captor.getValue().getData().getError().getCode()).isEqualTo("status");
    assertThat(captor.getValue().getData().getError().getDescription()).isEqualTo("error");
  }

  @Test
  void shouldReturnErrorWhenStakeIsNotSet() {
    // GIVEN
    when(session.getRegularSelectionResponse()).thenReturn(new RegularSelectionResponse());
    RegularPlaceBetRequest request = createPlaceBetRequest();
    request.setStake(null);

    // WHEN
    regularPlaceBetOperationHandler.placeBet(session, request);

    // THEN
    ArgumentCaptor<RegularPlaceBetResponse> captor =
        ArgumentCaptor.forClass(RegularPlaceBetResponse.class);
    verify(session).sendData(eq(PLACE_BET_ERROR_RESPONSE_CODE.code()), captor.capture());

    assertThat(captor.getValue().getData().getError().getCode())
        .isEqualTo(Messages.STAKE_EMPTY.code());
  }

  @Test
  void shouldReturnErrorWhenBetPlaceResponseContainsError() {
    when(session.getRegularSelectionResponse()).thenReturn(new RegularSelectionResponse());
    RegularPlaceBetRequest request = createPlaceBetRequest();

    RegularSelectionResponse response = createPlaceBetResponse("simple");
    when(session.getRegularSelectionResponse()).thenReturn(response);

    BetsResponse body = new BetsResponse();
    Bet bet = new Bet();
    bet.setId(123L);
    body.setBet(singletonList(bet));
    BetError betError = new BetError();
    betError.setCode("code");
    betError.setErrorDesc("error desc");
    body.setBetError(singletonList(betError));
    GeneralResponse<BetsResponse> generalResponse = new GeneralResponse<>(body, null);
    when(bettingService.placeBet(any(), any())).thenReturn(generalResponse);

    // WHEN
    regularPlaceBetOperationHandler.placeBet(session, request);

    // THEN
    ArgumentCaptor<RegularPlaceBetResponse> captor =
        ArgumentCaptor.forClass(RegularPlaceBetResponse.class);
    verify(session).sendData(eq(PLACE_BET_ERROR_RESPONSE_CODE.code()), captor.capture());

    assertThat(captor.getValue().getData().getError().getCode()).isEqualTo(betError.getCode());
    assertThat(captor.getValue().getData().getError().getDescription())
        .isEqualTo(betError.getErrorDesc());
  }

  @Test
  void shouldSetPriceToNullWhenThereIsBetErrorAndBetIsScorecast() {
    when(session.getRegularSelectionResponse()).thenReturn(new RegularSelectionResponse());
    RegularPlaceBetRequest request = createPlaceBetRequest();

    RegularSelectionResponse response = createPlaceBetResponse(SCORECAST_SELECTION_TYPE);
    when(session.getRegularSelectionResponse()).thenReturn(response);

    BetsResponse body = new BetsResponse();
    Bet bet = new Bet();
    bet.setId(123L);
    body.setBet(singletonList(bet));
    BetError betError = new BetError();
    betError.setCode("code");
    betError.setErrorDesc("error desc");
    Price price = new Price();
    price.setPriceDen("1");
    price.setPriceNum("2");
    price.setPriceTypeRef(new IdRef());
    betError.setPrice(singletonList(price));
    body.setBetError(singletonList(betError));
    GeneralResponse<BetsResponse> generalResponse = new GeneralResponse<>(body, null);
    when(bettingService.placeBet(any(), any())).thenReturn(generalResponse);

    // WHEN
    regularPlaceBetOperationHandler.placeBet(session, request);

    // THEN
    ArgumentCaptor<RegularPlaceBetResponse> captor =
        ArgumentCaptor.forClass(RegularPlaceBetResponse.class);
    verify(session).sendData(eq(PLACE_BET_ERROR_RESPONSE_CODE.code()), captor.capture());

    assertThat(captor.getValue().getData().getError().getPrice()).isNull();
  }

  @Test
  void shouldContainClaimedOffers() {
    when(session.getRegularSelectionResponse()).thenReturn(createPlaceBetResponse("simple"));

    BetsResponse betsResponse = new BetsResponse();
    Bet bet = bet();

    final String offerID = "OfferID";
    ClaimedOffer claimedOffer = new ClaimedOffer();
    claimedOffer.setOfferId(offerID);
    bet.setClaimedOffers(singletonList(claimedOffer));
    betsResponse.setBet(singletonList(bet));
    GeneralResponse<BetsResponse> generalResponse = new GeneralResponse<>(betsResponse, null);
    when(bettingService.placeBet(any(), any())).thenReturn(generalResponse);

    // WHEN
    regularPlaceBetOperationHandler.placeBet(session, createPlaceBetRequest());

    // THEN
    ArgumentCaptor<RegularPlaceBetResponse> placeBetResponse =
        ArgumentCaptor.forClass(RegularPlaceBetResponse.class);
    verify(session).sendData(anyString(), placeBetResponse.capture());
    List<ClaimedOffer> claimedOffers =
        placeBetResponse.getValue().getData().getReceipt().get(0).getClaimedOffers();
    assertThat(claimedOffers).hasSize(1);
    assertThat(claimedOffers.get(0).getOfferId()).isEqualTo(offerID);
  }

  @Test
  void testPlaceBetWithLuckyDipDummySelection() {
    RegularPlaceBetRequest request = createPlaceBetRequest();
    request.setChannel("channel");
    request.setIp("128.1.0.0");

    Session session = mock(Session.class);
    RegularSelectionResponse response = createPlaceBetResponse("simple");
    response.setLDip(true);
    response.setLDipMar("1234567");
    when(session.getRegularSelectionResponse()).thenReturn(response);
    LuckyDipBetPlacementRequest luckyDipBetPlacementRequest =
        buildLuckyDipRequest(request, response.getLDipMar());
    doNothing()
        .when(luckDipPlaceBetOperationHandler)
        .processLuckyDipPlaceBet(session, luckyDipBetPlacementRequest);

    regularPlaceBetOperationHandler.placeBet(session, request);
    Assertions.assertNotNull(regularPlaceBetOperationHandler);
  }

  private Bet bet() {
    Bet bet = new Bet();
    bet.setId(123L);
    bet.setIsConfirmed(YesNo.Y);
    bet.setStake(new Stake());

    Leg leg = new Leg();
    SportsLeg sportsLeg = new SportsLeg();
    String CashoutValue = new String();
    sportsLeg.setLegPart(Collections.emptyList());
    Price price = new Price().setPriceTypeRef(new IdRef());
    price.setPriceDen("1");
    price.setPriceNum("2");
    sportsLeg.setPrice(price);
    leg.setSportsLeg(sportsLeg);
    bet.setLeg(singletonList(leg));

    bet.setPayout(singletonList(new Payout()));
    bet.setCashoutValue(CashoutValue);
    return bet;
  }

  @Test
  void testPlaceBetWithChannelAndroidZ() {
    testWithChannel("z", "S|W|A0000000");
  }

  @Test
  void testPlaceBetWithChannelIosY() {
    testWithChannel("y", "S|W|I0000000");
  }

  @Test
  void testPlaceBetWithChannelAndroid() {
    testWithChannel("A", "S|W|A0000000");
  }

  @Test
  void testConvertPrice() {
    try {
      ReflectionTestUtils.invokeMethod(
          regularPlaceBetOperationHandler, "convertPrice", "43", "12s2d3d");
    } catch (Exception e) {
      Assertions.assertNotNull(e);
    }
  }

  @Test
  void testPlaceBetWithChannelIos() {
    testWithChannel("i", "S|W|I0000000");
  }

  private void testWithChannel(String channel, String userAgent) {
    RegularPlaceBetRequest request = new RegularPlaceBetRequest();
    request.setStake("1");
    request.setPrice("4/1");
    request.setToken("123");
    request.setWinType("WIN");
    request.setChannel(channel);

    Session session = mock(Session.class);
    RegularSelectionResponse response = new RegularSelectionResponse();
    OutputEvent event = new OutputEvent();
    OutputMarket outputMarket = new OutputMarket();
    OutputOutcome outputOutcome = new OutputOutcome();
    outputOutcome.setId("123");
    outputMarket.setOutcomes(singletonList(outputOutcome));
    event.setMarkets(singletonList(outputMarket));
    response.setEvent(event);
    RegularSelectionRequest selectionRequest = new RegularSelectionRequest();
    selectionRequest.setSelectionType("simple");
    selectionRequest.setOutcomeIds(singletonList(123L));
    response.setRequest(selectionRequest);
    when(session.getRegularSelectionResponse()).thenReturn(response);

    regularPlaceBetOperationHandler.placeBet(session, request);

    verify(bettingService)
        .placeBet(
            anyString(),
            argThat(
                arg ->
                    arg.getChannel().equals(channel)
                        && arg.getClientUserAgent().equals(userAgent)));
  }

  private RegularSelectionResponse createPlaceBetResponse(String selectionType) {
    RegularSelectionResponse response = new RegularSelectionResponse();
    OutputEvent event = new OutputEvent();
    OutputMarket outputMarket = new OutputMarket();
    OutputOutcome outputOutcome = new OutputOutcome();
    outputOutcome.setId("123");
    outputMarket.setOutcomes(singletonList(outputOutcome));
    event.setMarkets(singletonList(outputMarket));
    response.setEvent(event);
    RegularSelectionRequest selectionRequest = new RegularSelectionRequest();
    selectionRequest.setSelectionType(selectionType);
    selectionRequest.setOutcomeIds(singletonList(123L));
    response.setRequest(selectionRequest);
    return response;
  }

  private RegularPlaceBetRequest createPlaceBetRequest() {
    RegularPlaceBetRequest request = new RegularPlaceBetRequest();
    request.setStake("1");
    request.setPrice("4/1");
    request.setToken("123");
    request.setWinType("WIN");
    request.setClientUserAgent("S|H|A0000000");
    return request;
  }

  private LuckyDipBetPlacementRequest buildLuckyDipRequest(
      RegularPlaceBetRequest request, String luckyDipMarket) {
    LuckyDipBetPlacementRequest luckyDipBetPlacementRequest =
        new LuckyDipBetPlacementRequest(
            request.getToken(), request.getStake(), luckyDipMarket, request.getWinType());
    luckyDipBetPlacementRequest.setChannel(request.getChannel());
    luckyDipBetPlacementRequest.setClientUserAgent(request.getClientUserAgent());
    luckyDipBetPlacementRequest.setIp(request.getIp());
    return luckyDipBetPlacementRequest;
  }
}
