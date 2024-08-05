package com.ladbrokescoral.oxygen.notification.services.handler.football;

import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.notification.entities.IncidentMessage;
import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.services.EventService;
import com.ladbrokescoral.oxygen.notification.services.notifications.NotificationsFactory;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import com.newrelic.api.agent.NewRelic;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class IncidentsMessageHandler extends AbstractFootballNotificationMessageHandler {

  private static final String TYPE_FOR_CARDS = "cards";
  private static final String TYPE_FOR_GOALS = "goals";

  private static final String YELLOW_CARD = "YELLOW_CARD";
  private static final String RED_CARD = "RED_CARD";
  private static final String PENALTY_AWARDED = "PENALTY_AWARDED";
  private static final String PENALTY_MISSED = "PENALTY_MISSED";

  private static final String YELLOW_CARD_MESSAGE = "Yellow Card! ";
  private static final String RED_CARD_MESSAGE = "Red Card! ";
  private static final String PENALTY_MESSAGE = "Penalty! ";
  private static final String PENALTY_MISSED_MESSAGE = "Penalty Missed! ";

  @Autowired
  public IncidentsMessageHandler(
      Gson gson,
      Events events,
      Subscriptions subscriptions,
      EventService eventService,
      NotificationsFactory notificationsFactory) {
    super(gson, events, subscriptions, eventService, notificationsFactory);
  }

  @Override
  public Payload process(String json) {
    try {
      final IncidentMessage message = gson.fromJson(json, IncidentMessage.class);
      long eventId = message.getEventId();
      final Event event = getEventById(eventId);

      switch (message.getIncidentCode()) {
        case YELLOW_CARD:
          return getPayloadFor(
              YELLOW_CARD_MESSAGE, message.getParticipantName(), event, TYPE_FOR_CARDS);
        case RED_CARD:
          return getPayloadFor(
              RED_CARD_MESSAGE, message.getParticipantName(), event, TYPE_FOR_CARDS);
        case PENALTY_AWARDED:
          return getPayloadFor(
              PENALTY_MESSAGE, message.getParticipantName(), event, TYPE_FOR_GOALS);
        case PENALTY_MISSED:
          return getPayloadFor(
              PENALTY_MISSED_MESSAGE, message.getParticipantName(), event, TYPE_FOR_GOALS);
        default:
          break;
      }
      return Payload.builder().build();
    } catch (Exception e) {
      logger.error("Error during processing cards", e);
      NewRelic.noticeError(e);
      return Payload.builder().build();
    }
  }
}
