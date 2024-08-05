package com.ladbrokescoral.oxygen.listeners;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.corundumstudio.socketio.listener.DataListener;
import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.dto.messages.Envelope;
import com.ladbrokescoral.oxygen.service.KafkaPublisherImpl;
import com.ladbrokescoral.oxygen.service.RedisOperations;
import com.ladbrokescoral.oxygen.utils.MessageUtils;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import java.util.List;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class SubscribeOnChannelsListener implements DataListener<List<String>> {

  private final SocketIOServer socketIOServer;
  private final KafkaPublisherImpl kafkaPublisherImpl;
  private final RedisOperations redisOperations;

  private final Gson gson;
  private final ThrottleLogic throttleLogic;

  public SubscribeOnChannelsListener(
      SocketIOServer socketIOServer,
      KafkaPublisherImpl kafkaPublisherImpl,
      RedisOperations redisOperations,
      Gson gson,
      ThrottleLogic throttleLogic) {
    this.socketIOServer = socketIOServer;
    this.kafkaPublisherImpl = kafkaPublisherImpl;
    this.redisOperations = redisOperations;
    this.gson = gson;
    this.throttleLogic = throttleLogic;
  }

  @Trace(dispatcher = true)
  @Override
  public void onData(SocketIOClient client, List<String> data, AckRequest ackSender) {
    NewRelic.recordMetric("ActiveConnections", socketIOServer.getAllClients().size());
    log.info("SubscribeOnChannelsListener-onData list of channels {}", data);
    if (throttleLogic.hackerDetected(client, data)) {
      return;
    }
    if (client.isChannelOpen()) {
      data.stream()
          .filter(channel -> !channel.startsWith("SEVENT") && !isLeadboardChannel(channel))
          .forEach(
              channel -> {
                if (!client.getAllRooms().contains(channel)) {
                  client.joinRoom(channel);
                }
                kafkaPublisherImpl.publish(channel, null);
                sendLastMessageToClient(channel, client);
              });
      log.debug("Were processed {} subscriptions for client {}", data, client.getSessionId());
    } else {
      log.info("Client got disconected with IP:{}", client.getHandshakeData().getAddress());
      client.disconnect();
    }
  }

  private boolean isLeadboardChannel(String channel) {
    return (channel.startsWith("EVENT")
        || channel.startsWith("SCORE")
        || channel.startsWith("CLOCK"));
  }

  private void sendLastMessageToClient(String channel, SocketIOClient client) {
    redisOperations
        .getLastMessage(channel)
        .thenApply(
            optionalMessage -> {
              optionalMessage.ifPresent(
                  message -> {
                    log.trace(
                        "Response from channel {} for client {}: {}",
                        channel,
                        client.getSessionId(),
                        message.getMessage());
                    Envelope envelope = gson.fromJson(message.getMessage(), Envelope.class);
                    MessageUtils.notify(
                        channel,
                        MessageUtils.convert(envelope, gson),
                        client,
                        "lastmessage/success");
                  });
              return null;
            });
  }
}
