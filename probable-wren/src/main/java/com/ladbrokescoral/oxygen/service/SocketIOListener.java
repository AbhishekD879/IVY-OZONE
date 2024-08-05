package com.ladbrokescoral.oxygen.service;

import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.corundumstudio.socketio.listener.DataListener;
import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.listeners.IncidentsListener;
import com.ladbrokescoral.oxygen.listeners.IncidentsUnsubscribeListener;
import com.ladbrokescoral.oxygen.listeners.MatchFactCodesListener;
import com.ladbrokescoral.oxygen.listeners.ScoreboardUsunscribeListener;
import com.ladbrokescoral.oxygen.listeners.SubscribeOnChannelsListener;
import com.ladbrokescoral.oxygen.listeners.ThrottleLogic;
import com.ladbrokescoral.oxygen.listeners.UnsubscribeOnChannelsListener;
import com.ladbrokescoral.oxygen.listeners.betpack.SubscribeBetPackListener;
import com.ladbrokescoral.oxygen.listeners.betpack.UnsubscribeBetPackListener;
import com.ladbrokescoral.oxygen.service.betpack.BetPackRedisOperations;
import com.ladbrokescoral.oxygen.utils.EnvironmentProvider;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import java.text.MessageFormat;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import lombok.extern.slf4j.Slf4j;
import lombok.val;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Service
public class SocketIOListener implements Listener {

  private static final String SUBSCRIBE_TOPIC = "subscribe";
  private static final String UNSUBSCRIBE_TOPIC = "unsubscribe";
  private static final String BET_PACK_SUBSCRIBE_TOPIC = "bet-pack-subscribe";
  private static final String BET_PACK_UNSUBSCRIBE_TOPIC = "bet-pack-unsubscribe";
  private final SocketIOServer socketIOServer;
  private final EnvironmentProvider environmentProvider;
  private final KafkaPublisherImpl kafkaPublisherImpl;
  private final RedisOperations redisOperations;
  private final Gson gson = new Gson();
  private final ThrottleLogic throttleLogic;
  private final DataListener<String> scoreboardListener;
  private LeaderboardSocketIOHelper leaderboardSocketIOHelper;
  final DataListener<String> incidentsListener;
  private LeaderboardSubscriptionHelper leaderboardSubscriptionHelper;
  private final BetPackKafkaPublisher betPackKafkaPublisher;
  private final BetPackRedisOperations betPackRedisOperations;
  private final DataListener<List<String>> matchFactCodesListener;

  @Autowired
  public SocketIOListener(
      SocketIOServer socketIOServer,
      EnvironmentProvider environmentProvider,
      Gson gson,
      KafkaPublisherImpl kafkaPublisherImpl,
      RedisOperations redisOperations,
      Optional<LeaderboardSocketIOHelper> leaderboardSocketIOHelper,
      ThrottleLogic throttleLogic,
      DataListener<String> scoreboardListener,
      IncidentsListener incidentsListener,
      Optional<LeaderboardSubscriptionHelper> leaderboardSubscriptionHelper,
      BetPackKafkaPublisher betPackKafkaPublisher,
      BetPackRedisOperations betPackRedisOperations,
      MatchFactCodesListener matchFactCodesListener) {

    this.socketIOServer = socketIOServer;
    this.environmentProvider = environmentProvider;
    this.kafkaPublisherImpl = kafkaPublisherImpl;
    this.redisOperations = redisOperations;
    this.scoreboardListener = scoreboardListener;
    this.betPackKafkaPublisher = betPackKafkaPublisher;
    this.betPackRedisOperations = betPackRedisOperations;
    if (leaderboardSocketIOHelper.isPresent()) {
      this.leaderboardSocketIOHelper = leaderboardSocketIOHelper.get();
    }
    this.throttleLogic = throttleLogic;
    this.incidentsListener = incidentsListener;
    this.matchFactCodesListener = matchFactCodesListener;
    if (leaderboardSubscriptionHelper.isPresent()) {
      this.leaderboardSubscriptionHelper = leaderboardSubscriptionHelper.get();
    }
  }

