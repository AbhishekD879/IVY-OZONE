package com.ladbrokescoral.oxygen.trendingbets.liveserv.updates;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.client.model.Message;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.liveserv.LiveServMessageHandler;
import com.ladbrokescoral.oxygen.trendingbets.model.OutputMarket;
import com.ladbrokescoral.oxygen.trendingbets.model.OutputOutcome;
import com.ladbrokescoral.oxygen.trendingbets.model.OutputPrice;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import com.ladbrokescoral.oxygen.trendingbets.service.PopularBetUpdateService;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.SpyBean;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@ContextConfiguration(
    classes = {
      ObjectMapper.class,
      SelectionMessageApplier.class,
      MarketMessageApplier.class,
      EventMessageApplier.class
    })
public abstract class AbstractLiveServMessageHandlerTest {
  @SpyBean protected LiveServMessageHandler handler;
  @SpyBean protected LiveserveMessageApplierFactory factory;

  @MockBean protected LiveServService liveServService;
  @SpyBean protected ObjectMapper mapper;

  @SpyBean protected PopularBetUpdateService eventService;

  protected static final String SEL_CHANNEL = "sSELCN0235366998";
  protected static final String MARKET_CHANNEL = "sEVMKT1568888624";
  protected static final String EVENT_CHANNEL = "sEVENT0123456782";
  protected static final String EVENT_CHANNEL_INVALID = "EVENT0123456782";

  @BeforeEach
  public void init()
      throws NoSuchMethodException, InvocationTargetException, InstantiationException,
          IllegalAccessException {
    Constructor<?> constructor =
        TrendingBetsContext.class.getDeclaredConstructor(
            Integer.class, Integer.class, Integer.class);
    constructor.setAccessible(true);
    Object context = constructor.newInstance(10, 10, 10);
  }

  protected TrendingEvent getTrendingSelection() {

    TrendingEvent trendingEvent = new TrendingEvent();
    trendingEvent.setSelectionId("235366998");
    trendingEvent.setId("123456782");
    trendingEvent.setName("Team D - Team E");
    trendingEvent.setStartTime("2023-06-07 23:00:00");
    trendingEvent.setTypeId("123");
    trendingEvent.setLiveServChannels("sEVENT0123456782");
    trendingEvent.setEventStatusCode("A");
    OutputMarket market = new OutputMarket();
    market.setId("1568888624");
    market.setName("Match Betting");
    market.setLiveServChannels("sEVMKT1568888624");
    market.setMarketStatusCode("A");
    OutputOutcome outcome = new OutputOutcome();
    outcome.setId("123456782");
    outcome.setName("Team E");
    outcome.setLiveServChannels("sSELCN0235366998");
    outcome.setPrices(List.of(new OutputPrice()));
    outcome.setOutcomeStatusCode("A");
    market.setOutcomes(List.of(outcome));
    trendingEvent.setMarkets(List.of(market));

    return trendingEvent;
  }

  protected MessageEnvelope prepareMessageEnvolpe(String channel, String jsonData) {
    return new MessageEnvelope(channel, 123456782, new Message("", jsonData));
  }

  protected void createContext(boolean istrendingbets, boolean ispersonlizedBets, String... args) {
    TrendingEvent selection = getTrendingSelection();
    for (String arg : args) {
      if (istrendingbets)
        TrendingBetsContext.getPopularSelections().put(arg, convertToList(selection));
      if (ispersonlizedBets)
        TrendingBetsContext.getPersonalizedSelections().put(arg, convertToList(selection));
    }
  }

  protected static Boolean isSuspended(String channel) {
    return Optional.ofNullable(TrendingBetsContext.getPopularSelections().get(channel))
        .orElse(TrendingBetsContext.getPersonalizedSelections().get(channel))
        .get(0)
        .getIsSuspended();
  }

  protected static Boolean isEventLive(String selectionId) {
    return Optional.ofNullable(TrendingBetsContext.getPopularSelections().get(selectionId))
        .orElse(TrendingBetsContext.getPersonalizedSelections().get(selectionId))
        .get(0)
        .getEventIsLive();
  }

  @AfterEach
  public void tearDown() {
    TrendingBetsContext.getPopularSelections().clear();
    TrendingBetsContext.getPersonalizedSelections().clear();
  }

  public List<TrendingEvent> convertToList(TrendingEvent event) {
    List<TrendingEvent> list = new ArrayList<>();
    list.add(event);
    return list;
  }
}
