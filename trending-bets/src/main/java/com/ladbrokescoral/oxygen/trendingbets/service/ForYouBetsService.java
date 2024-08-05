package com.ladbrokescoral.oxygen.trendingbets.service;

import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetSession;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.dto.PersonalizedBets;
import com.ladbrokescoral.oxygen.trendingbets.dto.TrendingItem;
import com.ladbrokescoral.oxygen.trendingbets.model.PersonalizedBetsDto;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingPosition;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.PersonalizedBetsSiteServImpl;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicReference;
import java.util.function.Function;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;
import reactor.core.publisher.SynchronousSink;

@Service
@Slf4j
public class ForYouBetsService extends PersonalizedBetsService {

  private static final String DEFAULT_CHANNEL = "football_tb_48h_48h";

  private static final String PERSONALIZED = "personalized";

  private final ADAService adaService;

  @Autowired
  public ForYouBetsService(
      LiveUpdatesService liveUpdatesService,
      PersonalizedBetsSiteServImpl siteServeService,
      ADAService adaService,
      @Value("${foryou.filter.market.drilldownTagNames}") String[] filterMarketDrilldownTagNames,
      @Value("${foryou.filter.event.drilldownTagNames}") String[] filterEventDrilldownTagNames) {
    super(
        liveUpdatesService,
        siteServeService,
        filterMarketDrilldownTagNames,
        filterEventDrilldownTagNames);
    this.adaService = adaService;
  }

  public Mono<PersonalizedBetsDto> processTrendingBets(String userName) {

    AtomicReference<TrendingBetSession> trendingBetsession = new AtomicReference<>();
    return adaService
        .getForYouTrendingBets(frontend + "_" + userName)
        .handle(
            (PersonalizedBets personalizedBets, SynchronousSink<Mono<List<TrendingItem>>> sink) -> {
              try {
                trendingBetsession.set(
                    new TrendingBetSession(
                        liveUpdatesService, null, personalizedBets.getLastUpdate(), getBetType()));
                trendingBetsession
                    .get()
                    .setNewUser(
                        !PERSONALIZED.equalsIgnoreCase(personalizedBets.getUserRecordsType()));
                sink.next(
                    siteServeService.getEventToOutcomeForOutcome(
                        personalizedBets.getPersonalizedRecords()));
              } catch (Exception ex) {
                sink.error(ex);
              }
            })
        .flatMap(Function.identity())
        .map(this::enhanceTrendingBets)
        .doOnNext(items -> updatePersonalizedBetsPositions(trendingBetsession.get(), items))
        .map(events -> trendingBetsession.get())
        .doOnNext(TrendingBetSession::subscribeToLiveServer)
        .map(TrendingBetSession::buildTrendingBets);
  }

  private void updatePersonalizedBetsPositions(
      TrendingBetSession session, List<TrendingItem> items) {
    if (session.isNewUser()) {
      Optional.ofNullable(TrendingBetsContext.getTrendingBets().get(DEFAULT_CHANNEL))
          .ifPresent(
              trendingBetsDto -> session.getPositions().addAll(trendingBetsDto.getPositions()));

    } else {
      items.forEach(
          (TrendingItem item) -> {
            TrendingPosition position = populateTrendingPosition(item);
            session.getPositions().add(position);
            session.getNewSelections().add(position.getEvent());
          });
    }
  }
}
