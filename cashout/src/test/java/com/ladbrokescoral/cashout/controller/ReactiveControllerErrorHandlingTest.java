package com.ladbrokescoral.cashout.controller;

import static com.ladbrokescoral.cashout.model.Code.BET_PLACEMENT_CONNECTION_ERROR;
import static com.ladbrokescoral.cashout.model.Code.UNAUTHORIZED_ACCESS;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.coral.bpp.api.exception.BppConnectionException;
import com.coral.bpp.api.exception.BppUnauthorizedException;
import com.ladbrokescoral.cashout.bpptoken.BppToken;
import com.ladbrokescoral.cashout.bpptoken.BppTokenOperations;
import com.ladbrokescoral.cashout.bpptoken.User;
import com.ladbrokescoral.cashout.model.SSEType;
import com.ladbrokescoral.cashout.model.response.BetResponse;
import com.ladbrokescoral.cashout.model.response.ErrorBetResponse;
import com.ladbrokescoral.cashout.service.AccountHistoryService;
import com.ladbrokescoral.cashout.service.BetUpdateService;
import com.ladbrokescoral.cashout.service.DefaultErrorHandler;
import java.time.Duration;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.codec.ServerSentEvent;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@ExtendWith(MockitoExtension.class)
@Disabled
class ReactiveControllerErrorHandlingTest {

  public static final String TOKEN = "token";
  @Mock private BetUpdateService betUpdateServiceMock;
  @Mock private AccountHistoryService accountHistoryServiceMock;

  private ReactiveController controller;
  private BppTokenOperations bppTokenOps;

  @BeforeEach
  public void setUp() {
    bppTokenOps = Mockito.mock(BppTokenOperations.class);

    when(bppTokenOps.parseToken(TOKEN))
        .thenReturn(
            BppToken.builder()
                .token(TOKEN)
                .timeLeftToExpire(Duration.ofMinutes(30))
                .encodedUser(User.builder().sportBookUserName("user1").build())
                .build());

    controller =
        new ReactiveController(
            betUpdateServiceMock,
            accountHistoryServiceMock,
            new DefaultErrorHandler(),
            bppTokenOps);

    when(betUpdateServiceMock.getAccHistoryUpdatedBets(any(BppToken.class), any(), any()))
        .thenReturn(Flux.empty());
  }

  @Test
  void testBetDetailsWithBppAnauthorizedException() {
    when(accountHistoryServiceMock.getDetailedAccountHistoryWithOpenBetsOnly(any()))
        .thenReturn(Mono.error(new BppUnauthorizedException("Unauthorized")));

    Flux<ServerSentEvent<BetResponse>> result = controller.getBetDetails(TOKEN);

    StepVerifier.create(result)
        .assertNext(
            element -> {
              assertEquals(SSEType.INITIAL.getValue(), element.event());
              ErrorBetResponse data = (ErrorBetResponse) element.data();
              assertEquals(ErrorBetResponse.create(UNAUTHORIZED_ACCESS), data);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void testBetDetailsWithBppConnectionException() {
    when(accountHistoryServiceMock.getDetailedAccountHistoryWithOpenBetsOnly(any()))
        .thenReturn(Mono.error(new BppConnectionException()));

    Flux<ServerSentEvent<BetResponse>> result = controller.getBetDetails(TOKEN);

    StepVerifier.create(result)
        .assertNext(
            element -> {
              assertEquals(SSEType.INITIAL.getValue(), element.event());
              ErrorBetResponse data = (ErrorBetResponse) element.data();
              assertEquals(ErrorBetResponse.create(BET_PLACEMENT_CONNECTION_ERROR), data);
            })
        .expectComplete()
        .verify();
  }
}
