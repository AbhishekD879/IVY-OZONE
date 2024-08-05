package com.ladbrokescoral.oxygen.trendingbets.handler;

import com.ladbrokescoral.oxygen.trendingbets.context.ChannelHandlersContext;
import com.ladbrokescoral.oxygen.trendingbets.context.PopularAccaContext;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingBetsDto;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingPosition;
import java.util.ArrayList;
import java.util.Date;
import java.util.Set;
import java.util.TreeSet;
import org.junit.jupiter.api.*;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.ApplicationContext;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.reactive.server.WebTestClient;

@RunWith(SpringRunner.class)
@SpringBootTest
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
@ActiveProfiles("TEST")
class TrendingBetsApiIntegrationTest {

  @Autowired private ApplicationContext context;

  private WebTestClient webTestClient;

  private static final String TRENDING_BETS_URL = "/api/trendingbets/betslip";

  private static final String TRENDING_STATS_URL = "/api/trendingstats";

  @BeforeEach
  public void setUp() {
    webTestClient = WebTestClient.bindToApplicationContext(context).build();
  }

  private WebTestClient.ResponseSpec executeRequest(String url) {
    return webTestClient.get().uri(url).accept(MediaType.APPLICATION_JSON).exchange();
  }

  @Test
  @Order(1)
  void testTrendingBetsForBetslipWithoutData() {
    executeRequest(TRENDING_BETS_URL + "/football_tb_12h_1h").expectStatus().isBadRequest();
  }

  @Test
  @Order(2)
  void testTrendingBetsForBetslip() {
    TrendingBetsContext.getTrendingBets().put("football_tb_1h_1h", prepareTrendingBetsDto(6));
    executeRequest(TRENDING_BETS_URL + "/football_tb_1h_1h").expectStatus().isOk();
  }

  @Test
  @Order(3)
  void testTrendingBetsForBetslipWithoutChannelAndData() {
    executeRequest(TRENDING_BETS_URL).expectStatus().isNotFound();
  }

  @Test
  @Order(4)
  void testTrendingBetStatistics() {
    ChannelHandlersContext.createIfAbsentAndReturnChannel("football_tb_12h_1h");
    TrendingBetsContext.getPopularSelections().put("sEVENT123121", new ArrayList<>());
    executeRequest(TRENDING_STATS_URL).expectStatus().isOk();
    TrendingBetsContext.getPopularSelections().remove("sEVENT123121");
  }

  @Test
  @Order(5)
  void testPopularAccaStatistics() {
    String stats = "/popularAccaStats";
    pushDataToPopulatAcca();
    executeRequest(TRENDING_STATS_URL + stats).expectStatus().isOk();

    PopularAccaContext.getEventAccas().clear();
    PopularAccaContext.getSelectionAccas().clear();
    PopularAccaContext.getLeagueAccas().clear();
  }

  private void pushDataToPopulatAcca() {

    Set<TrendingPosition> positions = new TreeSet<>();
    positions.add(prepareTrendingPosition("s200", true, false, 200));
    positions.add(prepareTrendingPosition("s300", false, true, 300));

    PopularAccaContext.getEventAccas().put("eventId", positions);
    PopularAccaContext.getSelectionAccas()
        .put("s200", prepareTrendingPosition("s200", true, false, 200));
    PopularAccaContext.getSelectionAccas()
        .put("s300", prepareTrendingPosition("s200", true, false, 200));

    PopularAccaContext.getLeagueAccas().put("typeId", positions);
  }

  private TrendingBetsDto prepareTrendingBetsDto(int count) {

    Set<TrendingPosition> positions = new TreeSet<>();
    for (int i = 0; i < count; i++) {
      positions.add(prepareTrendingPosition("s" + i, false, false, i));
    }
    positions.add(prepareTrendingPosition("s200", true, false, 200));
    positions.add(prepareTrendingPosition("s300", false, true, 300));
    return TrendingBetsDto.builder().updatedAt(new Date()).positions(positions).build();
  }

  private TrendingPosition prepareTrendingPosition(
      String selectionId, Boolean isSuspended, Boolean isLive, int rank) {
    TrendingPosition position = new TrendingPosition();
    position.setEvent(prepareTrendingSelection(selectionId, isSuspended, isLive));
    position.setRank(rank);
    return position;
  }

  private TrendingEvent prepareTrendingSelection(
      String selectionId, Boolean isSuspended, Boolean isLive) {
    TrendingEvent selection = new TrendingEvent();
    selection.setSelectionId(selectionId);
    selection.setId("eventId");
    selection.setTypeId("typeId");

    selection.setIsSuspended(isSuspended);
    selection.setEventIsLive(isLive);
    return selection;
  }
}
