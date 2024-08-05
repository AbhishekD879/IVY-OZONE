package com.coral.oxygen.middleware.in_play.service;

import static com.coral.oxygen.middleware.pojos.model.output.MarketTemplateType.*;

import com.coral.oxygen.middleware.common.service.MarketTemplateNameService;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.MarketTemplateType;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayModel;
import com.egalacoral.spark.liveserver.Subscriber;
import com.egalacoral.spark.liveserver.service.LiveServerSubscriber;
import com.egalacoral.spark.liveserver.service.LiveServerSubscriptionsQAStorage;
import java.util.*;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

/**
 * Subscribes on events/markets/outcomes found in #{@link InPlayModel}. Not all markets/outcomes are
 * shown on InPlay, that's why it's needed to filter them before subscription. That's because
 * #{@link InPlayModel} events can contain all possible markets (Live Now Football, for example).
 */
@Service
@Slf4j
public class InplayLiveServerSubscriber {
  private final Subscriber liveServerClient;
  private final LiveServerSubscriptionsQAStorage lsQAStorage;
  private final LiveServerSubscriber liveServerSubscriber;
  private final MarketTemplateNameService marketTemplateNameService;

  private static final EnumSet<MarketTemplateType> SUPPORTED_MARKETS =
      EnumSet.of(
          MATCH_BETTING,
          MATCH_RESULT,
          FIRST_HALF_RESULT,
          TOTAL_GOALS_OVER_UNDER,
          TO_QUALIFY,
          DRAW_NO_BET,
          BOTH_TEAMS_TO_SCORE,
          MATCH_RESULT_AND_BOTH_TEAMS_TO_SCORE,
          PENALTY_SO_WINNER,
          EXTRA_TIME_RESULT);

  /** Describes what markets we should subscribe to - all markets that can be shown on InPlay */
  private final List<Predicate<OutputMarket>> marketsToSubscribePredicates;

  private List<String> sportsNeedliveupdatesForNonprimaryMarkets;
  private List<String> nonPrimaryMarketsForLiveUpdates;

  @Autowired
  // todo move subscriber and hz to other place
  public InplayLiveServerSubscriber(
      Subscriber liveServerClient,
      LiveServerSubscriptionsQAStorage lsQAStorage,
      LiveServerSubscriber liveServerSubscriber,
      MarketTemplateNameService marketTemplateNameService,
      @Value("${sports.category.liveupdates.nonprimary.markets}")
          String[] sportsNeedSubForNonprimaryMarkets,
      @Value("${market.template.marketsNeedSubscriptionForLiveUpdates}")
          String[] marketsNeedSubscriptionForLiveUpdates) {
    this.liveServerClient = liveServerClient;
    this.liveServerSubscriber = liveServerSubscriber;
    this.lsQAStorage = lsQAStorage;
    this.marketTemplateNameService = marketTemplateNameService;

    List<String> supportedMarketNames =
        Arrays.asList(marketTemplateNameService.getNames(SUPPORTED_MARKETS));
    marketsToSubscribePredicates =
        Arrays.asList(
            m -> marketTemplateNameService.containsName(OUTRIGHT, m.getTemplateMarketName()),
            m -> supportedMarketNames.contains(m.getName()));

    sportsNeedliveupdatesForNonprimaryMarkets =
        sportsNeedSubForNonprimaryMarkets != null
            ? Arrays.asList(sportsNeedSubForNonprimaryMarkets)
            : new ArrayList<>();

    nonPrimaryMarketsForLiveUpdates =
        marketsNeedSubscriptionForLiveUpdates != null
            ? Arrays.asList(marketsNeedSubscriptionForLiveUpdates)
            : new ArrayList<>();
  }

  public void subscribe(InPlayModel model) {
    toModuleDataItemList(model).forEach(liveServerSubscriber::subscribe);

    lsQAStorage.storeActiveLiveServePayload(liveServerClient.getPayloadItems());
  }

