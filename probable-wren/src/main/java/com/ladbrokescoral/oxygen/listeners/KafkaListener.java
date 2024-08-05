package com.ladbrokescoral.oxygen.listeners;

import com.corundumstudio.socketio.SocketIOServer;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.dto.messages.Envelope;
import com.ladbrokescoral.oxygen.dto.messages.SimpleMessage;
import com.ladbrokescoral.oxygen.service.IncidentsDataProcessor;
import com.ladbrokescoral.oxygen.service.RedisOperations;
import com.ladbrokescoral.oxygen.utils.MessageUtils;
import com.newrelic.api.agent.NewRelic;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import lombok.extern.slf4j.Slf4j;
import lombok.val;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.concurrent.CustomizableThreadFactory;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@Configuration
@Slf4j
public class KafkaListener {

  private final SocketIOServer socketIOServer;
  private final ExecutorService executor;
  private final Gson gson;
  private static final String FACT_MSG = "sFACTS";
  private final IncidentsDataProcessor incidentsDataProcessor;
  private final RedisOperations redisOperations;

  @Autowired
  public KafkaListener(
      SocketIOServer socketIOServer,
      RedisOperations redisOperations,
      Gson gson,
      @Value("${liveserve.executor-threads:100}") int executorThreads,
      ThreadPoolTaskExecutor leaderboardExecutor,
      IncidentsDataProcessor incidentsDataProcessor) {
    this.socketIOServer = socketIOServer;
    this.redisOperations = redisOperations;
    this.gson = gson;
    executor =
        Executors.newFixedThreadPool(
            executorThreads, new CustomizableThreadFactory("liveupdates-"));
    this.incidentsDataProcessor = incidentsDataProcessor;
  }

  @org.springframework.kafka.annotation.KafkaListener(
      topics = "${topic.live-updates}",
      containerFactory = "kafkaLiveupdatesListenerContainerFactory")
  public void consume(ConsumerRecord<String, String> record) {
    String message = record.value();
    NewRelic.recordMetric(
        "PublishingDelayBeforeThreadPool",
        (float) (System.currentTimeMillis() - record.timestamp()));
    executor.submit(
        () -> {
          try {
            log.debug("Message received from Kafka: {}", message);
            val messageObject = gson.fromJson(message, Envelope.class);
            val channel = messageObject.getChannel();

            NewRelic.recordMetric(
                "PublishingDelay", (float) (System.currentTimeMillis() - record.timestamp()));

            MessageUtils.toMessage(messageObject, gson)
                .ifPresent(
                    data -> socketIOServer.getRoomOperations(channel).sendEvent(channel, data));
            redisOperations.saveLastMessage(new SimpleMessage(channel, message));

          } catch (Exception e) {
            log.error(e.getMessage(), e);
            NewRelic.noticeError(e);
          }
        });
  }

  @org.springframework.kafka.annotation.KafkaListener(
      topics = "${topic.scoreboards}",
      containerFactory = "kafkaScoreboardsListenerContainerFactory")
  public void consumeScoreboard(ConsumerRecord<String, String> record) {
    try {
      socketIOServer
          .getRoomOperations(record.key())
          .sendEvent(
              record.key(),
              new ObjectMapper()
                  .readValue(record.value(), new TypeReference<Map<String, Object>>() {}));
    } catch (JsonProcessingException e) {
      log.error("Cannot parse scoreboard live update {}", e.getMessage());
    }
  }

  /**
   * Consume Incidents Messages and send an event to SocketIoServer client
   *
   * @param incidentsData
   */
  @org.springframework.kafka.annotation.KafkaListener(
      topics = "${topic.incidents}",
      containerFactory = "kafkaScoreboardsListenerContainerFactory")
  public void consumeIncidents(ConsumerRecord<String, String> incidentsData) {
    log.info("consumeIncidents key {} value {}", incidentsData.key(), incidentsData.value());
    try {
      Map<String, Object> incidentResponse =
          new ObjectMapper()
              .readValue(incidentsData.value(), new TypeReference<Map<String, Object>>() {});
      ((Map<String, Object>) incidentResponse.get("incident")).put("eventId", incidentsData.key());
      socketIOServer
          .getRoomOperations(incidentsData.key())
          .sendEvent(FACT_MSG + incidentsData.key(), incidentResponse);
      incidentsDataProcessor.incidentsDataIntoCache(incidentsData, incidentResponse);

    } catch (JsonProcessingException e) {
      log.error("Can not parse incidents incidetsData update {}", e.getMessage());
    }
  }
}
