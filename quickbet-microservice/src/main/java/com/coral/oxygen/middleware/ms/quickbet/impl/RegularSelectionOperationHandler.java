package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.*;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequestValidator;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RequestValidationException;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputEvent;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputMarket;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputOutcome;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputPrice;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2.OddsBoostToken;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2.RegularSelectionResponse;
import com.coral.oxygen.middleware.ms.quickbet.converter.EventToOutputEventConverter;
import com.coral.oxygen.middleware.ms.quickbet.converter.PriceToOutputPriceConverter;
import com.coral.oxygen.middleware.ms.quickbet.converter.RegularSelectionResponseToBuildBetDtoConverter;
import com.egalacoral.spark.siteserver.model.*;
import com.egalacoral.spark.siteserver.model.Price;
import com.entain.oxygen.bettingapi.exception.BettingConnectionException;
import com.entain.oxygen.bettingapi.model.bet.api.response.*;
import com.entain.oxygen.bettingapi.service.BettingService;
import com.newrelic.api.agent.NewRelic;
import java.util.*;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.lang3.StringUtils;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

@Component
public class RegularSelectionOperationHandler {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  public static final String SINGLE_BET_TYPE = "SGL";
  private static final String INTERNAL_ERROR = "Internal error";
  private static final String ERROR_READING_OUTCOME_DATA = "Error reading outcome data.";

  private final SiteServerService siteServerService;
  private final LiveServService liveServService;
  private final BettingService bettingService;
  private final EventToOutputEventConverter eventConverter;
  private final PriceToOutputPriceConverter priceConverter;
  private final RegularSelectionResponseToBuildBetDtoConverter buildBetDtoConverter;
  private final ScorecastPriceService scorecastPriceService;
  private final RegularFanzoneSelectionHandler regularFanzoneSelectionHandler;

  private final Environment environment;

  public RegularSelectionOperationHandler(
      SiteServerService siteServerService,
      LiveServService liveServService,
      BettingService bettingService,
      EventToOutputEventConverter eventConverter,
      PriceToOutputPriceConverter priceConverter,
      RegularSelectionResponseToBuildBetDtoConverter buildBetDtoConverter,
      ScorecastPriceService scorecastPriceService,
      RegularFanzoneSelectionHandler regularFanzoneSelctionHandler,
      Environment environment) {
    this.siteServerService = siteServerService;
    this.liveServService = liveServService;
    this.bettingService = bettingService;
    this.eventConverter = eventConverter;
    this.priceConverter = priceConverter;
    this.buildBetDtoConverter = buildBetDtoConverter;
    this.scorecastPriceService = scorecastPriceService;
    this.regularFanzoneSelectionHandler = regularFanzoneSelctionHandler;
    this.environment = environment;
  }

  public void restoreState(Session session) {
    if (session.getRegularSelectionRequest() != null) {
      internalAddSelection(session, session.getRegularSelectionRequest());
    }
  }

  public void addSelection(Session session, RegularSelectionRequest request) {
    try {
      RegularSelectionRequestValidator validator = new RegularSelectionRequestValidator();
      validator.validate(request);
      session.setRegularSelectionRequest(request);
      session.save();
      internalAddSelection(session, request);
    } catch (RequestValidationException e) {
      NewRelic.noticeError(e);
      ASYNC_LOGGER.error("Invalid request", e);
      session.sendData(
          REGULAR_OUTCOME_RESPONSE_ERROR_CODE.code(),
          RegularPlaceBetResponse.errorResponse("INVALID_REQUEST", e.getMessage()));
    } catch (Exception e) {
      NewRelic.noticeError(e);
      ASYNC_LOGGER.error(INTERNAL_ERROR, e);
      session.sendData(
          REGULAR_OUTCOME_RESPONSE_ERROR_CODE.code(),
          RegularPlaceBetResponse.errorResponse("INTERNAL_ERROR", e.getMessage()));
    }
  }

  private void processSimpleSelection(
      Session session, RegularSelectionRequest request, Event event) {

    List<String> channels = calculateLiveServChannels(event);
    long eventId = Long.parseLong(event.getId());
    channels.forEach(ch -> liveServService.subscribe(ch, eventId));
    RegularSelectionResponse response = buildRegularSelectionResponse(event, request);
    setSessionWithBuildbet(session, channels, response, request.isOddsBoost());
  }

