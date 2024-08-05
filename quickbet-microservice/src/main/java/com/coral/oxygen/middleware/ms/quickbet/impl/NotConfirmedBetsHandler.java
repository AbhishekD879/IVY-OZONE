package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.*;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.ErrorMessageFactory;
import com.coral.oxygen.middleware.ms.quickbet.connector.OveraskReadBetExecutionService;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.BirResponse;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.ErrorMessage;
import com.coral.oxygen.middleware.ms.quickbet.converter.PlaceBetResponseAdapter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/** Handles overask and bet in run responses (not confirmed bets) */
@Component
public class NotConfirmedBetsHandler {
  private final OveraskReadBetExecutionService readBetExecutionService;

  @Autowired
  public NotConfirmedBetsHandler(OveraskReadBetExecutionService readBetExecutionService) {
    this.readBetExecutionService = readBetExecutionService;
  }

  public void handle(Session session, PlaceBetResponseAdapter betsResponse, String bppToken) {
    if (betsResponse.isOverask()) {
      session.sendData(PLACE_BET_OVERASK_RESPONSE_CODE.code(), betsResponse.getResponse());
      scheduleReadBet(session, betsResponse, bppToken);
    } else if (betsResponse.isBetInRun()) {
      session.sendData(
          PLACE_BET_BIR.code(),
          new BirResponse(betsResponse.getConfirmationExpectedAt(), betsResponse.getProvider()));
      scheduleReadBet(session, betsResponse, bppToken);
    } else {
      ErrorMessage errorMessage =
          ErrorMessageFactory.internalError(
              "Bet isn't confirmed, but isn't an overask nor bet in run");
      session.sendData(PLACE_BET_ERROR_RESPONSE_CODE.code(), errorMessage);
    }
  }

  private void scheduleReadBet(
      Session session, PlaceBetResponseAdapter betsResponse, String bppToken) {
    readBetExecutionService.scheduleReadBet(
        session, betsResponse.getBetsToRead(), bppToken, betsResponse.getConfirmationExpectedAt());
  }
}
