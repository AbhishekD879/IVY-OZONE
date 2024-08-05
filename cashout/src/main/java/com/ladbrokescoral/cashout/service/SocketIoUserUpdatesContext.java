package com.ladbrokescoral.cashout.service;

import com.coral.bpp.api.model.bet.api.response.oxi.base.Bet;
import com.corundumstudio.socketio.BroadcastOperations;
import com.corundumstudio.socketio.SocketIOServer;
import com.ladbrokescoral.cashout.model.response.ErrorBetResponse;
import com.ladbrokescoral.cashout.model.response.UpdateBetResponse;
import com.ladbrokescoral.cashout.model.response.UpdateCashoutResponse;
import com.ladbrokescoral.cashout.service.updates.UserUpdateTrigger;
import com.ladbrokescoral.cashout.service.updates.UserUpdateTriggerDto;
import com.newrelic.api.agent.NewRelic;
import lombok.RequiredArgsConstructor;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

@Component
@RequiredArgsConstructor
public class SocketIoUserUpdatesContext implements UserUpdatesContext, UserUpdateTrigger {

  private final SocketIOServer socketIOServer;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Override
  public void sendBetUpdate(String emitKey, UpdateBetResponse updateBetResponse) {
    BroadcastOperations roomOperations = socketIOServer.getRoomOperations(emitKey);
    roomOperations.sendEvent("betUpdate", updateBetResponse);
    NewRelic.incrementCounter("Custom/SocketIO/Updates/BetUpdate");
    int clientsInRoom = roomOperations.getClients().size();
    NewRelic.incrementCounter("Custom/SocketIO/Updates/BetUpdateTotalClients", clientsInRoom);
    ASYNC_LOGGER.debug(
        "Sent betUpdate={} in room {} [{}]", updateBetResponse, emitKey, clientsInRoom);
  }

  @Override
  public void sendBetUpdateError(String emitKey, ErrorBetResponse errorBetResponse) {
    BroadcastOperations roomOperations = socketIOServer.getRoomOperations(emitKey);
    roomOperations.sendEvent("betUpdate", errorBetResponse);
    NewRelic.incrementCounter("Custom/SocketIO/Updates/BetUpdateError");
    int clientsInRoom = roomOperations.getClients().size();
    NewRelic.incrementCounter("Custom/SocketIO/Updates/BetUpdateErrorTotalClients", clientsInRoom);
    ASYNC_LOGGER.debug(
        "Sent betUpdateError={} in room {} [{}]", errorBetResponse, emitKey, clientsInRoom);
  }

  @Override
  public void sendCashoutUpdate(String emitKey, UpdateCashoutResponse updateCashoutResponse) {
    BroadcastOperations roomOperations = socketIOServer.getRoomOperations(emitKey);
    roomOperations.sendEvent("cashoutUpdate", updateCashoutResponse);
    NewRelic.incrementCounter("Custom/SocketIO/Updates/CashoutUpdate");
    int clientsInRoom = roomOperations.getClients().size();
    NewRelic.incrementCounter("Custom/SocketIO/Updates/CashoutUpdateTotalClients", clientsInRoom);
    ASYNC_LOGGER.debug(
        "Sent cashoutUpdate={} in room {} [{}]", updateCashoutResponse, emitKey, clientsInRoom);
  }

  @Override
  public void triggerCashoutSuspension(UserUpdateTriggerDto suspensionDto) {
    if (suspensionDto != null && !CollectionUtils.isEmpty(suspensionDto.getBetIds())) {
      suspensionDto.getBetIds().stream()
          .map(this::cashoutSuspendedBet)
          .map(UpdateBetResponse::new)
          .forEach(response -> sendBetUpdate(suspensionDto.getToken(), response));
    }
  }

  @Override
  public void triggerBetSettled(UserUpdateTriggerDto suspensionDto) {
    if (suspensionDto != null && !CollectionUtils.isEmpty(suspensionDto.getBetIds())) {
      suspensionDto.getBetIds().stream()
          .map(this::settledBet)
          .forEach(bet -> sendBetUpdate(bet.getBetId(), new UpdateBetResponse(bet)));
    }
  }

  private Bet cashoutSuspendedBet(String betId) {
    Bet bet = new Bet();
    bet.setBetId(betId);
    bet.setCashoutValue("CASHOUT_SELN_SUSPENDED");
    bet.setCashoutStatus("Suspended by cashout microservice: bet has suspended selection(s)");
    return bet;
  }

  private Bet settledBet(String betId) {
    Bet bet = new Bet();
    bet.setBetId(betId);
    bet.setCashoutValue("BET_SETTLED");
    bet.setSettled("Y");
    return bet;
  }
}