  public boolean isActive(RegularSelectionResponse response) {
    OutputEvent event = response != null ? response.getEvent() : null;
    List<OutputMarket> markets = event != null ? event.getMarkets() : Collections.emptyList();
    List<OutputOutcome> outcomes = markets.stream().flatMap(m -> m.getOutcomes().stream()).toList();
    if (event == null || markets.isEmpty() || outcomes.isEmpty()) {
      return false;
    }

    Predicate<String> statusPredicate = "A"::equalsIgnoreCase;
    return statusPredicate.test(event.getEventStatusCode())
        && markets.stream().map(OutputMarket::getMarketStatusCode).allMatch(statusPredicate)
        && outcomes.stream().map(OutputOutcome::getOutcomeStatusCode).anyMatch(statusPredicate);
  }

  private void setSessionWithBuildbet(
      Session session,
      List<String> channels,
      RegularSelectionResponse response,
      boolean isOddsBoost) {
    try {
      final BuildBetResponse buildBetResponse =
          handleBuildBet(
              bettingService.buildBet(
                  response.getRequest().getToken(), buildBetDtoConverter.convert(response)));

      response.setMaxPayout(buildBetResponse.getBets().get(0).getMaxPayout());
      List<Freebet> freebets =
          Optional.ofNullable(buildBetResponse.getBets().get(0).getFreebet())
              .orElse(Collections.emptyList());
      if (isValidResponse(response, isOddsBoost)) {
        setSessionForOddsBoost(freebets, response);
      }
      setSessionForRegularFreebets(freebets, session, channels, response);
    } catch (BettingException e) {
      if ("OUTCOME_SUSPENDED".equals(e.getResponse().getData().getError().getSubErrorCode())) {
        setSession(session, channels, response);
      } else {
        handleBettingException(e, session);
      }
    } catch (BettingConnectionException e) {
      handleBettingConnectionException(e, session);
    } catch (Exception e) {
      handleErrorReadingOutcomeDate(e, session);
    }
  }

  public boolean isValidResponse(RegularSelectionResponse response, boolean isOddsBoost) {
    return isOddsBoost && response.getSelectionPrice() != null && isActive(response);
  }

  private void setSessionForOddsBoost(List<Freebet> freebets, RegularSelectionResponse response) {
    freebets.stream()
        .filter(freebet -> "BETBOOST".equals(freebet.getType()))
        .max(
            Comparator.comparing(
                freebet ->
                    typeToInt(freebet.getFreebetOfferType()))) // what freebet should be chosen?
        .map(this::convertToOddsBoostToken)
        .ifPresent(response::setOddsBoost);
  }

  private void setSessionForRegularFreebets(
      List<Freebet> freebets,
      Session session,
      List<String> channels,
      RegularSelectionResponse response) {
    response.setFreebetList(
        freebets.stream().filter((Freebet freebet) -> "SPORTS".equals(freebet.getType())).toList());
    setSession(session, channels, response);
  }

  private void handleBettingConnectionException(BettingConnectionException e, Session session) {
    NewRelic.noticeError(e);
    ASYNC_LOGGER.error(INTERNAL_ERROR, e);
    sendSiteServerException(
        session,
        new SiteServException(
            REGULAR_OUTCOME_RESPONSE_ERROR_CODE, BETTING_ERROR.code(), "Betting Connection Error"));
  }

  private Void handleBettingException(BettingException bettingException, Session session) {
    NewRelic.noticeError(bettingException);
    ASYNC_LOGGER.error(INTERNAL_ERROR, bettingException);
    session.sendData(bettingException.getMsg().code(), bettingException.getResponse());
    return null;
  }

  private void setSession(
      Session session, List<String> channels, RegularSelectionResponse response) {
    session.setRegularSelectionResponse(response);
    session.sendData(
        REGULAR_OUTCOME_RESPONSE_CODE.code(),
        new com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2.GeneralResponse<>(
            response));
    session.subscribeToRooms(channels);
  }

  private int typeToInt(String type) {
    if (SINGLE_BET_TYPE.equalsIgnoreCase(type)) {
      return 1;
    } else if ("ANY".equalsIgnoreCase(type)) {
      return 0;
    } else {
      return -1;
    }
  }

