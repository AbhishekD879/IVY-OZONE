package com.ladbrokescoral.oxygen.trendingbets.handler;

import com.ladbrokescoral.oxygen.trendingbets.context.PopularAccaContext;
import com.ladbrokescoral.oxygen.trendingbets.dto.PopularAccaDto;
import com.ladbrokescoral.oxygen.trendingbets.dto.PopularAccaType;
import com.ladbrokescoral.oxygen.trendingbets.model.OutputMarket;
import com.ladbrokescoral.oxygen.trendingbets.model.OutputOutcome;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingPosition;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;
import org.jetbrains.annotations.NotNull;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.ApplicationContext;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.reactive.server.WebTestClient;

@RunWith(SpringRunner.class)
@SpringBootTest
@ActiveProfiles("TEST")
class PopularAccaHandlerTest {

  @Autowired private ApplicationContext context;

  private WebTestClient webTestClient;

  private static final String POPULAR_ACCA_URL = "/api/popular-acca";

  @BeforeEach
  public void setUp() {
    webTestClient = WebTestClient.bindToApplicationContext(context).build();
    pushDataToPopulatAcca();
  }

  private WebTestClient.ResponseSpec executeRequest(String url, PopularAccaDto request) {
    WebTestClient.RequestHeadersSpec<?> requestHeadersSpec =
        webTestClient
            .method(HttpMethod.POST)
            .uri(url)
            .accept(MediaType.APPLICATION_JSON)
            .bodyValue(request);

    return requestHeadersSpec.exchange();
  }

  @Test
  void testPopularAccaForMaxAccA() {
    checkResponseForMaxAcca(PopularAccaType.ALL, null, 2);
    checkResponseForMaxAcca(PopularAccaType.ALL, null, 3);

    checkResponseForMaxAcca(PopularAccaType.SELECTION, List.of("s1", "s4", "s3", "s8", "s20"), 2);
    checkResponseForMaxAcca(PopularAccaType.SELECTION, List.of("s1", "s4", "s3", "s8", "s20"), 3);

    checkResponseForMaxAcca(PopularAccaType.EVENT, List.of("e2", "e3", "e4"), 2);
    checkResponseForMaxAcca(PopularAccaType.EVENT, List.of("e2", "e3", "e4"), 3);

    checkResponseForMaxAcca(PopularAccaType.TYPEID, List.of("T2"), 1);
    checkResponseForMaxAcca(PopularAccaType.TYPEID, List.of("T2"), 2);
  }

  @Test
  void testPopularAccaForMinAccA() {
    checkResponseForMinAcca(PopularAccaType.ALL, null, 4);

    checkResponseForMinAcca(PopularAccaType.SELECTION, List.of("s1", "s4", "s3"), 4);

    checkResponseForMinAcca(PopularAccaType.EVENT, List.of("e2", "e3", "e4"), 4);

    checkResponseForMinAcca(PopularAccaType.TYPEID, List.of("T2"), 4);
  }

  @Test
  void testPopularAccaForThresoldValue() {
    checkResponseForThresold(PopularAccaType.ALL, null, 400, 0);

    checkResponseForThresold(PopularAccaType.SELECTION, List.of("s1", "s4", "s3"), 100, 3);

    checkResponseForThresold(PopularAccaType.EVENT, List.of("e2", "e3", "e4"), 100, 3);

    checkResponseForThresold(PopularAccaType.TYPEID, List.of("T2"), 400, 0);
  }

  @Test
  void testPopularAccaFormarket_template() {
    checkResponseForMarketTemplate(PopularAccaType.ALL, null, List.of("market_template"), 3);

    checkResponseForMarketTemplate(
        PopularAccaType.SELECTION, List.of("s1", "s4", "s3"), List.of("market_template1"), 0);

    checkResponseForMarketTemplate(
        PopularAccaType.EVENT, List.of("e2", "e3", "e4"), List.of("market_template"), 3);

    checkResponseForMarketTemplate(
        PopularAccaType.TYPEID, List.of("T2"), List.of("market_template1"), 0);
  }

  @Test
  void testPopularAccaForInvalidEvents() {

    checkResponseForInvalidIds(PopularAccaType.SELECTION, List.of("s11", "s41", "s31"));

    checkResponseForInvalidIds(
        PopularAccaType.EVENT, List.of("eventId21", "eventId31", "eventId41"));

    checkResponseForInvalidIds(PopularAccaType.TYPEID, List.of("TypeId21"));
  }

  @Test
  void testPopularAccaForLiveEvents() {
    checkResponseForMarketTemplate(
        PopularAccaType.SELECTION, List.of("s1", "s4", "s3"), List.of("market_template1"), 0);
  }

  @Test
  void testPopularAccaForException() {

    executeRequest(
            POPULAR_ACCA_URL, createPopularRequest(PopularAccaType.SELECTION, null, 0, 10, 0, null))
        .expectStatus()
        .is5xxServerError();
  }

  private WebTestClient.BodyContentSpec checkResponseForMinAcca(
      PopularAccaType type, List<String> values, int minAcca) {

    return executeRequest(
            POPULAR_ACCA_URL, createPopularRequest(type, values, minAcca, 10, 0, null))
        .expectStatus()
        .is2xxSuccessful()
        .expectBody()
        .jsonPath("positions")
        .isArray()
        .jsonPath("positions.length()")
        .isEqualTo(0);
  }

