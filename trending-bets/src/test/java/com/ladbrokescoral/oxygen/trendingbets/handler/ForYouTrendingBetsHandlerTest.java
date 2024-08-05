package com.ladbrokescoral.oxygen.trendingbets.handler;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

import com.coral.bpp.api.exception.BppConnectionException;
import com.coral.bpp.api.exception.BppUnauthorizedException;
import com.coral.bpp.api.model.bet.api.response.UserDataResponse;
import com.coral.bpp.api.service.BppApiAsync;
import com.ladbrokescoral.oxygen.trendingbets.model.PersonalizedBetsDto;
import com.ladbrokescoral.oxygen.trendingbets.service.ForYouBetsService;
import org.junit.jupiter.api.*;
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
import org.springframework.util.StringUtils;
import reactor.core.publisher.Mono;

@RunWith(SpringRunner.class)
@SpringBootTest
@ActiveProfiles("TEST")
class ForYouTrendingBetsHandlerTest {

  @Autowired private ApplicationContext context;

  @MockBean private BppApiAsync bppApiAsync;

  @MockBean private ForYouBetsService betsService;

  private WebTestClient webTestClient;

  private static final String FY_TRENDING_BETS_URL = "/api/fy/tb";

  @BeforeEach
  public void setUp() {
    webTestClient = WebTestClient.bindToApplicationContext(context).build();
  }

  private WebTestClient.ResponseSpec executeRequest(String url, String token) {
    WebTestClient.RequestHeadersSpec<?> requestHeadersSpec =
        webTestClient.method(HttpMethod.GET).uri(url).accept(MediaType.APPLICATION_JSON);
    if (StringUtils.hasText(token)) {
      requestHeadersSpec.header("token", token);
    }
    return requestHeadersSpec.exchange();
  }

  @Test
  void testFyTrendingBetsWithOutToken() {
    executeRequest(FY_TRENDING_BETS_URL, null).expectStatus().isBadRequest();
  }

  @Test
  void testFyTrendingBetsWithInvalidToken() {
    BppUnauthorizedException unauthorizedException = new BppUnauthorizedException("Invalid Token");
    when(bppApiAsync.getUserData(anyString()))
        .thenReturn(Mono.error(new RuntimeException(unauthorizedException)));
    executeRequest(FY_TRENDING_BETS_URL, "invalid_token").expectStatus().isUnauthorized();
  }

  @Test
  void testFyTrendingBetsWithConnectionError() {
    when(bppApiAsync.getUserData(anyString())).thenReturn(Mono.error(new BppConnectionException()));
    executeRequest(FY_TRENDING_BETS_URL, "invalid_token").expectStatus().is5xxServerError();
  }

  @Test
  void testFyTrendingBetsWithValidToken() {
    String token = "valid_token";
    UserDataResponse response = new UserDataResponse();
    response.setOxiApiToken(token);
    response.setSportBookUserName("ld_vk");
    when(bppApiAsync.getUserData(anyString())).thenReturn(Mono.just(response));
    when(betsService.processTrendingBets(any()))
        .thenReturn(Mono.just(PersonalizedBetsDto.builder().build()));
    executeRequest(FY_TRENDING_BETS_URL, token).expectStatus().isOk();
  }

  @Test
  void testFyTrendingBetsWithValidTokenButError() {
    String token = "valid_token";
    UserDataResponse response = new UserDataResponse();
    response.setOxiApiToken(token);
    response.setSportBookUserName("ld_vk");
    when(bppApiAsync.getUserData(anyString())).thenReturn(Mono.just(response));
    when(betsService.processTrendingBets(any())).thenThrow(new RuntimeException());
    executeRequest(FY_TRENDING_BETS_URL, token).expectStatus().is5xxServerError();
  }
}