  @Trace(dispatcher = true)
  public void onConnect(SocketIOClient client) {

    NewRelic.setTransactionName(null, "connect");

    String onConnectMessageTemplate = "Connection was opened for: <{0}>, from {1}";
    log.debug(
        MessageFormat.format(
            onConnectMessageTemplate, client.getSessionId(), client.getRemoteAddress()));
    String connectionsMetric = "Concurrent/onConnect";
    NewRelic.incrementCounter(connectionsMetric);
    log.info(
        "Concurrent/onConnect Client session : {} Remote Adress : {}",
        client.getSessionId(),
        client.getRemoteAddress());
    Map<String, String> versionDescription = new HashMap<>();

    versionDescription.put("version", environmentProvider.getEnvironmentVariable("git.branch"));
    versionDescription.put("id", environmentProvider.getEnvironmentVariable("git.commit.id"));

    String versionRoomTemplate = "version";
    client.sendEvent(versionRoomTemplate, versionDescription);
  }

  @Trace(dispatcher = true)
  public void onDisconnect(SocketIOClient client) {
    NewRelic.setTransactionName(null, "disconnect");
    String onDisconnectMessageTemplate = "Connection was closed for: <{0}>, from {1}";
    log.debug(
        MessageFormat.format(
            onDisconnectMessageTemplate, client.getSessionId(), client.getRemoteAddress()));
    String disconnectionsMetric = "Concurrent/onDisconnect";
    log.info(
        "Concurrent/onDisconnect Client session : {} Remote Adress : {}",
        client.getSessionId(),
        client.getRemoteAddress());
    NewRelic.incrementCounter(disconnectionsMetric);
    String sessionId = client.getSessionId().toString();
    Set<String> channels = client.getAllRooms();
    if (Objects.nonNull(leaderboardSubscriptionHelper))
      leaderboardSubscriptionHelper.clearShowdownSubscriptions(sessionId, channels);
    if (!CollectionUtils.isEmpty(channels)) {
      channels.forEach(client::leaveRoom);
    }
  }

  @Override
  public void start() {

    DataListener<List<String>> onSubscribeListener =
        new SubscribeOnChannelsListener(
            socketIOServer, kafkaPublisherImpl, redisOperations, gson, throttleLogic);
    DataListener<List<String>> onUnsubscribeListener = new UnsubscribeOnChannelsListener();
    @SuppressWarnings("unchecked")
    val typeOfPayload = (Class<List<String>>) (Object) List.class;

    this.socketIOServer.addConnectListener(this::onConnect);
    this.socketIOServer.addDisconnectListener(this::onDisconnect);
    this.socketIOServer.addEventListener(SUBSCRIBE_TOPIC, typeOfPayload, onSubscribeListener);
    this.socketIOServer.addEventListener(UNSUBSCRIBE_TOPIC, typeOfPayload, onUnsubscribeListener);
    socketIOServer.addEventListener("scoreboard", String.class, scoreboardListener);
    this.socketIOServer.addEventListener(
        "unsubscribeScoreboard", String.class, new ScoreboardUsunscribeListener());
    this.socketIOServer.addEventListener("subMatchCmtry", String.class, incidentsListener);
    this.socketIOServer.addEventListener(
        "unsubMatchCmtry", String.class, new IncidentsUnsubscribeListener());
    this.socketIOServer.addEventListener("subLastMatchCode", typeOfPayload, matchFactCodesListener);
    if (Objects.nonNull(leaderboardSocketIOHelper))
      leaderboardSocketIOHelper.regShowdownListener(this.socketIOServer);

    DataListener<List<String>> onSubscribeBetPackListener =
        new SubscribeBetPackListener(betPackKafkaPublisher, betPackRedisOperations, throttleLogic);
    DataListener<List<String>> onUnsubscribeBetPackListener = new UnsubscribeBetPackListener();

    this.socketIOServer.addEventListener(
        BET_PACK_SUBSCRIBE_TOPIC, typeOfPayload, onSubscribeBetPackListener);
    this.socketIOServer.addEventListener(
        BET_PACK_UNSUBSCRIBE_TOPIC, typeOfPayload, onUnsubscribeBetPackListener);

    this.socketIOServer.start();
  }

  @Override
  public void stop() {
    this.socketIOServer
        .getAllClients()
        .forEach(
            socketIOClient -> {
              Set<String> channels = socketIOClient.getAllRooms();
              if (Objects.nonNull(leaderboardSubscriptionHelper))
                leaderboardSubscriptionHelper.clearShowdownSubscriptions(
                    socketIOClient.getSessionId().toString(), channels);
              channels.forEach(socketIOClient::leaveRoom);
            });
    this.socketIOServer.stop();
  }
}