  private OddsBoostToken convertToOddsBoostToken(Freebet freebet) {
    OddsBoostToken oddsBoostToken = new OddsBoostToken();
    oddsBoostToken.setId(freebet.getId());
    oddsBoostToken.setEnhancedOddsPrice(freebet.getEnhancedOddsPrice());
    oddsBoostToken.setEnhancedOddsPriceDen(freebet.getEnhancedOddsPriceDen());
    oddsBoostToken.setEnhancedOddsPriceNum(freebet.getEnhancedOddsPriceNum());
    oddsBoostToken.setBetBoostMaxStake(freebet.getBetBoostMaxStake());
    oddsBoostToken.setBetBoostMinStake(freebet.getBetBoostMinStake());
    return oddsBoostToken;
  }

  private BuildBetResponse handleBuildBet(GeneralResponse<BuildBetResponse> generalResponse) {
    if (generalResponse.getErrorBody() != null) {
      throw new BettingException(
          REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
          generalResponse.getErrorBody().getStatus(),
          generalResponse.getErrorBody().getError());
    } else {
      BuildBetResponse body = generalResponse.getBody();
      BetErrors betError =
          !CollectionUtils.isEmpty(body.getBets()) ? body.getBets().get(0).getBetErrors() : null;
      if (betError != null) {
        throw new BettingException(
            REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
            betError.getCode(),
            betError.getSubErrorCode(),
            betError.getErrorDesc());
      } else {
        return body;
      }
    }
  }

  private void processScorecastSelection(
      Session session, RegularSelectionRequest request, Event event) {
    OutputPrice scorecastPrice = getScorecastPrice(request, event);
    RegularSelectionResponse response =
        buildRegularSelectionResponse(event, request, scorecastPrice);
    setSessionWithBuildbet(session, Collections.emptyList(), response, false);
  }

  private OutputPrice getScorecastPrice(RegularSelectionRequest request, Event event) {
    Market correctSoreMarket = getCorrectScoreMarket(event);
    Market goalScorerMarket = getGoalScorerMarket(event);

    return scorecastPriceService
        .calculate(
            getPriceDec(correctSoreMarket),
            getPriceDec(goalScorerMarket),
            ScorecastPriceService.ScorecastType.generate(
                getCorrectScoreHome(correctSoreMarket),
                getCorrectScoreAway(correctSoreMarket),
                getFsResult(goalScorerMarket)))
        .orElseGet(() -> getOutputPriceFromService(request));
  }

  private OutputPrice getOutputPriceFromService(RegularSelectionRequest request) {
    String marketId = String.valueOf(request.getAdditional().getScorecastMarketId());
    String scorerOutcomeId = String.valueOf(request.getOutcomeIds().get(0));
    Scorecast scorecast =
        siteServerService
            .getScorecast(marketId, scorerOutcomeId)
            .orElseThrow(
                () ->
                    new SiteServException(
                        REGULAR_OUTCOME_RESPONSE_CODE,
                        SCORECAST_NOT_FOUND.code(),
                        "Error during loading scorecast. Scorecast not found"));
    final String scoreOutcomeString = " and scorerOutcome ";
    String pricesStr = scorecast.getScorecastPrices();
    if (Objects.isNull(pricesStr)) {
      throw new SiteServException(
          REGULAR_OUTCOME_RESPONSE_CODE,
          PRICES_NOT_FOUND.code(),
          "Prices not found in scorecast for market "
              + marketId
              + scoreOutcomeString
              + scorerOutcomeId);
    }
    String[] split = pricesStr.split(",");
    String scoreOutcomeId = String.valueOf(request.getOutcomeIds().get(1));
    OutputPrice outputPrice = null;
    for (int i = 0; i < split.length; i += 4) {
      String scoreOutcomeIdCandidate = split[i];
      if (scoreOutcomeId.equals(scoreOutcomeIdCandidate)) {
        outputPrice = new OutputPrice();
        try {
          outputPrice.setPriceNum(Integer.parseInt(split[i + 1]));
          outputPrice.setPriceDen(Integer.parseInt(split[i + 2]));
          outputPrice.setPriceDec(Double.parseDouble(split[i + 3]));
        } catch (Exception e) {
          NewRelic.noticeError(e);
          throw new SiteServException(
              REGULAR_OUTCOME_RESPONSE_CODE,
              PRICES_NOT_PARSED.code(),
              "Error parsing price in scorecast for market "
                  + marketId
                  + scoreOutcomeString
                  + scorerOutcomeId
                  + " and scoreOutcomeId "
                  + scoreOutcomeId);
        }
        break;
      }
    }
    return outputPrice;
  }