  private Set<LiveServerSubscriber.EventSubscribeInfo> toModuleDataItemList(InPlayModel model) {
    return model.getSportEvents().stream()
        .flatMap(sportSegment -> sportSegment.getEventsByTypeName().stream())
        .flatMap(typeSegment -> typeSegment.getEvents().stream())
        .map(this::toSubscribeInfo)
        .collect(Collectors.toSet());
  }

  private LiveServerSubscriber.EventSubscribeInfo toSubscribeInfo(EventsModuleData moduleDataItem) {
    List<OutputMarket> filteredMarkets = filterMarkets(moduleDataItem);

    return LiveServerSubscriber.EventSubscribeInfo.builder()
        .categoryId(Integer.parseInt(moduleDataItem.getCategoryId()))
        .id(moduleDataItem.getId().toString())
        .markets(filteredMarkets.stream().map(OutputMarket::getId).collect(Collectors.toSet()))
        .outcomes(extractOutcomes(filteredMarkets))
        .build();
  }

  // subscribes on primary market + markets from inplay selector
  private List<OutputMarket> filterMarkets(EventsModuleData moduleDataItem) {
    List<OutputMarket> filteredMarkets = new ArrayList<>(moduleDataItem.getPrimaryMarkets());

    List<OutputMarket> markets = new ArrayList<>(moduleDataItem.getMarkets());
    markets.sort(
        Comparator.comparing(
                OutputMarket::getDisplayOrder, Comparator.nullsLast(Comparator.naturalOrder()))
            .thenComparing(OutputMarket::getName, Comparator.nullsLast(Comparator.naturalOrder())));

    boolean nextTeamToScoreMarketAlreadyIn = false;
    for (OutputMarket market : markets) {

      boolean isNextTeamToScore = isNextTeamToScore(market);
      if (!nextTeamToScoreMarketAlreadyIn && isNextTeamToScore) {
        filteredMarkets.add(market);
        nextTeamToScoreMarketAlreadyIn = true;
        logSubscribedToMarket(market);
        continue;
      } else if (isNextTeamToScore) {
        logNotSubscribedToMarket(market);
        continue;
      }

      for (Predicate<OutputMarket> predicate : marketsToSubscribePredicates) {
        if (predicate.test(market)) {
          filteredMarkets.add(market);
          logSubscribedToMarket(market);
          break;
        } else {
          logNotSubscribedToMarket(market);
        }
      }
      if (sportsNeedliveupdatesForNonprimaryMarkets.contains(moduleDataItem.getCategoryId())
          && nonPrimaryMarketsForLiveUpdates.contains(market.getTemplateMarketName())
          && moduleDataItem.getEventIsLive()) {
        filteredMarkets.add(market);
        logSubscribedToMarket(market);
      }
    }

    return filteredMarkets;
  }

  private void logNotSubscribedToMarket(OutputMarket market) {
    log.debug(
        "Not subscribing to {} [{}] with id {}",
        market.getName(),
        market.getTemplateMarketName(),
        market.getId());
  }

  private void logSubscribedToMarket(OutputMarket market) {
    log.debug(
        "Will subscribe to {} [{}] with id {}",
        market.getName(),
        market.getTemplateMarketName(),
        market.getId());
  }

  private boolean isNextTeamToScore(OutputMarket market) {
    return marketTemplateNameService.containsName(
        NEXT_TEAM_TO_SCORE, market.getTemplateMarketName());
  }

  private Set<String> extractOutcomes(List<OutputMarket> outputMarkets) {
    return outputMarkets.stream()
        // No point to subscribe on outright market's outcomes since they aren't being shown on
        // InPlay UI
        .filter(
            market ->
                !marketTemplateNameService.containsName(OUTRIGHT, market.getTemplateMarketName()))
        .flatMap(m -> m.getOutcomes().stream())
        .map(OutputOutcome::getId)
        .collect(Collectors.toSet());
  }
}
