package com.ladbrokescoral.cashout.socketio;

import com.coral.bpp.api.exception.BppUnauthorizedException;
import com.coral.bpp.api.model.bet.api.request.AccountHistoryRequest;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.annotation.OnConnect;
import com.corundumstudio.socketio.annotation.OnDisconnect;
import com.corundumstudio.socketio.annotation.OnEvent;
import com.ladbrokescoral.cashout.api.client.entity.request.BetUpdateRequest;
import com.ladbrokescoral.cashout.bpptoken.BppToken;
import com.ladbrokescoral.cashout.bpptoken.BppTokenOperations;
import com.ladbrokescoral.cashout.model.Code;
import com.ladbrokescoral.cashout.model.response.ErrorBetResponse;
import com.ladbrokescoral.cashout.model.response.InitialAccountHistoryBetResponse;
import com.ladbrokescoral.cashout.payout.PayoutUpdatesPublisher;
import com.ladbrokescoral.cashout.service.AccountHistoryService;
import com.ladbrokescoral.cashout.service.BetUpdateService;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class SocketIoController {
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  private final AccountHistoryService accountHistoryService;
  private final BetUpdateService betUpdateService;
  private final BppTokenOperations bppTokenOperations;
  private final PayoutUpdatesPublisher payoutUpdatesPublisher;

  @OnConnect
  @Trace(dispatcher = true)
  public void onConnect(SocketIOClient client) {
    AccountHistoryRequest accountHistoryRequest = getAccountHistoryRequestFromQuery(client);
    String bppToken = accountHistoryRequest.getToken();
    ASYNC_LOGGER.info("Client {} with token {} connected", client.getSessionId(), bppToken);

    try {
      BppToken bppTokenWrapper = bppTokenOperations.parseToken(bppToken);
      accountHistoryService
          .accountHistoryInitBets(accountHistoryRequest)
          .doOnNext(resp -> sendInitialUpdate(client, resp))
          // .map(BetUtil::filterAccHistoryBetsWithCashoutValuePresent)
          .doOnNext(resp -> client.joinRoom(bppToken))
          .doOnNext(resp -> subscribeOnBetIds(resp.getBets(), client))
          .doOnNext(
              resp ->
                  betUpdateService.createSubscriptionInInternalPubSub(
                      client.getSessionId(),
                      bppTokenWrapper,
                      client.getHandshakeData().getTime(),
                      resp.getBets()))
          .doOnError(
              ex -> {
                ASYNC_LOGGER.error(
                    "[{}][{}] Error on initial accountHistory request with exception [{}]",
                    client.getSessionId(),
                    bppToken,
                    ex.getMessage());
                sendInitialUpdate(client, ErrorBetResponse.create(Code.fromException(ex)));
                betUpdateService.unsubscribeInInternalPubSub(client.getSessionId());
                client.disconnect();
              })
          .subscribe();
    } catch (BppUnauthorizedException e) {
      sendInitialUpdate(client, ErrorBetResponse.create(Code.fromException(e)));
      client.disconnect();
    }
  }

  private void sendInitialUpdate(SocketIOClient client, Object data) {
    if (data instanceof InitialAccountHistoryBetResponse) {
      payoutUpdatesPublisher.sendInitialUpdates(client, "initial", data);
    } else {
      client.sendEvent("initial", data);
    }
  }

  private void subscribeOnBetIds(List<BetSummaryModel> betSummaryModels, SocketIOClient client) {
    Set<String> betIds =
        betSummaryModels.stream().map(BetSummaryModel::getId).collect(Collectors.toSet());

    ASYNC_LOGGER.debug("Joining client {} to rooms(betIds) {}", client.getSessionId(), betIds);
    betIds.forEach(client::joinRoom);
  }

  private String getBppTokenFromQuery(SocketIOClient client) {
    return client.getHandshakeData().getSingleUrlParam("token");
  }

  @OnDisconnect
  @Trace(dispatcher = true)
  public void onDisconnect(SocketIOClient client) {
    String bppToken = getBppTokenFromQuery(client);
    ASYNC_LOGGER.info("Client {} with token {} disconnected", client.getSessionId(), bppToken);
    NewRelic.addCustomParameter("socketIoClientId", client.getSessionId().toString());
    NewRelic.addCustomParameter("bppToken", bppToken);

    betUpdateService.unsubscribeInInternalPubSub(client.getSessionId());
  }

  private AccountHistoryRequest getAccountHistoryRequestFromQuery(SocketIOClient client) {
    return AccountHistoryRequest.builder()
        .token(client.getHandshakeData().getSingleUrlParam("token"))
        .pagingBlockSize(client.getHandshakeData().getSingleUrlParam("pagingBlockSize"))
        .group(client.getHandshakeData().getSingleUrlParam("group"))
        .detailLevel(client.getHandshakeData().getSingleUrlParam("detailLevel"))
        .settled(client.getHandshakeData().getSingleUrlParam("settled"))
        .fromDate(client.getHandshakeData().getSingleUrlParam("fromDate"))
        .toDate(client.getHandshakeData().getSingleUrlParam("toDate"))
        .build();
  }

  @OnEvent("nextBets")
  public void onEvent(SocketIOClient client, Map<String, Object> requestDataMap) {
    ASYNC_LOGGER.info("nextBets onEvent method {}", requestDataMap);
    BetUpdateRequest betUpdateRequest = new BetUpdateRequest(requestDataMap);
    String bppToken = betUpdateRequest.getToken();
    try {
      BppToken bppTokenWrapper = bppTokenOperations.parseToken(bppToken);
      accountHistoryService
          .accountHistoryInitBets(
              AccountHistoryRequest.builder()
                  .pagingToken(betUpdateRequest.getPagingToken())
                  .token(betUpdateRequest.getToken())
                  .blockSize(betUpdateRequest.getBlockSize())
                  .detailLevel(betUpdateRequest.getDetailLevel())
                  .group(betUpdateRequest.getGroup())
                  .build())
          .doOnNext(resp -> sendNextBetsUpdate(client, resp))
          // .map(BetUtil::filterAccHistoryBetsWithCashoutValuePresent)
          .doOnNext(resp -> client.joinRoom(bppToken))
          .doOnNext(resp -> subscribeOnBetIds(resp.getBets(), client))
          .doOnNext(
              resp ->
                  betUpdateService.createSubscriptionInInternalPubSub(
                      client.getSessionId(),
                      bppTokenWrapper,
                      client.getHandshakeData().getTime(),
                      resp.getBets()))
          .doOnError(
              (Throwable exc) -> {
                ASYNC_LOGGER.error(
                    "[{}][{}] Error on nextBets accountHistory request with exception [{}]",
                    client.getSessionId(),
                    bppToken,
                    exc.getMessage());
                sendNextBetsUpdate(client, ErrorBetResponse.create(Code.fromException(exc)));
                betUpdateService.unsubscribeInInternalPubSub(client.getSessionId());
                client.disconnect();
              })
          .subscribe();
    } catch (BppUnauthorizedException e) {
      ASYNC_LOGGER.error("nextBets Event processing failed for openBets {}", e.getMessage());
      sendNextBetsUpdate(client, ErrorBetResponse.create(Code.fromException(e)));
      client.disconnect();
    }
  }

  private void sendNextBetsUpdate(SocketIOClient client, Object data) {
    if (data instanceof InitialAccountHistoryBetResponse) {
      payoutUpdatesPublisher.sendInitialUpdates(client, "nextBetsUpdate", data);
    } else {
      client.sendEvent("nextBetsUpdate", data);
    }
  }

  @OnEvent("initialBets")
  public void onInitialEvent(SocketIOClient client, Map<String, Object> requestDataMap) {
    BetUpdateRequest betUpdateRequest = new BetUpdateRequest(requestDataMap);
    String bppToken = betUpdateRequest.getToken();

    try {
      BppToken bppTokenWrapper = bppTokenOperations.parseToken(bppToken);
      accountHistoryService
          .accountHistoryInitBets(
              AccountHistoryRequest.builder()
                  .token(betUpdateRequest.getToken())
                  .group(betUpdateRequest.getGroup())
                  .pagingBlockSize(betUpdateRequest.getPagingBlockSize())
                  .detailLevel(betUpdateRequest.getDetailLevel())
                  .settled(betUpdateRequest.getSettled())
                  .fromDate(betUpdateRequest.getFromDate())
                  .toDate(betUpdateRequest.getToDate())
                  .ev_category_id(betUpdateRequest.getEv_category_id())
                  .bet_type(betUpdateRequest.getBet_type())
                  .pool_type_id(betUpdateRequest.getPool_type_id())
                  .game_def(betUpdateRequest.getGame_def())
                  .build())
          .doOnNext(resp -> sendInitialUpdate(client, resp))
          //  .map(BetUtil::filterAccHistoryBetsWithCashoutValuePresent)
          .doOnNext(resp -> client.joinRoom(bppToken))
          .doOnNext(resp -> subscribeOnBetIds(resp.getBets(), client))
          .doOnNext(
              resp ->
                  betUpdateService.createSubscriptionInInternalPubSub(
                      client.getSessionId(),
                      bppTokenWrapper,
                      client.getHandshakeData().getTime(),
                      resp.getBets()))
          .doOnError(
              (Throwable exe) -> {
                ASYNC_LOGGER.error(
                    "[{}][{}] Error on initialBets accountHistory request with exception [{}]",
                    client.getSessionId(),
                    bppToken,
                    exe.getMessage());
                sendInitialUpdate(client, ErrorBetResponse.create(Code.fromException(exe)));
                betUpdateService.unsubscribeInInternalPubSub(client.getSessionId());
                client.disconnect();
              })
          .subscribe();
    } catch (BppUnauthorizedException e) {
      ASYNC_LOGGER.error("initialBets Event processing failed for openBets {}", e.getMessage());
      sendInitialUpdate(client, ErrorBetResponse.create(Code.fromException(e)));
      client.disconnect();
    }
  }
}
