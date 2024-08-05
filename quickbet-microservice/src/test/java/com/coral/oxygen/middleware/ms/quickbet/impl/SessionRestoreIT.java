package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.utils.BetBuildUtils.outcomeToEvent;
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.connector.ErrorMessageFactory;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.BetBuildResponse;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.ErrorMessage;
import com.coral.oxygen.middleware.ms.quickbet.utils.WebSocketTestClient;
import com.entain.oxygen.bettingapi.model.bet.api.response.GeneralResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuildResponseModel;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.OutcomeDetails;
import com.entain.oxygen.bettingapi.service.BettingService;
import io.vavr.collection.List;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@IntegrationTest
class SessionRestoreIT {

  @Autowired private SessionStorage<SessionDto> sessionStorage;
  @MockBean private BettingService bettingService;
  @MockBean private SiteServerService siteServerService;

  @Autowired private WebSocketTestClient webSocketTestClient;

  @Value("${remote-betslip.websocket.port}")
  int websocketPort;

  @Test
  void shouldBuildBetAndReturnBetsToTheClientAfterRestoringSession() {
    // GIVEN
    String outcomeId = "123456789";
    GeneralResponse<BetBuildResponseModel> bppResponse = createResponseWithoutErrors(outcomeId);
    when(bettingService.buildBetV2(any(), any())).thenReturn(bppResponse);
    String sessionId = UUID.randomUUID().toString();
    SessionDto session = new SessionDto(sessionId);
    session.setSelectedOutcomeIds(List.of(outcomeId));
    sessionStorage.persist(session);

    when(siteServerService.getEventsForOutcomeIds(any())).thenReturn(outcomeToEvent(outcomeId));

    // WHEN
    webSocketTestClient.start(websocketPort, sessionId);
    webSocketTestClient.wait(Messages.BUILD_BET_RESPONSE);

    // THEN
    BetBuildResponse receivedData =
        webSocketTestClient.getReceivedData(Messages.BUILD_BET_RESPONSE, BetBuildResponse.class);
    assertThat(receivedData.getBetBuildResponseModel().getOutcomeDetails())
        .flatExtracting(OutcomeDetails::getId)
        .contains(outcomeId);
  }

  @Test
  void shouldReturnExceptionWhenSessionIsNotFound() {
    // GIVEN
    String nonExistingSession = UUID.randomUUID().toString();

    // WHEN
    webSocketTestClient.start(websocketPort, nonExistingSession);
    ErrorMessage errorMessage = webSocketTestClient.wait(Messages.ERROR_CODE, ErrorMessage.class);

    // THEN
    assertThat(errorMessage).isEqualTo(ErrorMessageFactory.sessionNotFound());
    assertThat(webSocketTestClient.isConnected()).isFalse();
  }

  private GeneralResponse<BetBuildResponseModel> createResponseWithoutErrors(String outcomeId) {
    BetBuildResponseModel betBuild = new BetBuildResponseModel();
    betBuild.getOutcomeDetails().add(createOutcomeDetails(outcomeId));

    return new GeneralResponse<>(betBuild, null);
  }

  private OutcomeDetails createOutcomeDetails(String outcomeId) {
    OutcomeDetails outcomeDetails = new OutcomeDetails();
    outcomeDetails.setId(outcomeId);
    outcomeDetails.setMarketId("2");
    outcomeDetails.setEventId("1");
    return outcomeDetails;
  }
}
