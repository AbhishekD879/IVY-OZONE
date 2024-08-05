package com.ladbrokescoral.oxygen.trendingbets.service;

import static org.junit.Assert.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.dto.PersonalizedBets;
import com.ladbrokescoral.oxygen.trendingbets.dto.TrendingItem;
import com.ladbrokescoral.oxygen.trendingbets.model.*;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.PersonalizedBetsSiteServImpl;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.SiteServeService;
import com.ladbrokescoral.oxygen.trendingbets.utils.TestUtils;
import java.util.HashSet;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@SpringBootTest
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
@ActiveProfiles("TEST")
class FanzoneBetsServiceTest {

  @InjectMocks private FanzoneBetsService fanzoneBetsService;

  @Mock private LiveUpdatesService liveUpdatesService;

  @Mock private SiteServeService siteServeService;
  @Mock private PersonalizedBetsSiteServImpl personalizedBetsSiteServImpl;

  @Mock ADAService adaService;
  private PersonalizedBets personalizedBets;

  @Test
  void testPersonalizedWithMultipleSelection() {

    personalizedBets = TestUtils.deserialize("fanzoneBets.json", PersonalizedBets.class);
    when(adaService.getFanzoneTrendingBets(any())).thenReturn(Mono.just(personalizedBets));

    List<TrendingItem> items =
        Stream.of(personalizedBets.getFanzoneYourTeam(), personalizedBets.getFanzoneOtherTeam())
            .flatMap(trendingItems -> trendingItems.stream())
            .collect(Collectors.toList());
    populateEventData(items);

    when(personalizedBetsSiteServImpl.getEventToOutcomeForOutcome(items))
        .thenReturn(Mono.justOrEmpty(items));

    Mono<PersonalizedBetsDto> sessionMono = fanzoneBetsService.processFanzoneTrendingBets("test");
    StepVerifier.create(sessionMono)
        .assertNext(
            data -> {
              assertNotNull(data.getFzOtherTeamPositions());
              assertNotNull(data.getFzYourTeamPositions());
            })
        .verifyComplete();
  }

  @Test
  void testPersonalizedWithsameSelection() {

    personalizedBets = TestUtils.deserialize("personalizedbets_same.json", PersonalizedBets.class);
    when(adaService.getFanzoneTrendingBets(any())).thenReturn(Mono.just(personalizedBets));

    List<TrendingItem> items =
        Stream.of(personalizedBets.getFanzoneYourTeam(), personalizedBets.getFanzoneOtherTeam())
            .flatMap(trendingItems -> trendingItems.stream())
            .collect(Collectors.toList());
    populateEventData(items);

    when(personalizedBetsSiteServImpl.getEventToOutcomeForOutcome(items))
        .thenReturn(Mono.justOrEmpty(personalizedBets.getFanzoneOtherTeam()));

    Mono<PersonalizedBetsDto> sessionMono = fanzoneBetsService.processFanzoneTrendingBets("test");
    StepVerifier.create(sessionMono)
        .assertNext(
            data -> {
              assertNotNull(data.getFzOtherTeamPositions());
              assertNotNull(data.getFzYourTeamPositions());
            })
        .verifyComplete();
  }

  @Test
  void testPersonalizedWithFanzoneRecsEmpty() {

    TrendingBetsContext.getTrendingBets().put("football_tb_48h_48h", prepareTrendingBetsDto());
    personalizedBets = TestUtils.deserialize("personalizedbets_empty.json", PersonalizedBets.class);
    when(adaService.getFanzoneTrendingBets(any())).thenReturn(Mono.just(personalizedBets));

    List<TrendingItem> items =
        Stream.of(personalizedBets.getFanzoneYourTeam(), personalizedBets.getFanzoneOtherTeam())
            .flatMap(trendingItems -> trendingItems.stream())
            .collect(Collectors.toList());
    populateEventData(items);

    when(personalizedBetsSiteServImpl.getEventToOutcomeForOutcome(items))
        .thenReturn(Mono.justOrEmpty(items));

    Mono<PersonalizedBetsDto> sessionMono = fanzoneBetsService.processFanzoneTrendingBets("test");
    StepVerifier.create(sessionMono)
        .assertNext(
            data -> {
              assertNotNull(data.getFzOtherTeamPositions());
              assertNotNull(data.getFzYourTeamPositions());
            })
        .verifyComplete();
  }

  private TrendingBetsDto prepareTrendingBetsDto() {

    return TrendingBetsDto.builder().positions(new HashSet<>()).build();
  }

  @Test
  void testPersonalizedWithException() {

    personalizedBets = TestUtils.deserialize("personalizedbets_same.json", PersonalizedBets.class);
    when(adaService.getFanzoneTrendingBets(any())).thenReturn(Mono.just(personalizedBets));

    List<TrendingItem> items =
        Stream.of(personalizedBets.getFanzoneYourTeam(), personalizedBets.getFanzoneOtherTeam())
            .flatMap(trendingItems -> trendingItems.stream())
            .collect(Collectors.toList());
    populateEventData(items);

    when(personalizedBetsSiteServImpl.getEventToOutcomeForOutcome(items))
        .thenThrow(new RuntimeException("invalid Id"));

    Mono<PersonalizedBetsDto> sessionMono = fanzoneBetsService.processFanzoneTrendingBets("test");
    StepVerifier.create(sessionMono).verifyErrorMessage("invalid Id");
  }

  private void populateEventData(List<TrendingItem> items) {
    items.forEach(
        item -> {
          item.setSelectionLivesChannel("sSELN" + item.getSelectionId());
          item.setTrendingEvent(prepareTrendingEvent(item));
        });
  }

  private TrendingEvent prepareTrendingEvent(TrendingItem item) {
    TrendingEvent event = new TrendingEvent();
    event.setId(item.getEventId());
    event.setName(item.getEventName());
    event.setLiveServChannels("SEVNT" + item.getEventId());
    event.setSelectionId(item.getSelectionId());

    OutputPrice price = new OutputPrice();
    price.setPriceNum((int) (item.getOdds() * 100));
    price.setPriceDen(100);

    OutputOutcome outcome = new OutputOutcome();
    outcome.setId(item.getSelectionId());
    outcome.setName(item.getSelectionName());
    outcome.setPrices(List.of(price));
    outcome.setLiveServChannels(item.getSelectionLivesChannel());

    OutputMarket market = new OutputMarket();
    market.setId(item.getMarketId());
    market.setName(item.getMarketName());
    market.setOutcomes(List.of(outcome));
    market.setLiveServChannels("sEVMKT" + item.getMarketId());

    event.setMarkets(List.of(market));
    return event;
  }
}
