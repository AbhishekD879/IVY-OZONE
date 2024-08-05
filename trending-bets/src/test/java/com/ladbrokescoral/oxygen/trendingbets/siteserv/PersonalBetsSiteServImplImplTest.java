package com.ladbrokescoral.oxygen.trendingbets.siteserv;

import static org.junit.Assert.assertEquals;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.doReturn;

import com.egalacoral.spark.siteserver.api.SiteServerApiAsync;
import com.egalacoral.spark.siteserver.model.Event;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.dto.TrendingItem;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.converter.EventToTrendingEventConverter;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.converter.MarketToOutputMarketConverter;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.converter.OutcomeToOutputOutcomeConverter;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.converter.PriceToOutputPriceConverter;
import java.io.File;
import java.io.IOException;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.SpyBean;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@Slf4j
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = {PersonalizedBetsSiteServImpl.class, ObjectMapper.class})
class PersonalBetsSiteServImplImplTest {

  @Autowired public PersonalizedBetsSiteServImpl personalizedBetsSiteServImpl;
  @Autowired public SiteServeService siteServeService;

  @MockBean SiteServerApiAsync siteServerApiAsync;
  @SpyBean EventToTrendingEventConverter eventToTrendingEventConverter;
  @SpyBean MarketToOutputMarketConverter marketToOutputMarketConverter;
  @SpyBean PriceToOutputPriceConverter priceToOutputPriceConverter;
  @SpyBean OutcomeToOutputOutcomeConverter outcomeToOutputOutcomeConverter;

  @SpyBean ObjectMapper objectMapper;
  List<Event> events;

  String BASE_PATH = "src/test/resources/trendingbet/";

  @BeforeEach
  public void setUp()
      throws NoSuchMethodException, InvocationTargetException, InstantiationException,
          IllegalAccessException {

    Constructor<?> constructor =
        TrendingBetsContext.class.getDeclaredConstructor(
            Integer.class, Integer.class, Integer.class);
    constructor.setAccessible(true);
    Object context = constructor.newInstance(10, 10, 10);
    objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
  }

  @ParameterizedTest
  @CsvSource({
    "OutcomeForEvent.json,trending_bets_payload.json,trending_bet_response.json,false",
    "OutcomeForEvent_two_selections.json,trending_bets_payload.json,trending_bet_response.json,true",
    "OutcomeForEvent_two_selections_fz.json,trending_bets_payload.json,trending_bet_response.json,true",
    "OutcomeForEvent_InActive_Market.json,trending_bets_payload.json,trending_bet_response_InActive_Event_Market.json,true",
    "OutcomeForEvent_InActive_Event.json,trending_bets_payload.json,trending_bet_response_InActive_Event_Market.json,true",
    "OutcomeForEvent_InActive_Event_outcome.json,trending_bets_payload.json,trending_bet_response_InActive_Event_Market_outcome.json,true",
    ",trending_bets_payload_single_selection.json,trending_bet_response_single_selection.json,true"
  })
  void testSiteServe(
      String siteServerResponse, String request, String response, boolean isContextReq)
      throws IOException {
    if (isContextReq) addSelectionToContext();
    MockSiteServeResponse(siteServerResponse);
    List<TrendingItem> trendingItems = prepareRequest(request);
    assertResponse(
        response, personalizedBetsSiteServImpl.getEventToOutcomeForOutcome(trendingItems));
  }

  private void addSelectionToContext() throws IOException {
    TrendingBetsContext.getPopularSelections()
        .put(
            "241157646",
            objectMapper.readValue(
                new File(BASE_PATH + "trending_position_incontext.json"),
                new TypeReference<>() {}));
    TrendingBetsContext.getSubscribedChannels().put("241157646", "123");
    // TrendingBetsContext.getPersonalizedSelections().put("123",new ArrayList<>());
  }

  private void assertResponse(String pathname, Mono<List<TrendingItem>> responseTrendingItems)
      throws IOException {
    List<TrendingItem> actualResponse = prepareRequest(pathname);
    StepVerifier.create(responseTrendingItems)
        .assertNext(val -> assertEquals(val, actualResponse))
        .expectComplete()
        .verify();
  }

  private void MockSiteServeResponse(String path) {
    try {
      events = objectMapper.readValue(new File(BASE_PATH + path), new TypeReference<>() {});
    } catch (IOException e) {
      events = new ArrayList<>();
    }
    doReturn(Mono.just(events))
        .when(siteServerApiAsync)
        .getEventToOutcomeForOutcome(anyList(), any(), anyList(), anyBoolean());
  }

  private List<TrendingItem> prepareRequest(String pathname) throws IOException {
    return objectMapper.readValue(new File(BASE_PATH + pathname), new TypeReference<>() {});
  }

  @AfterEach
  public void tearDown() {
    TrendingBetsContext.getPopularSelections().clear();
    TrendingBetsContext.getSubscribedChannels().clear();
  }
}