  private Market getCorrectScoreMarket(Event event) {
    return event.getMarkets().stream()
        .filter(market -> market.getDispSortName().equals("CS"))
        .findFirst()
        .orElseThrow(RuntimeException::new);
  }

  private Market getGoalScorerMarket(Event event) {
    return event.getMarkets().stream()
        .filter(
            market ->
                market.getDispSortName().equals("FS") || market.getDispSortName().equals("LS"))
        .findFirst()
        .orElseThrow(RuntimeException::new);
  }

  private Double getPriceDec(Market market) {
    return market.getOutcomes().get(0).getPrices().get(0).getPriceDec();
  }

  private int getCorrectScoreHome(Market market) {
    return Integer.parseInt(market.getOutcomes().get(0).getOutcomeMeaningScores().split(",")[0]);
  }

  private int getCorrectScoreAway(Market market) {
    return Integer.parseInt(market.getOutcomes().get(0).getOutcomeMeaningScores().split(",")[1]);
  }

  private String getFsResult(Market market) {
    return market.getOutcomes().get(0).getOutcomeMeaningMinorCode();
  }

  private RegularSelectionResponse buildRegularSelectionResponse(
      Event event, RegularSelectionRequest request, OutputPrice outputPrice) {
    OutputEvent outputEvent = eventConverter.convert(event);
    RegularSelectionResponse result = new RegularSelectionResponse();
    verifyLuckyDip(event, result);
    result.setEvent(outputEvent);
    result.setSelectionPrice(outputPrice);
    result.setRequest(request);
    return result;
  }

  private void verifyLuckyDip(Event event, RegularSelectionResponse result) {
    if (isLuckyDipMarket(event)) {
      result.setLDip(true);
      result.setLDipMar(event.getMarkets().get(0).getId());
    }
  }

  private RegularSelectionResponse buildRegularSelectionResponse(
      Event event, RegularSelectionRequest request) {
    List<Price> prices = event.getMarkets().get(0).getOutcomes().get(0).getPrices();
    OutputPrice outputPrice = null;
    if (Objects.nonNull(prices) && !prices.isEmpty()) {
      Price price = prices.get(0);
      outputPrice = priceConverter.convert(price);
    }
    return buildRegularSelectionResponse(event, request, outputPrice);
  }

  public void internalAddSelection(Session session, RegularSelectionRequest request) {
    try {
      List<Long> outcomeIds = request.getOutcomeIds();
      Optional<List<Event>> response;
      response = siteServerService.getEventToOutcomeForOutcome(outcomeIds);
      Event event = validateOutcomesExist(outcomeIds, response);
      // OZONE-9555 changes
      if (StringUtils.isNotBlank(request.getFanzoneTeamId())) {
        processFanzoneSelection(request, event);
      } else {
        regularFanzoneSelectionHandler.validateFanPriceOutcome(event.getMarkets().get(0));
      }
      if (RegularSelectionRequest.SIMPLE_SELECTION_TYPE.equals(request.getSelectionType())) {
        processSimpleSelection(session, request, event);
      } else if (RegularSelectionRequest.SCORECAST_SELECTION_TYPE.equals(
          request.getSelectionType())) {
        processScorecastSelection(session, request, event);
      }
    } catch (SiteServException e) {
      String code = e.getResponse().getData().getError().getCode();
      if (EVENT_NOT_FOUND.code().equals(code) || OUTCOME_NOT_FOUND.code().equals(code)) {
        ASYNC_LOGGER.warn("Event was undisplayed {}", e.getResponse());
        sendSiteServerException(session, e);
      } else {
        NewRelic.noticeError(e);
        ASYNC_LOGGER.error("Error reading outcome data.{}", e.getDesc(), e);
        sendSiteServerException(session, e);
      }
    } catch (Exception e) {
      handleErrorReadingOutcomeDate(e, session);
    }
  }

