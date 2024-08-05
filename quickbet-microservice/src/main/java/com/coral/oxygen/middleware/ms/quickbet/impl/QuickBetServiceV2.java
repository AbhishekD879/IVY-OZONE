package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.LOGIN_SUCCESS;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.LOGOUT_SUCCESS;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.UIPlaceBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.AddComplexSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.AddSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.RemoveComplexSelectionRequest;
import java.time.Duration;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Component;

@Component
public class QuickBetServiceV2 {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  private static final Duration DURATION_TO_LOCK = Duration.ofSeconds(2);

  private SelectionOperations selectionOperations;
  private PlaceBetOperations placeBetOperations;
  private OnceExecutor onceExecutor;

  QuickBetServiceV2(
      SelectionOperations selectionOperations,
      PlaceBetOperations placeBetOperations,
      OnceExecutor onceExecutor) {
    this.selectionOperations = selectionOperations;
    this.placeBetOperations = placeBetOperations;
    this.onceExecutor = onceExecutor;
  }

  public void login(Session session, String bppToken) {
    ASYNC_LOGGER.info("Login using token: {}", bppToken);

    session.setToken(bppToken);
    session.save();

    session.sendData(LOGIN_SUCCESS.code(), "{}");
  }

  public void logout(Session session) {
    ASYNC_LOGGER.info("Logout for token: {}", session.getToken());

    session.setToken(null);
    session.save();

    session.sendData(LOGOUT_SUCCESS.code(), "{}");
  }

  public void addSelection(Session session, AddSelectionRequest request) {
    selectionOperations.addSelection(session, request);
  }

  public void removeOneSelection(Session session, String outcomeId) {
    selectionOperations.removeSelection(session, outcomeId);
  }

  public void addComplexSelection(Session session, AddComplexSelectionRequest request) {
    selectionOperations.addComplexSelection(session, request);
  }

  public void removeComplexSelection(Session session, RemoveComplexSelectionRequest request) {
    selectionOperations.removeComplexSelection(session, request);
  }

  public void placeBet(Session session, UIPlaceBetRequest placeBetRequest) {
    String bppToken = session.getToken();
    onceExecutor.executeOnceDuringTimePeriod(
        bppToken,
        () -> placeBetOperations.placeBet(session, placeBetRequest),
        () ->
            ASYNC_LOGGER.error(
                "[REGULAR] Duplicated request for place bet with token {}", bppToken),
        DURATION_TO_LOCK);
  }
}
