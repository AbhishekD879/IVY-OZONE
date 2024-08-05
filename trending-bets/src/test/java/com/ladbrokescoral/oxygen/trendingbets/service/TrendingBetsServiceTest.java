package com.ladbrokescoral.oxygen.trendingbets.service;

import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.trendingbets.context.ChannelHandlersContext;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetSession;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.dto.TrendingBets;
import com.ladbrokescoral.oxygen.trendingbets.dto.TrendingItem;
import com.ladbrokescoral.oxygen.trendingbets.model.*;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.SiteServeService;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.TrendingBetsSiteServImpl;
import com.ladbrokescoral.oxygen.trendingbets.util.TrendingBetsUtil;
import com.ladbrokescoral.oxygen.trendingbets.utils.TestUtils;
import java.util.Date;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;
import java.util.stream.Stream;
import lombok.SneakyThrows;
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.util.ReflectionTestUtils;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@SpringBootTest
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
@ActiveProfiles("TEST")
class TrendingBetsServiceTest {

  @InjectMocks private TrendingBetsService trendingBetsService;

  @Mock private LiveUpdatesService liveUpdatesService;

  @Mock private SiteServeService siteServeService;
  @Mock private TrendingBetsSiteServImpl trendingBetsSiteServImpl;

  private TrendingBets trendingBets;

  @ParameterizedTest
  @MethodSource("trendingBetCases")
  void test(String frontend, String resource) {
    String channelId = populateTrendingBetsAndChannelId(resource);
    ChannelHandlersContext.createIfAbsentAndReturnChannel(channelId);
    ReflectionTestUtils.setField(trendingBetsService, "frontend", frontend);
    ReflectionTestUtils.setField(trendingBetsService, "preMatchEventType", "prematch");
    ReflectionTestUtils.setField(trendingBetsService, "allPayloadType", "all");
    ReflectionTestUtils.setField(
        trendingBetsService,
        "filterMarketDrilldownTagNames",
        resource.contains("FZ") ? new String[] {"MKTFLAG_FZ", "MKTFLAG_PVT"} : null);
    ReflectionTestUtils.setField(
        trendingBetsService,
        "filterEventDrilldownTagNames",
        resource.contains("FZ") ? new String[] {"EVFLAG_SP"} : null);
    when(trendingBetsSiteServImpl.getEventToOutcomeForOutcome(trendingBets.events()))
        .thenReturn(Mono.justOrEmpty(trendingBets.events()));

    Mono<TrendingBetSession> sessionMono = trendingBetsService.processTrendingBets(trendingBets);
    sessionMono.subscribe();
    StepVerifier.create(sessionMono).expectSubscription();

    TrendingBetsDto trendingBetsDto = TrendingBetsContext.getTrendingBets().get(channelId);
    Assertions.assertNotNull(trendingBetsDto);
    if (resource.equals("trendingbets_FZ.json")) {
      Assertions.assertEquals(2, trendingBetsDto.getPositions().size());
    } else {
      Assertions.assertEquals(4, trendingBetsDto.getPositions().size());
    }
  }

  private static Stream<Arguments> trendingBetCases() {
    return Stream.of(
        Arguments.of("ld", "trendingbets_start.json"),
        Arguments.of("ld", "trendingbets_rank_changes.json"),
        Arguments.of("ld", "trendingbets_channel_12h_12h.json"),
        Arguments.of("ld", "trendingbets_channel_12h_12h_bet_change.json"),
        Arguments.of("ld", "trendingbets_bet_changes.json"),
        Arguments.of("ld", "trendingbets_outdated.json"),
        Arguments.of("cl", "trendingbets_bet_changes.json"),
        Arguments.of("ld", "trendingbets_bets_live_all.json"),
        Arguments.of("ld", "trendingbets_bets_live_edp.json"),
        Arguments.of("ld", "trendingbets_bets_prematch_all.json"),
        Arguments.of("ld", "trendingbets_bets_prematch_edp.json"),
        Arguments.of("ld", "trendingbets_FZ.json"));
  }

  @Test
  void testGetTrendingSelectionWithMappingClear() {
    test("ld", "trendingbets_channel_12h_12h.json");
    TrendingEvent event = new TrendingEvent();
    event.setSelectionId("241157657");
    TrendingBetsContext.getSelectionMappings().get(event).clear();
    test("ld", "trendingbets_channel_12h_12h_bet_change.json");
  }

  @SneakyThrows
  @Test
  void testGetTrendingSelectionWithLock() {
    populateTrendingBetsAndChannelId("trendingbets_start.json");
    TrendingItem item = trendingBets.events().get(0);
    CountDownLatch latch = new CountDownLatch(1);
    ReentrantLock[] locks =
        (ReentrantLock[]) ReflectionTestUtils.getField(PopularBetsService.class, "locks");
    ReentrantLock lock =
        locks[
            Integer.parseInt(item.getSelectionId().substring(item.getSelectionId().length() - 1))];
    lock.lock();
    CompletableFuture.runAsync(() -> trendingBetsService.getTrendingSelection(item));
    latch.await(2, TimeUnit.SECONDS);
    TrendingBetsContext.getPopularSelections()
        .put(item.getSelectionLivesChannel(), List.of(item.getTrendingEvent()));
    lock.unlock();
    Assertions.assertNotNull(
        TrendingBetsContext.getPopularSelections().get(item.getSelectionLivesChannel()));
  }

  @Test
  void testDateComparison() {
    Date date = new Date();

    Assertions.assertFalse(TrendingBetsUtil.isBefore(null, date));
    Assertions.assertFalse(TrendingBetsUtil.isBefore(date, null));
  }

  private String populateTrendingBetsAndChannelId(String resource) {
    trendingBets = TestUtils.deserialize(resource, TrendingBets.class);

    populateEventData(trendingBets.events());
    return TrendingBetsUtil.prepareChannelId(
        trendingBets.sport(), trendingBets.backedWithIn(), trendingBets.eventStartIn());
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
    event.setTypeId("typeId_" + item.getEventId());
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

    if ("FZ".equals(item.getMarketName())) {
      market.setDrilldownTagNames("MKTFLAG_FZ");
      event.setDrilldownTagNames("EVFLAG_FZ");
    } else {
      market.setDrilldownTagNames("MKTFLAG_BL");
    }
    if ("special".equals(item.getMarketName())) {
      market.setDrilldownTagNames("special");
      event.setDrilldownTagNames("EVFLAG_SP");
    }
    event.setMarkets(List.of(market));
    return event;
  }
}
