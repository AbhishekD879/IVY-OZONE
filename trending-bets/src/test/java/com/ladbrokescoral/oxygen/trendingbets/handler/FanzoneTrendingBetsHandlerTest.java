package com.ladbrokescoral.oxygen.trendingbets.handler;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.trendingbets.model.PersonalizedBetsDto;
import com.ladbrokescoral.oxygen.trendingbets.service.FanzoneBetsService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.ApplicationContext;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.reactive.server.WebTestClient;
import reactor.core.publisher.Mono;

@RunWith(SpringRunner.class)
@SpringBootTest
@ActiveProfiles("TEST")
class FanzoneTrendingBetsHandlerTest {

  @Autowired private ApplicationContext context;

  @MockBean private FanzoneBetsService betsService;

  private WebTestClient webTestClient;

  private static final String FZ_TRENDING_BETS_URL = "/api/fanzone/tb/{teamId}";

  @BeforeEach
  public void setUp() {
    webTestClient = WebTestClient.bindToApplicationContext(context).build();
  }

  private WebTestClient.ResponseSpec executeRequest(String url, String teamId) {
    WebTestClient.RequestHeadersSpec<?> requestHeadersSpec =
        webTestClient
            .method(HttpMethod.GET)
            .uri(uriBuilder -> uriBuilder.path(url).build(teamId))
            .accept(MediaType.APPLICATION_JSON);
    return requestHeadersSpec.exchange();
  }

  @Test
  void testFyTrendingBetsWithOutTeamId() {
    executeRequest(FZ_TRENDING_BETS_URL, null).expectStatus().isNotFound();
  }

  @Test
  void testFyTrendingBetsWithValidTeamId() {
    String teamId = "FZ001";
    when(betsService.processFanzoneTrendingBets(any()))
        .thenReturn(Mono.just(PersonalizedBetsDto.builder().build()));
    executeRequest(FZ_TRENDING_BETS_URL, teamId).expectStatus().isOk();
  }

  @ParameterizedTest
  @ValueSource(strings = {"message", ""})
  void testFyTrendingBetsWithValidTeamIdButError(String message) {
    String teamId = "FZ001";
    when(betsService.processFanzoneTrendingBets(any()))
        .thenReturn(Mono.error(new RuntimeException(message.isEmpty() ? null : message)));
    executeRequest(FZ_TRENDING_BETS_URL, teamId).expectStatus().is5xxServerError();
  }
}
