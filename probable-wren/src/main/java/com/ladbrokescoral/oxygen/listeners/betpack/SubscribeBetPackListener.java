package com.ladbrokescoral.oxygen.listeners.betpack;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.listener.DataListener;
import com.ladbrokescoral.oxygen.dto.messages.BetPackMessage;
import com.ladbrokescoral.oxygen.listeners.ThrottleLogic;
import com.ladbrokescoral.oxygen.service.BetPackKafkaPublisher;
import com.ladbrokescoral.oxygen.service.betpack.BetPackRedisOperations;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class SubscribeBetPackListener implements DataListener<List<String>> {

  private final BetPackKafkaPublisher betPackKafkaPublisher;
  private final BetPackRedisOperations betPackRedisOperations;

  private final ThrottleLogic throttleLogic;

  public SubscribeBetPackListener(
      BetPackKafkaPublisher betPackKafkaPublisher,
      BetPackRedisOperations betPackRedisOperations,
      ThrottleLogic throttleLogic) {
    this.betPackKafkaPublisher = betPackKafkaPublisher;
    this.betPackRedisOperations = betPackRedisOperations;
    this.throttleLogic = throttleLogic;
  }

  @Override
  public void onData(SocketIOClient client, List<String> data, AckRequest ackSender) {
    if (throttleLogic.hackerDetected(client, data)) {
      return;
    }
    String betPackOfferIds = String.join(",", data);
    log.info("bet pack subscriptions :{}", betPackOfferIds);

    if (client.isChannelOpen()) {
      data.forEach((String betPack) -> processBetPacks(betPack, client));
      log.debug("Were processed {} subscriptions for client {}", data, client.getSessionId());
    } else {
      log.info("Client got disconnected with IP:{}", client.getHandshakeData().getAddress());
      client.disconnect();
    }
  }

  private void processBetPacks(String betPack, SocketIOClient client) {
    if (!client.getAllRooms().contains(betPack)) {
      client.joinRoom(betPack);
    }
    betPackRedisOperations
        .getLastMessage(betPack)
        .thenAccept(
            (Optional<BetPackMessage> optionalMessage) -> {
              if (optionalMessage.isPresent()) {
                BetPackMessage betPackMessage = optionalMessage.get();
                log.info(
                    "Response from bet pack {} for client {}: {}",
                    betPack,
                    client.getSessionId(),
                    betPackMessage.getMessage());
                client.sendEvent(betPack, betPackMessage.getMessage());
              } else {
                betPackKafkaPublisher.publish(betPack, betPack);
              }
            });
  }
}
