package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.REGULAR_OUTCOME_RESPONSE_CODE;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.REGULAR_OUTCOME_RESPONSE_ERROR_CODE;
import static com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest.SCORECAST_SELECTION_TYPE;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatExceptionOfType;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputEvent;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputMarket;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputOutcome;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputPrice;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2.RegularSelectionResponse;
import com.coral.oxygen.middleware.ms.quickbet.converter.EventToOutputEventConverter;
import com.coral.oxygen.middleware.ms.quickbet.converter.MarketToOutputMarketConverter;
import com.coral.oxygen.middleware.ms.quickbet.converter.OutcomeToOutputOutcomeConverter;
import com.coral.oxygen.middleware.ms.quickbet.converter.PriceToOutputPriceConverter;
import com.coral.oxygen.middleware.ms.quickbet.converter.RegularSelectionResponseToBuildBetDtoConverter;
import com.coral.oxygen.middleware.ms.quickbet.utils.TestUtils;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Scorecast;
import com.entain.oxygen.bettingapi.exception.BettingConnectionException;
import com.entain.oxygen.bettingapi.model.bet.api.response.BuildBetResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.ErrorBody;
import com.entain.oxygen.bettingapi.model.bet.api.response.GeneralResponse;
import com.entain.oxygen.bettingapi.service.BettingService;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.core.env.Environment;

@ExtendWith(MockitoExtension.class)
class RegularSelectionOperationHandlerTest {

  @Mock private SiteServerService siteServerServiceMock;
  @Mock private LiveServService liveServServiceMock;
  @Mock private BettingService bettingServiceMock;

  @Mock private com.coral.bpp.api.service.BppService bppMock;
  @Mock private Session sessionMock;
  @Mock private ScorecastPriceService scorecastPriceService;

  @Mock private Environment environment;

  private RegularSelectionOperationHandler regularSelectionOperationHandler;

  @BeforeEach
  void setUp() {
    PriceToOutputPriceConverter priceConverter = new PriceToOutputPriceConverter();
    RegularSelectionResponseToBuildBetDtoConverter buildBetDtoConverter =
        new RegularSelectionResponseToBuildBetDtoConverter();
    EventToOutputEventConverter eventConverter =
        new EventToOutputEventConverter(
            new MarketToOutputMarketConverter(new OutcomeToOutputOutcomeConverter()));
    RegularFanzoneSelectionHandler regularFanzoneSelectionHandler =
        new RegularFanzoneSelectionHandler();
    regularSelectionOperationHandler =
        new RegularSelectionOperationHandler(
            siteServerServiceMock,
            liveServServiceMock,
            bettingServiceMock,
            eventConverter,
            priceConverter,
            buildBetDtoConverter,
            scorecastPriceService,
            regularFanzoneSelectionHandler,
            environment);
  }

  @Test
  void addSelectionSimpleTest() {
    // preparation
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(460826676L));
    request.setSelectionType(RegularSelectionRequest.SIMPLE_SELECTION_TYPE);
    request.setToken("dfsdfsfdsf");

