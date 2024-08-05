package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.util.BetUtils.OPEN_BET_OVERASK_PROVIDER;
import static com.coral.oxygen.middleware.ms.quickbet.utils.BetBuildUtils.outcomeToEvent;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.UIPlaceBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.AddSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.UIBet;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.UILeg;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.BetBuildResponse;
import com.coral.oxygen.middleware.ms.quickbet.utils.WebSocketTestClient;
import com.entain.oxygen.bettingapi.model.bet.api.common.Stake;
import com.entain.oxygen.bettingapi.model.bet.api.common.YesNo;
import com.entain.oxygen.bettingapi.model.bet.api.common.placeBetV2.BetId;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetRef;
import com.entain.oxygen.bettingapi.model.bet.api.response.Bet;
import com.entain.oxygen.bettingapi.model.bet.api.response.BetsResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.GeneralResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuild;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuildResponseModel;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetCombination;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.BetPlacement;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.RespBetPlace;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.RespStatus;
import com.entain.oxygen.bettingapi.service.BettingService;
import io.vavr.collection.HashMap;
import io.vavr.collection.List;
import java.util.Collections;
import java.util.UUID;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.mock.mockito.MockBean;

@IntegrationTest
class DelayedBetsTaskStoppingAndRestoringIT {

  private static final String TOKEN =
      "053f166a31c499d95d6ef2062d3ac1c92aa119981e2e694550378e8de5850e83";
  private static final String OUTCOME_ID = "553375164";

  @MockBean private ScheduledThreadPoolExecutor overaskReadBetThreadPoolExecutor;

  @Autowired private SessionStorage<SessionDto> sessionStorage;
  @Autowired private WebSocketTestClient client;
  @MockBean private BettingService bettingService;
  @MockBean private SiteServerService siteServerService;
  @Mock private ScheduledFuture readTask;

  @Value("${remote-betslip.websocket.port}")
  private int websocketPort;

  @BeforeEach
  void setUp() {
    when(overaskReadBetThreadPoolExecutor.scheduleWithFixedDelay(
            any(Runnable.class), anyLong(), anyLong(), eq(TimeUnit.MILLISECONDS)))
        .thenReturn(readTask);
    when(bettingService.placeBetV2(any(), any())).thenReturn(createBetPlaceOveraskResponse());
    when(bettingService.readBet(anyString(), anyList())).thenReturn(createBetReadResponse());
    when(bettingService.buildBetV2(any(), any())).thenReturn(createBetBuild());
    when(siteServerService.getEventsForOutcomeIds(any())).thenReturn(outcomeToEvent(OUTCOME_ID));
  }

  @Test
  void shouldCancelTaskWhenSocketIsDisconnected() {
    // GIVEN
    AddSelectionRequest request = new AddSelectionRequest(OUTCOME_ID);
    client.emitWithWaitForResponse(
        Messages.ADD_SELECTION, request, Messages.BUILD_BET_RESPONSE, BetBuildResponse.class);

    UIPlaceBetRequest uiPlaceBetRequest =
        new UIPlaceBetRequest("I", "S|H|O0000000", "GBP", buildBet(createLegs(OUTCOME_ID, 1, 1)));

    client.emitWithWaitForResponse(
        Messages.PLACE_BET,
        uiPlaceBetRequest,
        Messages.PLACE_BET_OVERASK_RESPONSE_CODE,
        Object.class);

    // WHEN
    client.stop();

    // THEN
    verify(readTask, timeout(1000)).cancel(true);
  }

  @Test
  void shouldRestoreTaskAfterSessionRestoration() {
    // GIVEN
    String sessionInSessionStorage = createSessionInSessionStorage();
    client.stop();
    reset(overaskReadBetThreadPoolExecutor);
    String bppToken = UUID.randomUUID().toString();

    // WHEN
    client.start(websocketPort, sessionInSessionStorage, bppToken);

    // THEN
    verify(overaskReadBetThreadPoolExecutor)
        .scheduleWithFixedDelay(any(), anyLong(), anyLong(), eq(TimeUnit.MILLISECONDS));
  }

  private GeneralResponse<BetsResponse> createBetReadResponse() {
    BetsResponse response = new BetsResponse();
    Bet bet = new Bet();
    bet.setStake(new Stake());
    bet.setIsConfirmed(YesNo.N);
    response.setBet(Collections.singletonList(bet));
    return new GeneralResponse<>(response, null);
  }

  private GeneralResponse<RespBetPlace> createBetPlaceOveraskResponse() {
    RespBetPlace response = new RespBetPlace();
    BetPlacement betPlacement = new BetPlacement();

    com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.Bet bet =
        new com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.Bet();
    bet.setStatus(RespStatus.P);
    bet.setBetId(new BetId());

    betPlacement.setBet(bet);

    response.getBetPlacement().add(betPlacement);
    return new GeneralResponse<>(response, null);
  }

  private GeneralResponse<BetBuildResponseModel> createBetBuild() {
    BetBuildResponseModel response = new BetBuildResponseModel();
    response.getBetBuild().add(createBet());
    return new GeneralResponse<>(response, null);
  }

  private BetBuild createBet() {
    BetBuild betBuild = new BetBuild();
    betBuild.setBetNo("1");
    BetCombination betCombination = new BetCombination();
    betCombination.setBetType("SGL");
    betCombination.setBetNoOfLines("1");

    betBuild.getBetCombination().add(betCombination);

    return betBuild;
  }

  private List<UIBet> buildBet(UILeg... legs) {
    return List.of(legs)
        .zipWithIndex(
            (leg, index) ->
                UIBet.builder()
                    .betNo(String.valueOf(index + 1))
                    .winType("W")
                    .stakePerLine("6")
                    .betType("SGL")
                    .legs(List.of(legs[index]))
                    .build());
  }

  private UILeg createLegs(String outcomeId, int priceNum, int priceDen) {
    return UILeg.builder()
        .priceNum(priceNum)
        .priceDen(priceDen)
        .outcomeIds(List.of(outcomeId))
        .priceType("L")
        .build();
  }

  private String createSessionInSessionStorage() {
    String sessionId = UUID.randomUUID().toString();
    SessionDto session = new SessionDto(sessionId);
    session.setBetsToReadInBackground(
        HashMap.of(UUID.randomUUID(), List.of(new BetRef(OUTCOME_ID, OPEN_BET_OVERASK_PROVIDER))));
    sessionStorage.persist(session);
    return sessionId;
  }
}
