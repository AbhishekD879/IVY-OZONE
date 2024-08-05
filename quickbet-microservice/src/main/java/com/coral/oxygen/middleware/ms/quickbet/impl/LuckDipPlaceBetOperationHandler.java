package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.*;
import static java.util.stream.Collectors.toList;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.LuckyDipBetPlacementRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.util.ResponseUtils;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import java.text.MessageFormat;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class LuckDipPlaceBetOperationHandler {

  private final LuckDipService luckDipService;
  private final SiteServerService siteServerService;
  private final LuckDipRNGService luckDipRngService;
  private final Environment environment;

  public LuckDipPlaceBetOperationHandler(
      LuckDipService luckDipService,
      SiteServerService siteServerService,
      LuckDipRNGService luckDipRngService,
      Environment environment) {
    this.luckDipService = luckDipService;
    this.siteServerService = siteServerService;
    this.luckDipRngService = luckDipRngService;
    this.environment = environment;
  }

  public void processLuckyDipPlaceBet(Session session, LuckyDipBetPlacementRequest request) {
    try {
      log.info("LuckyDip Input {}", request);
      Optional<List<Event>> events =
          siteServerService.getEventToOutcomeForMarketForLuckyDip(request.getMarketId());
      if (events.isPresent()) {
        Event event = luckDipService.findFirst(events.get());
        processLuckyDipEvent(session, request, event);
      } else {
        throw new SiteServException(
            SITESERV_ERROR,
            SITESERV_ERROR.code(),
            "Site Server is Down , please try after sometime ");
      }
    } catch (SiteServException e) {
      log.error("Error lucky Dip place bet {}", e.getDesc());
      ResponseUtils.sendSiteServerException(session, e);
    } catch (Exception e) {
      log.error("Error lucky Dip bet {}", e.getMessage());
      session.sendData(
          PLACE_BET_ERROR_RESPONSE_CODE.code(),
          RegularPlaceBetResponse.errorResponse(
              INTERNAL_PLACE_BET_PROCESSING.code(), e.getMessage()));
    }
  }

  private void processLuckyDipEvent(
      Session session, LuckyDipBetPlacementRequest request, Event event) {
    if (Objects.nonNull(event)) {
      Market market = findLuckyDipMarket(event.getMarkets(), request.getMarketId());
      if (Objects.nonNull(market)) {
        if ("A".equalsIgnoreCase(market.getMarketStatusCode())) {
          processLuckyDip(session, event, market, request);
        } else {
          throw new SiteServException(
              MARKET_SUSPENDED,
              MARKET_SUSPENDED.code(),
              MessageFormat.format(" Lucky Dip Market Suspended : {0} ", request.getMarketId()));
        }
      } else {
        throw new SiteServException(
            MARKET_NOT_FOUND,
            MARKET_NOT_FOUND.code(),
            MessageFormat.format(" Lucky Dip Market Not found : {0} ", request.getMarketId()));
      }
    } else {
      throw new SiteServException(
          MARKET_NOT_FOUND,
          MARKET_NOT_FOUND.code(),
          MessageFormat.format(" Market Id Not found : {0} ", request.getMarketId()));
    }
  }

  private void processLuckyDip(
      Session session, Event event, Market market, LuckyDipBetPlacementRequest request) {
    if (isLuckyDipMarket(event, market)) {
      Outcome allottedPlayer = processPlayerAllotment(market);
      luckDipService.processLuckyDipPlaceBet(session, allottedPlayer, request);
    } else {
      throw new SiteServException(
          INVALID_MARKET,
          INVALID_MARKET.code(),
          MessageFormat.format(
              " Invalid Lucky Dip Market Id : {0} and its now allowed for LuckyDip",
              request.getMarketId()));
    }
  }

  private Market findLuckyDipMarket(List<Market> list, String marketId) {
    return list.stream()
        .filter(Objects::nonNull)
        .filter(market -> marketId.equals(market.getId()))
        .findFirst()
        .orElse(null);
  }

  private boolean isLuckyDipMarket(Event event, Market market) {
    if (Arrays.stream(this.environment.getActiveProfiles()).anyMatch(s -> s.startsWith("LB"))) {
      return StringUtils.isNotBlank(market.getDrilldownTagNames())
          && market.getDrilldownTagNames().contains("MKTFLAG_LD");
    } else {
      return StringUtils.isNotBlank(market.getDrilldownTagNames())
          && market.getDrilldownTagNames().contains("MKTFLAG_LD")
          && StringUtils.isNotBlank(event.getEventSortCode())
          && "TNMT".equals(event.getEventSortCode());
    }
  }

  private Outcome processPlayerAllotment(Market market) {
    List<Outcome> outcomes = market.getOutcomes();
    List<Outcome> activeOutcomes = fetchActiveSelections(outcomes);
    Outcome player = activeOutcomes.get(luckDipRngService.getRandomNumber(activeOutcomes.size()));
    log.info("Allotted Player : {}", player.getName());
    return player;
  }

  private List<Outcome> fetchActiveSelections(List<Outcome> outcomes) {
    return outcomes.stream()
        .filter(
            outcome ->
                Objects.nonNull(outcome.getOutcomeStatusCode())
                    && "A".equalsIgnoreCase(outcome.getOutcomeStatusCode()))
        .filter(outcome -> Objects.isNull(outcome.getIsDisplayed()))
        .collect(toList());
  }
}