    Event event =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/simple_selection_event.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(Collections.singletonList(460826676L)))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    BuildBetResponse buildBetResponse =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/buildBetResponse.json", BuildBetResponse.class);
    doReturn(new GeneralResponse<>(buildBetResponse, null))
        .when(bettingServiceMock)
        .buildBet(any(), any());
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"LB_TST0"});

    // acton
    regularSelectionOperationHandler.addSelection(sessionMock, request);

    verify(bettingServiceMock).buildBet(anyString(), Mockito.any());
  }

  @Test
  void addSelectionSimpleFreeBetsEmptyTest() {
    // preparation
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(460826676L));
    request.setSelectionType(RegularSelectionRequest.SIMPLE_SELECTION_TYPE);
    request.setToken("dfsdfsfdsf");

    Event event =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/simple_selection_event.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(Collections.singletonList(460826676L)))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    BuildBetResponse buildBetResponse =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/buildBetResponse_empty_freebets.json", BuildBetResponse.class);

    when(bettingServiceMock.buildBet(any(), any()))
        .thenReturn(new GeneralResponse<>(buildBetResponse, null));
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"LB_TST0", "LB_STG0"});

    // acton
    regularSelectionOperationHandler.addSelection(sessionMock, request);

    verify(bettingServiceMock).buildBet(anyString(), Mockito.any());
  }

  @Test
  void addSelectionSimpleWithOddsBoostTest() {
    // preparation
    String token = "token";
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(460826676L));
    request.setSelectionType(RegularSelectionRequest.SIMPLE_SELECTION_TYPE);
    request.setOddsBoost(true);
    request.setToken(token);

    Event event =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/simple_selection_event.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(Collections.singletonList(460826676L)))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    BuildBetResponse buildBetResponse =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/buildBetResponse.json", BuildBetResponse.class);
    when(bettingServiceMock.buildBet(any(), any()))
        .thenReturn(new GeneralResponse<>(buildBetResponse, null));
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"LB_TST0", "LB_STG0"});

    RegularSelectionResponse response =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/simple_selection_response_with_odds_boost.json",
            RegularSelectionResponse.class);
    com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2.GeneralResponse<
            RegularSelectionResponse>
        expectedResponse =
            new com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2.GeneralResponse<>(
                response);
    // acton
    regularSelectionOperationHandler.addSelection(sessionMock, request);

    // verification
    verify(sessionMock, timeout(100))
        .sendData(REGULAR_OUTCOME_RESPONSE_CODE.code(), expectedResponse);
  }

  @Test
  void addSelectionSimpleWithOddsBoostWhenBPPReturnWithoutFreebetTest() {
    // preparation
    String token = "token";
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(460826676L));
    request.setSelectionType(RegularSelectionRequest.SIMPLE_SELECTION_TYPE);
    request.setOddsBoost(true);
    request.setToken(token);

    Event event =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/simple_selection_event.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(Collections.singletonList(460826676L)))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    BuildBetResponse buildBetResponse =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/build_bet_response_without_tokens.json",
            BuildBetResponse.class);
    when(bettingServiceMock.buildBet(any(), any()))
        .thenReturn(new GeneralResponse<>(buildBetResponse, null));
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"LB_TST0", "LB_STG0"});

    // acton
    regularSelectionOperationHandler.addSelection(sessionMock, request);
    verify(bettingServiceMock).buildBet(anyString(), Mockito.any());
  }

  @Test
  void addSelectionSimpleWithOddsBoostWhenBPPReturnErrorTest() {
    // preparation
    String token = "token";
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(2193493591L));
    request.setSelectionType(RegularSelectionRequest.SIMPLE_SELECTION_TYPE);
    request.setOddsBoost(true);
    request.setToken(token);

    Event event =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/simple_selection_event_BB.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(Collections.singletonList(2193493591L)))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    BuildBetResponse buildBetResponse =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/build_bet_error_response_BB.json", BuildBetResponse.class);
    when(bettingServiceMock.buildBet(any(), any()))
        .thenReturn(new GeneralResponse<>(buildBetResponse, null));

    RegularPlaceBetResponse response =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/simple_selection_response_error_BB.json",
            RegularPlaceBetResponse.class);
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"LB_TST0", "LB_STG0"});

    // acton

    regularSelectionOperationHandler.addSelection(sessionMock, request);

    // verification
    verify(sessionMock).sendData(REGULAR_OUTCOME_RESPONSE_ERROR_CODE.code(), response);
  }

  @Test
  void addSelectionSimpleWithOddsBoostWhenBettingErrorTest() {
    String token = "token";
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(460826676L));
    request.setSelectionType(RegularSelectionRequest.SIMPLE_SELECTION_TYPE);
    request.setOddsBoost(true);
    request.setToken(token);

    Event event =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/simple_selection_event.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(Collections.singletonList(460826676L)))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    BuildBetResponse buildBetResponse =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/build_bet_error_response.json", BuildBetResponse.class);
    ErrorBody errorBody = new ErrorBody();
    errorBody.setError("Error");
    errorBody.setStatus("ErrorStatus");

    when(bettingServiceMock.buildBet(any(), any()))
        .thenReturn(new GeneralResponse<>(buildBetResponse, errorBody));

    RegularPlaceBetResponse response =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/simple_selection_response_with_odds_boost_error.json",
            RegularPlaceBetResponse.class);

    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"LB_TST0", "LB_STG0"});

    regularSelectionOperationHandler.addSelection(sessionMock, request);
    Assertions.assertNotNull(response);
  }

  @Test
  void addSelectionSimpleWithOddsBoostWhenBPPRDoesNotResponseTest() {
    // preparation
    String token = "token";
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(460826676L));
    request.setSelectionType(RegularSelectionRequest.SIMPLE_SELECTION_TYPE);
    request.setOddsBoost(true);
    request.setToken(token);

    Event event =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/simple_selection_event.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(Collections.singletonList(460826676L)))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    when(bettingServiceMock.buildBet(any(), any())).thenThrow(new BettingConnectionException());
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"LB_TST0", "LB_STG0"});

    RegularPlaceBetResponse response =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/simple_selection_response_with_bpp_error.json",
            RegularPlaceBetResponse.class);

    // action
    regularSelectionOperationHandler.addSelection(sessionMock, request);

    // verification
    verify(sessionMock).sendData(REGULAR_OUTCOME_RESPONSE_ERROR_CODE.code(), response);
  }

  @Test
  void addSelectionSimpleWithOddsBoostWhenBetPriceTypeIsSPTest() {
    // preparation
    String token = "token";
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(460826676L));
    request.setSelectionType(RegularSelectionRequest.SIMPLE_SELECTION_TYPE);
    request.setOddsBoost(true);
    request.setToken(token);

    Event event =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/simple_selection_sp_price_event.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(Collections.singletonList(460826676L)))
        .thenReturn(Optional.of(Collections.singletonList(event)));

    TestUtils.deserializeWithGson(
        "impl/fixedBetOperations/simple_selection_response_with_sp_price.json",
        RegularSelectionResponse.class);
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"LB_TST0", "LB_STG0"});

    // acton
    regularSelectionOperationHandler.addSelection(sessionMock, request);

    verify(bettingServiceMock).buildBet(anyString(), Mockito.any());
  }

  @Test
  void testActiveResponseNull() {
    RegularSelectionResponse response = null;
    boolean isActive = regularSelectionOperationHandler.isActive(response);
    Assertions.assertFalse(isActive);
  }

  @Test
  void testActiveResponse() {
    RegularSelectionResponse response = new RegularSelectionResponse();
    boolean isActive = regularSelectionOperationHandler.isActive(response);
    Assertions.assertFalse(isActive);
  }

  @Test
  void testActiveMarket() {
    RegularSelectionResponse response = new RegularSelectionResponse();
    OutputEvent outputEvent = new OutputEvent();
    outputEvent.setMarkets(Collections.emptyList());
    response.setEvent(outputEvent);
    boolean isActive = regularSelectionOperationHandler.isActive(response);
    Assertions.assertFalse(isActive);
  }

  @Test
  void testActiveMarkets() {
    RegularSelectionResponse response = new RegularSelectionResponse();
    OutputEvent outputEvent = new OutputEvent();
    OutputMarket outputMarket = new OutputMarket();
    outputMarket.setOutcomes(Collections.emptyList());
    List<OutputMarket> outputMarkets = new ArrayList<>();
    outputMarkets.add(outputMarket);
    outputEvent.setMarkets(outputMarkets);
    response.setEvent(outputEvent);
    boolean isActive = regularSelectionOperationHandler.isActive(response);
    Assertions.assertFalse(isActive);
  }

  @Test
  void testActiveOutComes() {
    RegularSelectionResponse response = new RegularSelectionResponse();
    OutputEvent outputEvent = new OutputEvent();
    List<OutputMarket> outputMarkets = new ArrayList<>();
    OutputMarket outputMarket = new OutputMarket();
    List<OutputOutcome> outputOutcomes = new ArrayList<>();
    OutputOutcome outputOutcome = new OutputOutcome();
    outputOutcomes.add(outputOutcome);
    outputMarket.setOutcomes(outputOutcomes);
    outputMarkets.add(outputMarket);
    outputEvent.setMarkets(outputMarkets);
    response.setEvent(outputEvent);
    boolean isActive = regularSelectionOperationHandler.isActive(response);
    Assertions.assertFalse(isActive);
  }

  @ParameterizedTest
  @CsvSource({"A, A", "S, A", "A, S", "S, S"})
  void testActive(String marketStatusCode, String outComeStatusCode) {
    RegularSelectionResponse response = new RegularSelectionResponse();
    OutputEvent outputEvent = new OutputEvent();
    List<OutputMarket> outputMarkets = new ArrayList<>();
    OutputMarket outputMarket = new OutputMarket();
    outputMarket.setMarketStatusCode(marketStatusCode);
    List<OutputOutcome> outputOutcomes = new ArrayList<>();
    OutputOutcome outputOutcome = new OutputOutcome();
    outputOutcome.setOutcomeStatusCode(outComeStatusCode);
    outputOutcomes.add(outputOutcome);
    outputMarket.setOutcomes(outputOutcomes);
    outputMarkets.add(outputMarket);
    outputEvent.setMarkets(outputMarkets);
    response.setEvent(outputEvent);
    boolean isActive = regularSelectionOperationHandler.isActive(response);
    Assertions.assertFalse(isActive);
  }

  @ParameterizedTest
  @CsvSource({"A, S, S", "A, A, S"})
  void testSuspended(String eventStatucCode, String marketStatusCode, String outComeStatusCode) {
    RegularSelectionResponse response = new RegularSelectionResponse();
    OutputEvent outputEvent = new OutputEvent();
    outputEvent.setEventStatusCode(eventStatucCode);
    List<OutputMarket> outputMarkets = new ArrayList<>();
    OutputMarket outputMarket = new OutputMarket();
    outputMarket.setMarketStatusCode(marketStatusCode);
    List<OutputOutcome> outputOutcomes = new ArrayList<>();
    OutputOutcome outputOutcome = new OutputOutcome();
    outputOutcome.setOutcomeStatusCode(outComeStatusCode);
    outputOutcomes.add(outputOutcome);
    outputMarket.setOutcomes(outputOutcomes);
    outputMarkets.add(outputMarket);
    outputEvent.setMarkets(outputMarkets);
    response.setEvent(outputEvent);
    boolean isActive = regularSelectionOperationHandler.isActive(response);
    Assertions.assertFalse(isActive);
  }

  @Test
  void testIsActive() {
    RegularSelectionResponse response = new RegularSelectionResponse();
    OutputEvent outputEvent = new OutputEvent();
    outputEvent.setEventStatusCode("A");
    List<OutputMarket> outputMarkets = new ArrayList<>();
    OutputMarket outputMarket = new OutputMarket();
    outputMarket.setMarketStatusCode("A");
    List<OutputOutcome> outputOutcomes = new ArrayList<>();
    OutputOutcome outputOutcome = new OutputOutcome();
    outputOutcome.setOutcomeStatusCode("A");
    outputOutcomes.add(outputOutcome);
    outputMarket.setOutcomes(outputOutcomes);
    outputMarkets.add(outputMarket);
    outputEvent.setMarkets(outputMarkets);
    response.setEvent(outputEvent);
    boolean isActive = regularSelectionOperationHandler.isActive(response);
    Assertions.assertTrue(isActive);
  }

  @Test
  void testValidResponse() {
    boolean isActive = regularSelectionOperationHandler.isValidResponse(null, false);
    Assertions.assertFalse(isActive);
  }

  @Test
  void testValidResponseSelectionPriceNull() {
    RegularSelectionResponse response = new RegularSelectionResponse();
    boolean isActive = regularSelectionOperationHandler.isValidResponse(response, true);
    Assertions.assertFalse(isActive);
  }

  @Test
  void testValidResponseSelectionPrice() {
    RegularSelectionResponse response = new RegularSelectionResponse();
    OutputPrice selectionPrice = new OutputPrice();
    response.setSelectionPrice(selectionPrice);
    boolean isActive = regularSelectionOperationHandler.isValidResponse(response, true);
    Assertions.assertFalse(isActive);
  }

  @Test
  void addSelectionScoreCastTest() {
    // preparation
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(Arrays.asList(463512829L, 463512480L));
    request.setSelectionType(SCORECAST_SELECTION_TYPE);
    request.setAdditional(
        new RegularSelectionRequest.AdditionalParameters() {
          {
            setScorecastMarketId(119576981L);
          }
        });

    Event event =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/scorecast_selection_event.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(Arrays.asList(463512829L, 463512480L)))
        .thenReturn(Optional.of(Collections.singletonList(event)));

    Scorecast scorecast =
        new Scorecast() {
          {
            setId("1");
            setScorerOutcomeId("463512829");
            setScorecastPrices(
                "463512480,2,1,3.00,463512481,2,1,3.00,463512482,2,1,3.00,463512484,3,1,4.00,463512485,2,1,3.00,463512487,2,1,3.00,");
          }
        };
    when(scorecastPriceService.calculate(any(), any(), any())).thenReturn(Optional.empty());
    when(siteServerServiceMock.getScorecast("119576981", "463512829"))
        .thenReturn(Optional.of(scorecast));
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"LB_TST0", "LB_STG0"});

    BuildBetResponse buildBetResponse =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/build_bet_outcome_suspended_response.json",
            BuildBetResponse.class);
    when(bettingServiceMock.buildBet(any(), any()))
        .thenReturn(new GeneralResponse<>(buildBetResponse, null));

    // acton
    regularSelectionOperationHandler.addSelection(sessionMock, request);
    ArgumentCaptor<Double> acPrice = ArgumentCaptor.forClass(Double.class);
    ArgumentCaptor<ScorecastPriceService.ScorecastType> acScorecastType =
        ArgumentCaptor.forClass(ScorecastPriceService.ScorecastType.class);
    verify(scorecastPriceService, times(1))
        .calculate(acPrice.capture(), acPrice.capture(), acScorecastType.capture());
    List<Double> allValues = acPrice.getAllValues();
    assertThat(allValues).isEqualTo(Arrays.asList(1.5, 1.33));
    assertThat(acScorecastType.getValue()).isEqualTo(ScorecastPriceService.ScorecastType.D);
  }

  @Test
  void testAddSelection() {
    Session session = mock(Session.class);
    regularSelectionOperationHandler.addSelection(session, new RegularSelectionRequest());
    verify(session).sendData(Mockito.any(), Mockito.any());
  }

  @Test
  void testAddSelectionType() {
    RegularSelectionRequest regularSelectionRequest = new RegularSelectionRequest();
    regularSelectionRequest.setSelectionType("simple");
    regularSelectionOperationHandler.addSelection(sessionMock, regularSelectionRequest);
    verify(sessionMock).sendData(Mockito.any(), Mockito.any());
  }

  @Test
  void testHandleError() {
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(Arrays.asList(123L));
    when(siteServerServiceMock.getEventToOutcomeForOutcome(Mockito.any()))
        .thenThrow(new SiteServException(Messages.BAD_PRICE, "23", "error"));
    regularSelectionOperationHandler.internalAddSelection(sessionMock, request);
    verify(siteServerServiceMock).getEventToOutcomeForOutcome(Mockito.any());
  }

  @Test
  void testInternalAddSelection() {
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(Arrays.asList(123L));
    when(siteServerServiceMock.getEventToOutcomeForOutcome(Mockito.any()))
        .thenThrow(new SiteServException(Messages.BAD_PRICE, "EVENT_NOT_FOUND", "error"));
    regularSelectionOperationHandler.internalAddSelection(sessionMock, request);
    verify(siteServerServiceMock).getEventToOutcomeForOutcome(Mockito.any());
  }

  @Test
  void testHandleErrorReadingOutcomeDate() {
    regularSelectionOperationHandler.handleErrorReadingOutcomeDate(new Throwable(), sessionMock);
    verify(sessionMock).sendData(Mockito.any(), Mockito.any());
  }

  @Test
  void testAddSelection_Exception() {
    RegularSelectionRequest regularSelectionRequest = new RegularSelectionRequest();
    regularSelectionRequest.setSelectionType("simple");
    regularSelectionRequest.setOutcomeIds(Arrays.asList(463512829L, 463512480L));
    regularSelectionRequest.setSelectionType(SCORECAST_SELECTION_TYPE);
    regularSelectionRequest.setAdditional(
        new RegularSelectionRequest.AdditionalParameters() {
          {
            setScorecastMarketId(119576981L);
          }
        });
    doThrow(new RuntimeException()).when(sessionMock).save();
    regularSelectionOperationHandler.addSelection(sessionMock, regularSelectionRequest);
    verify(sessionMock, times(1)).save();
  }

  @Test
  void verifyLuckyDipWithDrillDownTagNameNALadsTest() {
    RegularSelectionRequest request = createSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(463959176L));

    Event event =
        TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent2.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(any()))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"LB_TST0"});

    regularSelectionOperationHandler.addSelection(sessionMock, request);
    Assertions.assertEquals("16", event.getCategoryId());
  }

  @Test
  void verifyLuckyDipTestWithDrillDownTagNameNACoralTest() {
    RegularSelectionRequest request = createSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(463959176L));

    Event event =
        TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent2.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(any()))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"CR_TST0"});

    regularSelectionOperationHandler.addSelection(sessionMock, request);
    Assertions.assertEquals("FOOTBALL", event.getCategoryCode());
  }

  @Test
  void verifyLuckyDipTestWithDrillDownTagNameCorrectLads() {
    RegularSelectionRequest request = createSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(463959176L));

    Event event1 =
        TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(any()))
        .thenReturn(Optional.of(Collections.singletonList(event1)));
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"LB_TST0"});

    regularSelectionOperationHandler.addSelection(sessionMock, request);
    Assertions.assertEquals("FOOTBALL", event1.getCategoryCode());
  }

  @Test
  void verifyLuckyDipTestWithDrillDownTagNameNotCorrectLads() {
    RegularSelectionRequest request = createSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(463959176L));

    Event event1 =
        TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent3.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(any()))
        .thenReturn(Optional.of(Collections.singletonList(event1)));
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"LB_TST0"});

    regularSelectionOperationHandler.addSelection(sessionMock, request);
    Assertions.assertEquals("FOOTBALL", event1.getCategoryCode());
  }

  @Test
  void verifyLuckyDipTestWithDrillDownTagNameNotCorrectCoral() {
    RegularSelectionRequest request = createSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(463959176L));

    Event event1 =
        TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent3.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(any()))
        .thenReturn(Optional.of(Collections.singletonList(event1)));
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"CR_TST0"});

    regularSelectionOperationHandler.addSelection(sessionMock, request);
    Assertions.assertNotNull(regularSelectionOperationHandler);
  }

  @Test
  void verifyLuckyDipTstWithWhenEventSortCodeNA() {
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(463959176L));
    request.setSelectionType(RegularSelectionRequest.SIMPLE_SELECTION_TYPE);

    Event event =
        TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent4.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(any()))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"CR_TST0"});

    regularSelectionOperationHandler.addSelection(sessionMock, request);
    Assertions.assertNotNull(regularSelectionOperationHandler);
  }

  @Test
  void verifyLuckyDipTestWithWhenEventSortCodeNotCorrect() {
    RegularSelectionRequest request = createSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(463959176L));

    Event event =
        TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent5.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(any()))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"CR_TST0"});

    regularSelectionOperationHandler.addSelection(sessionMock, request);
    Assertions.assertEquals("16", event.getCategoryId());
  }

  @Test
  void verifyLuckyDipTestWithWhenOutcomesNA() throws Exception {
    Method method =
        RegularSelectionOperationHandler.class.getDeclaredMethod(
            "isLuckyDipDummySelection", Market.class);
    method.setAccessible(true);
    Event event =
        TestUtils.deserializeWithJackson(
            "impl/LuckyDipService/testEventWhenOutcomeEmpty.json", Event.class);
    assertThatExceptionOfType(InvocationTargetException.class)
        .isThrownBy(
            () ->
                method.invoke(
                    regularSelectionOperationHandler,
                    Objects.requireNonNull(event).getMarkets().get(0)));
  }

  @Test
  void verifyLuckyDipWithWhenOutcomesIsDisplayedNull() {
    RegularSelectionRequest request = createSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(463959176L));

    Event event =
        TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent6.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(any()))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"CR_TST0"});

    regularSelectionOperationHandler.addSelection(sessionMock, request);
    Assertions.assertNotNull(regularSelectionOperationHandler);
  }

  @Test
  void verifyLuckyDipTestWithWhenOutcomesIsDisplayedFalse() {
    RegularSelectionRequest request = createSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(463959177L));

    Event event =
        TestUtils.deserializeWithJackson(
            "impl/LuckyDipService/testEventWhenOutcomeNotActiveAndNotDisplayed.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(any()))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"CR_TST0"});

    regularSelectionOperationHandler.addSelection(sessionMock, request);
    Assertions.assertNotNull(request.getOutcomeIds());
  }

  @Test
  void verifyLuckyDipTestWhenOutcomesIsDisplayed() {
    RegularSelectionRequest request = createSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(463959177L));

    Event event =
        TestUtils.deserializeWithJackson(
            "impl/LuckyDipService/testEventWhenOutcomeActiveAndDisplayed.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(any()))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    when(this.environment.getActiveProfiles()).thenReturn(new String[] {"CR_TST0"});

    regularSelectionOperationHandler.addSelection(sessionMock, request);
    Assertions.assertNotNull(regularSelectionOperationHandler);
  }

  private RegularSelectionRequest createSelectionRequest() {
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setSelectionType(RegularSelectionRequest.SIMPLE_SELECTION_TYPE);
    request.setOddsBoost(true);
    return request;
  }

  @ParameterizedTest
  @CsvSource({
    "460826676,4dsgumo7d4zupm2ugsvm4zm4d,impl/fixedBetOperations/simple_selection_event.json",
    "460826676,4dsgumo7d4zupm2ugsvm4zm4d,impl/fixedBetOperations/simple_selection_event_teamid.json",
    "460826676,4dsgumo7d4zupm2ugsvm4zm4r,impl/fixedBetOperations/simple_selection_event_teamid.json",
    "460826676,4dsgumo7d4zupm2ugsvm4zm4d,impl/fixedBetOperations/simple_selection_event_teamid_nomarket.json",
    "460826676,4dsgumo7d4zupm2ugsvm4zm4d,impl/fixedBetOperations/simple_selection_event_teamid_outright_market.json",
    "460826676,4dsgumo7d4zupm2ugsvm4zm4d,impl/fixedBetOperations/simple_selection_event_teamid_null.json",
  })
  void addSelectionSimpleFanzoneSelectionTest(String outcomeId, String teamId, String path) {
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(Long.valueOf(outcomeId)));
    request.setFanzoneTeamId(teamId);
    request.setSelectionType(RegularSelectionRequest.SIMPLE_SELECTION_TYPE);
    request.setToken("dfsdfsfdsf");
    Event event = TestUtils.deserializeWithGson(path, Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(
            Collections.singletonList(Long.valueOf(outcomeId))))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    BuildBetResponse buildBetResponse =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/buildBetResponse.json", BuildBetResponse.class);
    regularSelectionOperationHandler.addSelection(sessionMock, request);
    Assertions.assertNotNull(request);
  }

  @ParameterizedTest
  @CsvSource({
    "460826676,impl/fixedBetOperations/simple_selection_event_teamid.json",
    "460826676,impl/fixedBetOperations/simple_selection_event_teamid_nomarket.json",
    "460826676,impl/fixedBetOperations/simple_selection_event_teamid_outright_market.json"
  })
  void addSelectionSimpleFanzoneSelectionLoggedOutTest(String outcomeId, String path) {
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(Long.valueOf(outcomeId)));
    // request.setFanzoneTeamId(teamId);
    request.setSelectionType(RegularSelectionRequest.SIMPLE_SELECTION_TYPE);
    request.setToken("dfsdfsfdsf");
    Event event = TestUtils.deserializeWithGson(path, Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(
            Collections.singletonList(Long.valueOf(outcomeId))))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    BuildBetResponse buildBetResponse =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/buildBetResponse.json", BuildBetResponse.class);
    regularSelectionOperationHandler.addSelection(sessionMock, request);
    Assertions.assertNotNull(request);
  }

  @Test
  void addSelectionSimpleFanzoneSelectionWithTeamIdnullTest() {
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(Collections.singletonList(460826676L));
    request.setFanzoneTeamId("4dsgumo7d4zupm2ugsvm4zm4r");
    request.setSelectionType(RegularSelectionRequest.SIMPLE_SELECTION_TYPE);
    request.setToken("dfsdfsfdsf");

    Event event =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/simple_selection_event_teamid_null.json", Event.class);
    when(siteServerServiceMock.getEventToOutcomeForOutcome(Collections.singletonList(460826676L)))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    when(siteServerServiceMock.getEventToOutcomeForOutcome(Collections.singletonList(460826676L)))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    BuildBetResponse buildBetResponse =
        TestUtils.deserializeWithGson(
            "impl/fixedBetOperations/buildBetResponse.json", BuildBetResponse.class);

    regularSelectionOperationHandler.addSelection(sessionMock, request);
    Assertions.assertNotNull(request);
  }
}
