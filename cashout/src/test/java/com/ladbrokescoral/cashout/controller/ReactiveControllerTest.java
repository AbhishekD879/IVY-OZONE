package com.ladbrokescoral.cashout.controller;

import static com.ladbrokescoral.cashout.model.Code.UNAUTHORIZED_ACCESS;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.argThat;
import static org.mockito.Mockito.when;

import com.coral.bpp.api.exception.BppUnauthorizedException;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.ladbrokescoral.cashout.bpptoken.BppToken;
import com.ladbrokescoral.cashout.bpptoken.BppTokenOperations;
import com.ladbrokescoral.cashout.bpptoken.User;
import com.ladbrokescoral.cashout.model.SSEType;
import com.ladbrokescoral.cashout.model.response.BetResponse;
import com.ladbrokescoral.cashout.model.response.CashoutData;
import com.ladbrokescoral.cashout.model.response.ErrorBetResponse;
import com.ladbrokescoral.cashout.model.response.InitialAccountHistoryBetResponseModel;
import com.ladbrokescoral.cashout.model.response.UpdateCashoutResponse;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import com.ladbrokescoral.cashout.service.AccountHistoryService;
import com.ladbrokescoral.cashout.service.BetUpdateService;
import com.ladbrokescoral.cashout.service.DefaultErrorHandler;
import com.newrelic.api.agent.Token;
import java.time.Duration;
import java.util.Collections;
import java.util.List;
import java.util.function.Consumer;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.http.codec.ServerSentEvent;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@Disabled
class ReactiveControllerTest {

  public static final String TOKEN = "123";
  private BetUpdateService betUpdateServiceMock;
  private AccountHistoryService accountHistoryServiceMock;

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

    betUpdateServiceMock = Mockito.mock(BetUpdateService.class);
    accountHistoryServiceMock = Mockito.mock(AccountHistoryService.class);

    controller =
        new ReactiveController(
            betUpdateServiceMock,
            accountHistoryServiceMock,
            new DefaultErrorHandler(),
            bppTokenOps);

    BetSummaryModel betSummaryModel = new BetSummaryModel();
    betSummaryModel.setId("1212");

    Mono<List<BetSummaryModel>> initialData =
        Mono.fromCallable(() -> Collections.singletonList(betSummaryModel));
    when(accountHistoryServiceMock.getDetailedAccountHistoryWithOpenBetsOnly(any()))
        .thenReturn(initialData);

    UpdateDto betUpdate =
        UpdateDto.builder()
            .cashoutData(CashoutData.builder().betId("1212").cashoutStatus("0.9").build())
            .build();
    Flux<UpdateDto> updateData = Flux.just(betUpdate);
    mockUpdatesService(updateData);
  }

  @Test
  void testBetDetails() {
    Flux<ServerSentEvent<BetResponse>> result = controller.getBetDetails(TOKEN);

    StepVerifier.create(result)
        .assertNext(
            element -> {
              assertEquals(SSEType.INITIAL.getValue(), element.event());
              InitialAccountHistoryBetResponseModel data =
                  (InitialAccountHistoryBetResponseModel) element.data();
              assertEquals("1212", data.getBets().get(0).getId());
            })
        .assertNext(
            element -> {
              assertEquals(SSEType.CASHOUT_UPDATE.getValue(), element.event());
              UpdateCashoutResponse data = (UpdateCashoutResponse) element.data();
              assertEquals(
                  CashoutData.builder().betId("1212").cashoutStatus("0.9").build(),
                  data.getCashoutData());
            })
        .expectComplete()
        .verify();
  }

  @Test
  void testTokenParsingThrowsUnauthorized() {
    when(bppTokenOps.parseToken(TOKEN)).thenThrow(new BppUnauthorizedException("Unauthorized"));
    Flux<ServerSentEvent<BetResponse>> result = controller.getBetDetails(TOKEN);

    StepVerifier.create(result)
        .assertNext(verifyInitialData(ErrorBetResponse.create(UNAUTHORIZED_ACCESS)))
        .expectComplete()
        .verify();
  }

  private Consumer<ServerSentEvent<BetResponse>> verifyInitialData(Object data) {
    return element -> {
      assertEquals(SSEType.INITIAL.getValue(), element.event());
      assertEquals(data, element.data());
    };
  }

  private void mockUpdatesService(Flux<UpdateDto> updateData) {
    when(betUpdateServiceMock.getAccHistoryUpdatedBets(
            argThat(bppToken -> bppToken.getToken().equals(TOKEN)),
            any(Mono.class),
            any(Token.class)))
        .thenReturn(updateData);
  }
}
