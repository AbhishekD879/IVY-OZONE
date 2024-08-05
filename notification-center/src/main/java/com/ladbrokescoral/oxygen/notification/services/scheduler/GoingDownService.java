package com.ladbrokescoral.oxygen.notification.services.scheduler;

import static com.ladbrokescoral.oxygen.notification.entities.MessageType.GOING_DOWN;

import com.google.gson.Gson;
import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import com.ladbrokescoral.oxygen.notification.entities.dto.SubscriptionDTO;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.SportsBookUpdate;
import com.ladbrokescoral.oxygen.notification.services.NotificationsMessageHandler;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import com.ladbrokescoral.oxygen.notification.utils.ObjectMapper;
import com.ladbrokescoral.oxygen.notification.utils.time.TimeProvider;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.joda.time.DateTime;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.util.ObjectUtils;

@Slf4j
@Component
public class GoingDownService {

  /**
   * Going down event is triggered two minutes (specified in properties) before event is started.
   */
  private final long goingDownRelativeDelayMilliseconds;

  private NotificationsMessageHandler messageHandler;
  private Subscriptions subscriptions;
  private Gson gson;
  private MasterSlaveExecutor masterSlaveExecutor;
  private final TimeProvider timeProvider;

  @Autowired
  public GoingDownService(
      Gson gson,
      TimeProvider timeProvider,
      Subscriptions subscriptions,
      NotificationsMessageHandler messageHandler,
      MasterSlaveExecutor masterSlaveExecutor,
      @Value("${event.going-down.pre-delay.seconds}") int goingDownPreDelaySeconds) {
    this.gson = gson;
    this.subscriptions = subscriptions;
    this.timeProvider = timeProvider;
    this.messageHandler = messageHandler;
    goingDownRelativeDelayMilliseconds = 1000 * goingDownPreDelaySeconds;

    this.masterSlaveExecutor = masterSlaveExecutor;
  }

  private boolean isGoingDownTime(SubscriptionDTO subscription) {
    boolean goingDownTime = false;
    String startTime = subscription.getStartTime();
    if (!ObjectUtils.isEmpty(startTime)) {
      goingDownTime = isGoingDownTime(startTime);
    }
    return goingDownTime;
  }

  private boolean isGoingDownTime(String startTime) {
    DateTime eventStartTime = DateTime.parse(startTime);
    DateTime currentTime = timeProvider.currentTime();

    return currentTime.isBefore(eventStartTime.minus(goingDownRelativeDelayMilliseconds / 2))
        && currentTime.isAfter(eventStartTime.minus(goingDownRelativeDelayMilliseconds));
  }

  @Scheduled(cron = "${application.going-down.check.cron.expression}", zone = "${time.zone}")
  protected void checkGoingDown() {
    masterSlaveExecutor.executeIfMaster(
        () ->
            subscriptions.findAllByType(GOING_DOWN.getType()).stream()
                .filter(this::isGoingDownTime)
                .map(SubscriptionDTO::getEventId)
                .distinct()
                .collect(Collectors.toList())
                .forEach(this::sendGoingDownEvent),
        () -> logger.info("[RACING FLOW][GOING DOWN]: Will not run cron for 'going down'"));
  }

  private void sendGoingDownEvent(long eventId) {
    logger.info("[RACING FLOW][GOING DOWN][{}]: Sending going down for event", eventId);

    SportsBookUpdate update = ObjectMapper.toUpdateEntity(Event.builder().eventId(eventId).build());
    update.getEvent().setGoingDown(true);
    String jsonUpdate = gson.toJson(update);
    messageHandler.handleSportsBookUpdate(jsonUpdate);
  }
}
