package com.ladbrokescoral.oxygen.listeners;

import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.Collection;
import java.util.List;
import java.util.regex.Pattern;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@Configuration
@Data
@ConditionalOnProperty(
    prefix = "leaderboard",
    value = "enabled",
    havingValue = "true",
    matchIfMissing = false)
@Slf4j
public class LeaderboardKafkaListener {

  private final SocketIOServer socketIOServer;
  private ThreadPoolTaskExecutor leaderboardExecutor;

  private static final int THREE = 3;
  private static final int FOUR = 4;
  private static final Pattern splitPattern = Pattern.compile("::");

  @Autowired
  public LeaderboardKafkaListener(
      SocketIOServer socketIOServer, ThreadPoolTaskExecutor leaderboardExecutor) {
    this.socketIOServer = socketIOServer;
    this.leaderboardExecutor = leaderboardExecutor;
  }

  @org.springframework.kafka.annotation.KafkaListener(
      topics = "${topic.showdown.response}",
      containerFactory = "kafkaLeaderboardUpdatesListenerContainerFactory")
  public void showdownResponse(ConsumerRecord<String, String> consumerRecord) {
    leaderboardExecutor.submit(() -> consumeShowdownResponse(socketIOServer, consumerRecord));
  }

  @org.springframework.kafka.annotation.KafkaListener(
      topics = "${topic.leaderboard.updates}",
      containerFactory = "kafkaLeaderboardUpdatesListenerContainerFactory")
  public void consumeLeaderboardUpdates(ConsumerRecord<String, String> consumerRecord) {
    leaderboardExecutor.submit(() -> consumeLeaderboardUpdate(socketIOServer, consumerRecord));
  }

  @org.springframework.kafka.annotation.KafkaListener(
      topics = "${topic.leaderboard.match.updates}",
      containerFactory = "kafkaLeaderboardUpdatesListenerContainerFactory")
  public void consumeLeaderboardMatchUpdates(ConsumerRecord<String, String> consumerRecord) {
    leaderboardExecutor.submit(() -> consumeLeaderboardMatchUpdate(socketIOServer, consumerRecord));
  }

  public void consumeShowdownResponse(
      SocketIOServer socketIOServer, ConsumerRecord<String, String> consumerRecord) {
    try {
      socketIOServer
          .getRoomOperations(consumerRecord.key())
          .sendEvent(
              consumerRecord.key(),
              new ObjectMapper().readValue(consumerRecord.value(), new TypeReference<Object>() {}));
      log.debug("Published Initial data :: {} :: {}", consumerRecord.key(), consumerRecord.value());
      Collection<SocketIOClient> clients =
          socketIOServer.getRoomOperations(consumerRecord.key()).getClients();
      int numberOfClients = clients.size();
      clients.forEach(client -> client.leaveRoom(consumerRecord.key()));
      log.debug(
          "Unsubscribed key for :: {} :: {} clients",
          consumerRecord.key(),
          numberOfClients
              - socketIOServer.getRoomOperations(consumerRecord.key()).getClients().size());
    } catch (Exception e) {
      log.error("Cannot parse LeaderBoard live update {}", e.getMessage(), e);
    }
  }

  @SuppressWarnings({"unchecked", "rawtypes"})
  public void consumeLeaderboardUpdate(
      SocketIOServer socketIOServer, ConsumerRecord<String, String> consumerRecord) {
    TypeReference type = null;
    try {
      int length = splitPattern.split(consumerRecord.key()).length;
      log.info("Channel length from leaderboard:{}", length);
      if (length == THREE || length == FOUR) {
        type = new TypeReference<Object>() {};
      } else {
        type = new TypeReference<List<Object>>() {};
      }
      socketIOServer
          .getRoomOperations(consumerRecord.key())
          .sendEvent(
              consumerRecord.key(), new ObjectMapper().readValue(consumerRecord.value(), type));
      log.info(
          "Published Leaderboard data :: {} :: {}", consumerRecord.key(), consumerRecord.value());
    } catch (Exception e) {
      log.error("Cannot parse My entries live update {}", e.getMessage(), e);
    }
  }

  public void consumeLeaderboardMatchUpdate(
      SocketIOServer socketIOServer, ConsumerRecord<String, String> consumerRecord) {
    try {
      socketIOServer
          .getRoomOperations(consumerRecord.key())
          .sendEvent(
              consumerRecord.key(),
              new ObjectMapper().readValue(consumerRecord.value(), new TypeReference<Object>() {}));
      log.info(
          "Published Match updates data :: {} :: {}", consumerRecord.key(), consumerRecord.value());
    } catch (Exception e) {
      log.error("Cannot parse Match updates {}", e.getMessage());
    }
  }
}