  private WebTestClient.BodyContentSpec checkResponseForThresold(
      PopularAccaType type, List<String> values, int thresold, int expectedValue) {
    PopularAccaContext.getLeagueAccas().size();
    return executeRequest(
            POPULAR_ACCA_URL, createPopularRequest(type, values, 0, 10, thresold, null))
        .expectStatus()
        .is2xxSuccessful()
        .expectBody()
        .jsonPath("positions")
        .isArray()
        .jsonPath("positions.length()")
        .isEqualTo(expectedValue);
  }

  private WebTestClient.BodyContentSpec checkResponseForMarketTemplate(
      PopularAccaType type, List<String> values, List<String> templates, int expectedValue) {
    PopularAccaContext.getLeagueAccas().size();
    return executeRequest(POPULAR_ACCA_URL, createPopularRequest(type, values, 0, 10, 0, templates))
        .expectStatus()
        .is2xxSuccessful()
        .expectBody()
        .jsonPath("positions")
        .isArray()
        .jsonPath("positions.length()")
        .isEqualTo(expectedValue);
  }

  @NotNull
  private WebTestClient.BodyContentSpec checkResponseForInvalidIds(
      PopularAccaType type, List<String> values) {
    return executeRequest(POPULAR_ACCA_URL, createPopularRequest(type, values, 0, 0, 0, null))
        .expectStatus()
        .is2xxSuccessful()
        .expectBody()
        .jsonPath("positions")
        .isArray()
        .jsonPath("positions.length()")
        .isEqualTo(0);
  }

  @NotNull
  private WebTestClient.BodyContentSpec checkResponseForMaxAcca(
      PopularAccaType type, List<String> values, int maxAcca) {
    return executeRequest(POPULAR_ACCA_URL, createPopularRequest(type, values, 0, maxAcca, 0, null))
        .expectStatus()
        .is2xxSuccessful()
        .expectBody()
        .jsonPath("positions")
        .isArray()
        .jsonPath("positions.length()")
        .isEqualTo(maxAcca);
  }

  private PopularAccaDto createPopularRequest(
      PopularAccaType key,
      List<String> values,
      int minAccA,
      int maxAcca,
      int thresold,
      List<String> identifiers) {
    PopularAccaDto popularAccaDto = new PopularAccaDto();
    popularAccaDto.setKey(key);
    popularAccaDto.setValues(values);
    popularAccaDto.setMinAccas(minAccA);
    popularAccaDto.setMaxAccas(maxAcca);
    popularAccaDto.setThresholdValue(thresold);
    popularAccaDto.setMarketIdentifiers(identifiers);
    return popularAccaDto;
  }

  private void pushDataToPopulatAcca() {

    Set<TrendingPosition> positions = new TreeSet<>();
    positions.add(prepareTrendingPosition("s1", "e2", "T2", 200));
    positions.add(prepareTrendingPosition("s2", "e2", "T2", 300));
    positions.add(prepareTrendingPosition("s1", "e2", "T2", 301));
    positions.add(prepareTrendingPosition("s4", "e4", "T2", 302));
    positions.add(prepareTrendingPosition("s3", "e3", "T3", 303));
    positions.add(prepareTrendingPosition("s1", "e2", "T2", 199));
    positions.add(prepareTrendingPosition("s8", "e2", "T2", 199));
    positions.add(prepareTrendingPosition("s20", "e2", "T2", 2));
    positions.add(prepareTrendingPosition("s21", "e2", "T2", 400));

    positions.add(prepareTrendingPosition("inplaySelection", "e9", "T4", 302));
    positions.add(prepareTrendingPosition("SuspendenSelection", "e2", "T5", 303));

    PopularAccaContext.addItemsToQueue("12_12", positions);
  }

  private TrendingPosition prepareTrendingPosition(
      String selectionId, String eventId, String typeId, int bets) {
    TrendingPosition position = new TrendingPosition();
    position.setEvent(prepareTrendingSelection(selectionId, eventId, typeId));
    position.setNBets(bets);
    position.setRank(bets);
    return position;
  }

  @NotNull
  private TrendingEvent prepareTrendingSelection(
      String selectionId, String eventId, String typeId) {
    TrendingEvent event = new TrendingEvent();
    event.setLiveServChannels(selectionId);
    event.setSelectionId(selectionId);
    event.setId(eventId);
    event.setTypeId(typeId);

    OutputOutcome outcome = new OutputOutcome();
    outcome.setId(selectionId);
    outcome.setLiveServChannels(selectionId);
    OutputMarket market = new OutputMarket();
    market.setId("");
    market.setLiveServChannels(selectionId);
    market.setOutcomes(List.of(outcome));
    market.setTemplateMarketName("market_template");
    market.setMaxAccumulators(10);
    market.setMinAccumulators(2);
    event.setMarkets(List.of(market));
    event.setEventIsLive("inplaySelection".equals(selectionId));
    event.setIsSuspended("SuspendenSelection".equals(selectionId));
    return event;
  }

  @AfterEach
  public void clearCache() {
    List.of("s1", "s2", "s4", "s3").forEach(PopularAccaContext.getSelectionAccas()::remove);
    List.of("e2", "e4", "e3").forEach(PopularAccaContext.getEventAccas()::remove);
    List.of("T2", "T3").forEach(PopularAccaContext.getLeagueAccas()::remove);
  }
}
