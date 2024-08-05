package com.ladbrokescoral.oxygen.notification.services.handler.football;

import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.notification.entities.ClockMessage;
import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.services.EventService;
import com.ladbrokescoral.oxygen.notification.services.notifications.NotificationsFactory;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class PeriodsMessageHandler extends AbstractFootballNotificationMessageHandler {

  private final String TYPE = "periods";
  private static final String SCORER = "";

  @Autowired
  public PeriodsMessageHandler(
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
      final ClockMessage message = gson.fromJson(json, ClockMessage.class);
      String nextPeriod = message.getPeriodCode();
      final Event event = getEventById(message.getEventId());

      String firstLineOfMessage = "";

      if (nextPeriod.equals(event.getPeriod())) {
        events.save(event.setPeriod(nextPeriod));
        return Payload.builder().build();
      } else {
        switch (message.getPeriodCode()) {
          case "FIRST_HALF":
            //            firstLineOfMessage = "First Half";
            break;
          case "FINISH":
            firstLineOfMessage = "Full Time Result!";
            break;
          case "HALF_TIME":
            firstLineOfMessage = "Half Time";
            break;
          case "SECOND_HALF":
            //            firstLineOfMessage = "Second Half";
            break;
          case "OVER":
            firstLineOfMessage = "Full Time";
            break;
          case "EXTRA_TIME_HALF_TIME":
            firstLineOfMessage = "Extra Time - Half Time";
            break;
          case "PENALTIES":
            firstLineOfMessage = "Extra Time - Full Time";
            break;
          default:
            break;
        }

        events.save(event.setPeriod(nextPeriod));

        if (firstLineOfMessage.isEmpty()) {
          logger.info("Unsupported type of period code: " + message.getPeriodCode());
          return Payload.builder().build();
        }

        return getPayloadFor(firstLineOfMessage, SCORER, event, TYPE);
      }
    } catch (Exception e) {
      logger.error("Error during processing updates for periods ", e);
      return Payload.builder().build();
    }
  }
}