  public Void handleErrorReadingOutcomeDate(Throwable e, Session session) {
    NewRelic.noticeError(e);
    ASYNC_LOGGER.error(ERROR_READING_OUTCOME_DATA, e);
    sendSiteServerException(
        session,
        new SiteServException(
            REGULAR_OUTCOME_RESPONSE_ERROR_CODE, SITESERV_ERROR.code(), e.getMessage()));
    return null;
  }

  private void sendSiteServerException(Session session, SiteServException e) {
    session.sendData(e.getMsg().code(), e.getResponse());
  }

  // TODO: we have event here - how they know that the 1st outcome from 1st market of this event has
  // selected outcomeId?
  private List<String> calculateLiveServChannels(Event event) {
    Market market = event.getMarkets().get(0);
    Outcome outcome = market.getOutcomes().get(0);
    return LiveServChannelUtils.calculateLiveServChannels(
        outcome.getId(), event.getMarkets().get(0).getId(), event.getId());
  }

  private Event validateOutcomesExist(List<Long> outcomeIds, Optional<List<Event>> response) {
    if (!response.isPresent()) {
      throw new SiteServException(
          REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
          SITESERV_ERROR.code(),
          ERROR_READING_OUTCOME_DATA + " Siteserv is down");
    }
    if (response.get().isEmpty()) {
      throw new SiteServException(
          REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
          EVENT_NOT_FOUND.code(),
          ERROR_READING_OUTCOME_DATA + " Data not found. OutcomeIds - " + outcomeIds);
    }
    if (response.get().size() > 1) {
      throw new SiteServException(
          REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
          EVENTS_TOO_MUCH.code(),
          ERROR_READING_OUTCOME_DATA + " Too many events. OutcomeIds - " + outcomeIds);
    }
    Event event = response.get().get(0);

    Set<Long> loadedOutcomeIds =
        event.getMarkets().stream() //
            .map(Market::getOutcomes) //
            .flatMap(Collection::stream) //
            .map(Outcome::getId) //
            .map(Long::valueOf) //
            .collect(Collectors.toSet());

    Optional<Long> lostOutcomeId =
        outcomeIds.stream() //
            .filter(outcomeId -> !loadedOutcomeIds.contains(outcomeId))
            .findFirst();

    if (lostOutcomeId.isPresent()) {
      throw new SiteServException(
          REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
          OUTCOME_NOT_FOUND.code(),
          " Outcome " + lostOutcomeId + " not found");
    }
    return event;
  }

  private boolean isLuckyDipMarket(Event event) {
    Market market = event.getMarkets().get(0);
    boolean isLuckyDipMarket;
    if (Arrays.stream(this.environment.getActiveProfiles()).anyMatch(s -> s.startsWith("LB"))) {
      isLuckyDipMarket =
          StringUtils.isNotBlank(market.getDrilldownTagNames())
              && market.getDrilldownTagNames().contains("MKTFLAG_LD");
    } else {
      isLuckyDipMarket =
          StringUtils.isNotBlank(market.getDrilldownTagNames())
              && market.getDrilldownTagNames().contains("MKTFLAG_LD")
              && StringUtils.isNotBlank(event.getEventSortCode())
              && "TNMT".equals(event.getEventSortCode());
    }
    return isLuckyDipMarket && isLuckyDipDummySelection(market);
  }

  private boolean isLuckyDipDummySelection(Market market) {
    boolean isLuckyDipDummySelection =
        CollectionUtils.isNotEmpty(market.getOutcomes())
            && Objects.nonNull(market.getOutcomes().get(0).getIsDisplayed())
            && market.getOutcomes().get(0).getIsDisplayed();
    if (!isLuckyDipDummySelection) {
      ASYNC_LOGGER.info(
          "LuckyDip Event {},Market {} found and selection not found {}",
          market.getEventId(),
          market.getId(),
          market.getOutcomes().get(0));
    }
    return isLuckyDipDummySelection;
  }

  /**
   * processFanzoneSelection method will handle fanzone user selections Regular or fan price.
   *
   * @param request request object
   * @return return event
   */
  private void processFanzoneSelection(RegularSelectionRequest request, Event event) {
    Market market = event.getMarkets().get(0);
    regularFanzoneSelectionHandler.validateFanzoneMarket(request, market);
  }
}
