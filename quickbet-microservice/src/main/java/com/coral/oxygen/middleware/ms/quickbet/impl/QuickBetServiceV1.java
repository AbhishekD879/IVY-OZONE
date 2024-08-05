package com.coral.oxygen.middleware.ms.quickbet.impl;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.BanachSelection;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.LuckyDipBetPlacementRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.RegularPlaceBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachPlaceBetRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachSelectionRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.FreeBetForChannelRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest;
import java.time.Duration;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Component;

/**
 * This is old version of QuickBet API, it is currently used in quickbet widget in frontend.
 * QuickBetServiceV2 should be used in any future development.
 */
@Deprecated
@Component
public class QuickBetServiceV1 {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  private static final Duration DURATION_TO_LOCK = Duration.ofSeconds(2);

  private final SelectionOperations selectionOperations;
  private final BanachBetsOperations banachBetsOperations;
  private final FreeBetForChannelOperations freeBetForChannelOperations;
  private final OnceExecutor onceExecutor;
  private final RegularPlaceBetOperationHandler regularPlaceBetOperationHandler;
  private final RegularSelectionOperationHandler regularSelectionOperationHandler;
  private final LuckDipPlaceBetOperationHandler luckDipPlaceBetOperationHandler;

  public QuickBetServiceV1(
      SelectionOperations selectionOperations,
      BanachBetsOperations banachBetsOperations,
      FreeBetForChannelOperations freeBetForChannelOperations,
      OnceExecutor onceExecutor,
      RegularPlaceBetOperationHandler regularPlaceBetOperationHandler,
      RegularSelectionOperationHandler regularSelectionOperationHandler,
      LuckDipPlaceBetOperationHandler luckDipPlaceBetOperationHandler) {
    this.selectionOperations = selectionOperations;
    this.banachBetsOperations = banachBetsOperations;
    this.freeBetForChannelOperations = freeBetForChannelOperations;
    this.onceExecutor = onceExecutor;
    this.regularPlaceBetOperationHandler = regularPlaceBetOperationHandler;
    this.regularSelectionOperationHandler = regularSelectionOperationHandler;
    this.luckDipPlaceBetOperationHandler = luckDipPlaceBetOperationHandler;
  }

  public void addRegularSelection(Session session, RegularSelectionRequest request) {
    regularSelectionOperationHandler.addSelection(session, request);
  }

  public void addBanachSelection(
      Session session, BanachSelectionRequestData banachSelectionRequestData) {
    banachBetsOperations.addSelection(session, new BanachSelection(banachSelectionRequestData));
  }

  public void placeBanachBet(Session session, BanachPlaceBetRequestData requestData) {
    String bppToken = requestData.getToken();
    onceExecutor.executeOnceDuringTimePeriod(
        bppToken,
        () -> banachBetsOperations.placeBet(session, requestData),
        () -> ASYNC_LOGGER.error("[BYB] Duplicated request for place bet with token {}", bppToken),
        DURATION_TO_LOCK);
  }

  public void addFreeBetTokensForChannel(
      Session session, FreeBetForChannelRequestData requestData) {
    freeBetForChannelOperations.requestFreeBetTokensForChannel(session, requestData);
  }

  public void clearSelection(Session session) {
    selectionOperations.clearSelection(session);
    banachBetsOperations.clearSelection(session);
  }

  public void restoreState(Session session, String bppToken) {
    regularSelectionOperationHandler.restoreState(session);
    banachBetsOperations.restoreState(session);
    selectionOperations.restoreState(session, bppToken);
  }

  public void placeRegularBet(Session session, RegularPlaceBetRequest request) {
    String bppToken = request.getToken();
    onceExecutor.executeOnceDuringTimePeriod(
        bppToken,
        () -> regularPlaceBetOperationHandler.placeBet(session, request),
        () ->
            ASYNC_LOGGER.error(
                "[REGULAR] Duplicated request for place bet with token {}", bppToken),
        DURATION_TO_LOCK);
  }

  public void placeLuckyDipBet(Session session, LuckyDipBetPlacementRequest request) {
    String bppToken = request.getToken();
    onceExecutor.executeOnceDuringTimePeriod(
        bppToken,
        () -> luckDipPlaceBetOperationHandler.processLuckyDipPlaceBet(session, request),
        () ->
            ASYNC_LOGGER.error(
                "[REGULAR] Duplicated request for place bet with token {}", bppToken),
        DURATION_TO_LOCK);
  }
}
