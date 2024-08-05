package com.ladbrokescoral.oxygen.trendingbets.service;

import static org.junit.Assert.*;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.dto.PopularBets;
import com.ladbrokescoral.oxygen.trendingbets.model.*;
import com.ladbrokescoral.oxygen.trendingbets.utils.TestUtils;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

@SpringBootTest
@ActiveProfiles("TEST")
class LiveUpdatesServiceTest {
  @Mock LiveServService liveServService;
  private static final String CHANNEL1 = "sEVENT0003959750";
  private static final String CHANNEL2 = "sEVMKT0052730250";
  private static final String CHANNEL3 = "sSELCN0241157646";

  @InjectMocks LiveUpdatesService liveUpdatesService;

  private TrendingEvent trendingEvent;

  @Test
  void testSubscriberForEvent() {
    trendingEvent = TestUtils.deserialize("trendingevent.json", TrendingEvent.class);

    TrendingEvent trendingEvent2 =
        TestUtils.deserialize("trendingevent_channels.json", TrendingEvent.class);
    TrendingBetsContext.getPopularSelections().put(CHANNEL1, Arrays.asList(trendingEvent));
    TrendingBetsContext.getPopularSelections().put(CHANNEL2, new ArrayList());
    ArrayList<TrendingEvent> list = new ArrayList<>();
    list.add(trendingEvent2);
    TrendingBetsContext.getPopularSelections().put(CHANNEL3, list);

    doNothing().when(liveServService).subscribe(any(), any());
    liveUpdatesService.subscriberForEvent(trendingEvent.getStreamChannels(), trendingEvent.getId());
    assertEquals(3, TrendingBetsContext.getPopularSelections().size());
  }

  @Test
  void testSubscriberForEvent1() {
    trendingEvent = TestUtils.deserialize("trendingevent.json", TrendingEvent.class);
    trendingEvent.setLiveServChannels(null);

    TrendingEvent trendingEvent2 =
        TestUtils.deserialize("trendingevent_channels.json", TrendingEvent.class);
    TrendingBetsContext.getPopularSelections().put(CHANNEL1, Arrays.asList(trendingEvent));
    TrendingBetsContext.getPopularSelections().put(CHANNEL2, new ArrayList());
    ArrayList<TrendingEvent> list = new ArrayList<>();
    list.add(trendingEvent2);
    TrendingBetsContext.getPopularSelections().put(CHANNEL3, list);

    doNothing().when(liveServService).subscribe(any(), any());
    Stream<String> streamChannels = trendingEvent.getStreamChannels();
    String trendingEventId = trendingEvent.getId();
    assertThrows(
        NullPointerException.class,
        () -> liveUpdatesService.subscriberForEvent(streamChannels, trendingEventId));
  }

  @ParameterizedTest
  @CsvSource({"TRENDING_BETS", "PERSONALIZED_BETS"})
  void testSubscriberForEvent_SubscribedChannelsNull(String bets) {
    trendingEvent = prepareTrendingSelection("1221212121", false, true);
    prepareTrendingContext(bets);
    doNothing().when(liveServService).subscribe(any(), any());
    liveUpdatesService.subscriberForEvent(trendingEvent.getStreamChannels(), trendingEvent.getId());
    assertEquals(3, TrendingBetsContext.getSelectionByBetsType(PopularBets.valueOf(bets)).size());
  }

  private TrendingEvent prepareTrendingSelection(
      String selectionId, Boolean isSuspended, Boolean isLive) {
    TrendingEvent trendingEvent = new TrendingEvent();
    trendingEvent.setId("123456782");
    trendingEvent.setName("Team D - Team E");
    trendingEvent.setStartTime("2023-06-07 23:00:00");
    trendingEvent.setLiveServChannels("sEVENT0123456782");
    OutputMarket market = new OutputMarket();
    market.setId("1568888624");
    market.setName("Match Betting");
    market.setLiveServChannels("sEVMKT1568888624");
    OutputOutcome outcome = new OutputOutcome();
    outcome.setId(selectionId);
    outcome.setName("Team E");
    outcome.setLiveServChannels("sSELCN0235366998");
    outcome.setPrices(List.of(new OutputPrice()));
    market.setOutcomes(List.of(outcome));
    trendingEvent.setMarkets(List.of(market));
    trendingEvent.setSelectionId(selectionId);
    trendingEvent.setIsSuspended(isSuspended);
    trendingEvent.setEventIsLive(isLive);
    return trendingEvent;
  }

  public List<TrendingEvent> convertToList(TrendingEvent... event) {
    return Stream.of(event).collect(Collectors.toCollection(ArrayList::new));
  }

  @AfterEach
  public void tearDown() {
    TrendingBetsContext.getPopularSelections().clear();
    TrendingBetsContext.getSelectionMappings().clear();
    TrendingBetsContext.getPersonalizedSelections().clear();
    TrendingBetsContext.getSubscribedChannels().clear();
  }

  private void prepareTrendingContext(String bets) {
    TrendingEvent trendingEvent = prepareTrendingSelection("1221212121", false, true);
    if ("TRENDING_BETS".equals(bets) || "both".equals(bets)) {

      TrendingBetsContext.getPopularSelections()
          .put("sEVENT0123456782", convertToList(trendingEvent));
      TrendingBetsContext.getPopularSelections()
          .put("sEVMKT1568888624", convertToList(trendingEvent));
      TrendingBetsContext.getPopularSelections()
          .put("sSELCN0235366998", convertToList(trendingEvent));
    }
    if ("PERSONALIZED_BETS".equals(bets) || "both".equals(bets)) {

      TrendingBetsContext.getPersonalizedSelections()
          .put("sEVENT0123456782", convertToList(trendingEvent));
      TrendingBetsContext.getPersonalizedSelections()
          .put("sEVMKT1568888624", convertToList(trendingEvent));
      TrendingBetsContext.getPersonalizedSelections()
          .put("sSELCN0235366998", convertToList(trendingEvent));
    }
    TrendingBetsContext.getSubscribedChannels().put("sEVENT0123456782", "default");
    TrendingBetsContext.getSubscribedChannels().put("sEVMKT1568888624", "default");
    TrendingBetsContext.getSubscribedChannels().put("sSELCN0235366998", "default");

    TrendingBetsContext.getSelectionMappings()
        .put(trendingEvent, Set.of("football_trendingbets_1h_1h"));
  }
}
