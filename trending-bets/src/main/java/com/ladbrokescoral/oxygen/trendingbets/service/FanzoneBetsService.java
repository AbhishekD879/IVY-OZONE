package com.ladbrokescoral.oxygen.trendingbets.service;

import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetSession;
import com.ladbrokescoral.oxygen.trendingbets.dto.PersonalizedBets;
import com.ladbrokescoral.oxygen.trendingbets.dto.TrendingItem;
import com.ladbrokescoral.oxygen.trendingbets.model.PersonalizedBetsDto;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingPosition;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.PersonalizedBetsSiteServImpl;
import java.util.Collection;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;
import reactor.core.publisher.SynchronousSink;

@Service
@Slf4j
public class FanzoneBetsService extends PersonalizedBetsService {

  private final ADAService adaService;

  @Autowired
  public FanzoneBetsService(
      LiveUpdatesService liveUpdatesService,
      PersonalizedBetsSiteServImpl siteServeService,
      ADAService adaService,
      @Value("${fanzone.filter.market.drilldownTagNames}") String[] filterMarketDrilldownTagNames,
      @Value("${fanzone.filter.event.drilldownTagNames}") String[] filterEventDrilldownTagNames) {
    super(
        liveUpdatesService,
        siteServeService,
        filterMarketDrilldownTagNames,
        filterEventDrilldownTagNames);
    this.adaService = adaService;
  }

  public Mono<PersonalizedBetsDto> processFanzoneTrendingBets(String teamId) {
    AtomicReference<TrendingBetSession> trendingBetsession = new AtomicReference<>();
    return adaService
        .getFanzoneTrendingBets(teamId)
        .handle(
            (PersonalizedBets personalizedBets, SynchronousSink<Mono<PersonalizedBets>> sink) -> {
              try {
                trendingBetsession.set(
                    new TrendingBetSession(
                        liveUpdatesService, null, personalizedBets.getLastUpdate(), getBetType()));
                List<TrendingItem> items =
                    Stream.of(
                            personalizedBets.getFanzoneYourTeam(),
                            personalizedBets.getFanzoneOtherTeam())
                        .flatMap(Collection::stream)
                        .collect(Collectors.toList());
                int totalSize = items.size();
                sink.next(
                    siteServeService
                        .getEventToOutcomeForOutcome(items)
                        .map(this::enhanceTrendingBets)
                        .flatMap(
                            (List<TrendingItem> trendingItems) -> {
                              if (totalSize != trendingItems.size()) {
                                personalizedBets.getFanzoneYourTeam().retainAll(trendingItems);
                                personalizedBets.getFanzoneOtherTeam().retainAll(trendingItems);
                              }
                              return Mono.just(personalizedBets);
                            }));
              } catch (Exception ex) {
                sink.error(ex);
              }
            })
        .flatMap(Function.identity())
        .doOnNext(personalizedBets -> updatePositions(trendingBetsession.get(), personalizedBets))
        .map(events -> trendingBetsession.get())
        .doOnNext(TrendingBetSession::subscribeToLiveServer)
        .map(TrendingBetSession::buildTrendingBets);
  }

  private void updatePositions(TrendingBetSession session, PersonalizedBets personalizedBets) {

    personalizedBets
        .getFanzoneYourTeam()
        .forEach(
            (TrendingItem item) -> {
              TrendingPosition position = populateTrendingPosition(item);
              session.getFzYourTeamPositions().add(position);
              session.getNewSelections().add(position.getEvent());
            });
    personalizedBets
        .getFanzoneOtherTeam()
        .forEach(
            (TrendingItem item) -> {
              TrendingPosition position = populateTrendingPosition(item);
              session.getFzOtherTeamPositions().add(position);
              session.getNewSelections().add(position.getEvent());
            });
  }
}
