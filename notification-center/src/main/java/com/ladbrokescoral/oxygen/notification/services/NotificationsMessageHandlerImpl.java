package com.ladbrokescoral.oxygen.notification.services;

import static com.ladbrokescoral.oxygen.notification.configs.AsyncConfig.EXECUTOR_QUALIFIER_KAFKA;

import com.coral.oxygen.middleware.ms.liveserv.model.messages.Envelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.EnvelopeType;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import com.ladbrokescoral.oxygen.notification.entities.MessageType;
import com.ladbrokescoral.oxygen.notification.services.handler.SportsbookUpdateTypeMapper;
import com.ladbrokescoral.oxygen.notification.services.handler.football.IncidentsMessageHandler;
import com.ladbrokescoral.oxygen.notification.services.handler.football.KickOffMessageHandler;
import com.ladbrokescoral.oxygen.notification.services.handler.football.PeriodsMessageHandler;
import com.ladbrokescoral.oxygen.notification.services.handler.horses.GoingDownMessageHandler;
import com.ladbrokescoral.oxygen.notification.services.handler.horses.NonRunnerMessageHandler;
import com.ladbrokescoral.oxygen.notification.services.handler.horses.RaceOffMessageHandler;
import com.ladbrokescoral.oxygen.notification.services.handler.horses.ResultsMessageHandler;
import com.ladbrokescoral.oxygen.notification.services.handler.horses.StreamStartingMessageHandler;
import com.newrelic.api.agent.NewRelic;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

/** A place to handle updates for Football and Racing */
@Slf4j
@Component
@RequiredArgsConstructor
public class NotificationsMessageHandlerImpl implements NotificationsMessageHandler {

  private final PeriodsMessageHandler periodsHandler;
  private final IncidentsMessageHandler incidentsHandler;
  private final KickOffMessageHandler kickOffHandler;
  private final GoingDownMessageHandler goingDownMessageHandler;
  private final RaceOffMessageHandler raceOffMessageHandler;
  private final ResultsMessageHandler resultsMessageHandler;
  private final NonRunnerMessageHandler nonRunnerMessageHandler;
  private final StreamStartingMessageHandler streamStartingMessageHandler;
  private final ScoresInNameMessageHandler scoresInNameHandler;
  private final ScoreBoardUpdateMessageHandler scoreBoardUpdateMessageHandler;
  private final MasterSlaveExecutor masterSlaveExecutor;
  private final SportsbookUpdateTypeMapper sportsbookUpdateTypeMapper;

  /**
   * Handles football updates from liveserv In case if the microservice runs on multiple nodes -
   * only master node will handle these type of updates, so that it avoids duplicate messages
   */
  @Override
  public void handle(Envelope envelope) {
    masterSlaveExecutor.executeIfMaster(
        () -> {
          if (envelope.getType() == EnvelopeType.MESSAGE) {
            handleLiveServeUpdateMessage((MessageEnvelope) envelope);
          }
        },
        () -> logger.info("[FOOTBALL FLOW] Update from liveserv. Handled only on master."));
  }

  public void handleLiveServeUpdateMessage(MessageEnvelope messageEnvelope) {
    final String msgBody = messageEnvelope.getMessage().getJsonData();
    final String type = extractTypeFromChannel(messageEnvelope);
    switch (MessageType.valueOf(type)) {
      case sEVENT:
        scoresInNameHandler.handle(messageEnvelope);
        break;
      case sSCBRD:
        // todo is it ok to handle scrbd if we already taken score from event's name?
        // does SS trigger scrbd update anyway?
        scoreBoardUpdateMessageHandler.handle(msgBody);
        break;
      case sCLOCK:
        periodsHandler.handle(msgBody);
        break;
      case sICENT:
        incidentsHandler.handle(msgBody);
        kickOffHandler.handle(msgBody);
        break;
    }
  }

  private String extractTypeFromChannel(Envelope envelope) {
    return envelope.getChannel().substring(0, 6);
  }

  /**
   * Uses MessageTypes.java#forMessage() to determine the type of update based on message.
   *
   * @param message from DF kafka, 'sportsbook' topic. Also could be received in the same format
   *     from GoingDownService.java, and StreamStartedService.java
   */
  @Override
  @Async(EXECUTOR_QUALIFIER_KAFKA)
  public void handleSportsBookUpdate(String message) {
    sportsbookUpdateTypeMapper
        .forMessage(message)
        .parallelStream()
        .forEach(
            type -> {
              logger.info("[RACING FLOW][{}]: Received message: {}", type.toUpperCase(), message);
              handleInternal(message, type);
            });
  }

  /**
   * Delegates an update to relevant handler based on its type
   *
   * @param message from DF kafka, 'sportsbook' topic. Also could be received in the same format
   *     from * GoingDownService.java, and StreamStartedService.java
   * @param type of the update.
   */
  private void handleInternal(String message, String type) {
    try {
      MessageType messageType = MessageType.valueOf(type);
      switch (messageType) {
        case GOING_DOWN:
          goingDownMessageHandler.handle(message);
          break;
        case RACE_OFF:
          raceOffMessageHandler.handle(message);
          break;
        case RESULTS:
          resultsMessageHandler.handle(message);
          break;
        case NON_RUNNER:
          nonRunnerMessageHandler.handle(message);
          break;
        case STREAM_STARTING:
          streamStartingMessageHandler.handle(message);
          break;
      }
    } catch (IllegalArgumentException illegalArgumentException) {
      logger.error("Unsupported message: <{}> {}", type, message);
      NewRelic.noticeError(illegalArgumentException);
    } catch (Exception exception) {
      logger.error("Error during processing message", exception);
      NewRelic.noticeError(exception);
    }
  }
}
