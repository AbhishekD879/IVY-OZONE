package com.ladbrokescoral.oxygen.trendingbets.service;

import static org.mockito.Mockito.*;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.trendingbets.dto.PersonalizedBets;
import com.ladbrokescoral.oxygen.trendingbets.webclient.ADARequestClient;
import java.io.IOException;
import okhttp3.mockwebserver.MockResponse;
import okhttp3.mockwebserver.MockWebServer;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.InjectMocks;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@SpringBootTest
@ActiveProfiles("TEST")
public class ADAServiceTest {

  private static final String USER_NAME = "ld_user";

  private static final String TEAM_ID = "teamId";

  @InjectMocks @Autowired private ADAService adaService;

  @Autowired WebClient adaWebClient;
  @Autowired ADARequestClient adaRequestClient;

  private static MockWebServer mockWebServer = new MockWebServer();
  @Autowired ObjectMapper objectMapper;

  @BeforeEach
  void setup() {
    String baseUrl = mockWebServer.url("/").toString();
    WebClient webClient = adaWebClient.mutate().baseUrl(baseUrl).build();
    ReflectionTestUtils.setField(adaRequestClient, "webClient", webClient);
  }

  @ParameterizedTest
  @ValueSource(booleans = {true, false})
  void testForYouTrendingBets(boolean input) {

    if (input) {
      mockWebServer.enqueue(new MockResponse().setResponseCode(200));
      Mono<PersonalizedBets> trendingBets = adaService.getForYouTrendingBets(USER_NAME);
      StepVerifier.create(trendingBets).verifyComplete();
    } else {
      mockWebServer.enqueue(new MockResponse().setResponseCode(500));
      Mono<PersonalizedBets> trendingBets = adaService.getForYouTrendingBets(USER_NAME);
      StepVerifier.create(trendingBets).verifyError();
    }
  }

  @ParameterizedTest
  @ValueSource(booleans = {true, false})
  void testFanzoneTrendingBets(boolean input) {

    if (input) {
      mockWebServer.enqueue(new MockResponse().setResponseCode(200));
      Mono<PersonalizedBets> trendingBets = adaService.getFanzoneTrendingBets(TEAM_ID);
      StepVerifier.create(trendingBets).verifyComplete();
    } else {
      mockWebServer.enqueue(new MockResponse().setResponseCode(500));
      Mono<PersonalizedBets> trendingBets = adaService.getFanzoneTrendingBets(TEAM_ID);
      StepVerifier.create(trendingBets).verifyError();
    }
  }

  @AfterAll
  public static void tearDown() throws IOException {
    mockWebServer.shutdown();
  }
}
