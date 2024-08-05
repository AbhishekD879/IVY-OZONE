package com.ladbrokescoral.oxygen.notification.services.stream;

import static com.ladbrokescoral.oxygen.notification.entities.MessageType.STREAM_STARTING;

import com.google.gson.Gson;
import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import com.ladbrokescoral.oxygen.notification.client.optin.IGameMediaApi;
import com.ladbrokescoral.oxygen.notification.client.optin.model.IGMEvent;
import com.ladbrokescoral.oxygen.notification.entities.dto.SubscriptionDTO;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.SportsBookUpdate;
import com.ladbrokescoral.oxygen.notification.services.NotificationsMessageHandler;
import com.ladbrokescoral.oxygen.notification.services.SiteServerApiService;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import com.ladbrokescoral.oxygen.notification.utils.ObjectMapper;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class StreamStartedService {

  private Gson gson;
  private Subscriptions subscriptions;
  private IGameMediaApi iGameMediaApi;
  private NotificationsMessageHandler messageHandler;
  private SiteServerApiService siteServerApiService;
  private MasterSlaveExecutor masterSlaveExecutor;

  public StreamStartedService(
      Subscriptions subscriptions,
      IGameMediaApi iGameMediaApi,
      NotificationsMessageHandler messageHandler,
      Gson gson,
      SiteServerApiService siteServerApiService,
      MasterSlaveExecutor masterSlaveExecutor) {
    this.subscriptions = subscriptions;
    this.iGameMediaApi = iGameMediaApi;
    this.messageHandler = messageHandler;
    this.gson = gson;
    this.siteServerApiService = siteServerApiService;
    this.masterSlaveExecutor = masterSlaveExecutor;
  }

  /**
   * Runs every 10 seconds. Checks if there are any subscribers for "stream_starting" notification.
   * If there are no subs - do nothing Gets events that are currently streaming, and searches if
   * there is any match between subs and events. Sends "stream_starting" to handler.
   */
  @Scheduled(cron = "${application.available-streams.check.cron.expression}", zone = "${time.zone}")
  public void checkAvailableStreams() {
    masterSlaveExecutor.executeIfMaster(
        this::checkStreamsInternal,
        () -> logger.info("[RACING FLOW][STREAM STARTING] Will not run cron job for slave."));
  }

  private void checkStreamsInternal() {
    logger.info("[RACING FLOW][STREAM STARTING] Running cron job to check available streams.");
    // get all subscribers for "stream_starting" event
    List<SubscriptionDTO> streamStartingSubscriptions =
        subscriptions.findAllByType(STREAM_STARTING.getType());

    if (streamStartingSubscriptions.size() == 0) {
      logger.info(
          "[RACING FLOW][STREAM STARTING] Cancelling cron job to check available streams since no one is subscribed.");
      // no subscribers for "stream_starting" event - nothing to do here
      return;
    }

    List<IGMEvent> igmEvents = iGameMediaApi.getOpenedStreamEvents();

    if (igmEvents.size() == 0) {
      logger.info(
          "[RACING FLOW][STREAM STARTING] Cancelling cron job to check available streams since no events are streaming.");
      // no opened IGM streams - nothing to do here
      return;
    }

    streamStartingSubscriptions.stream()
        .filter(dto -> Objects.nonNull(dto.getIGameMediaId()))
        .filter(
            dto ->
                igmEvents.stream()
                    .anyMatch(event -> dto.getIGameMediaId().equals(event.getEventID())))
        .collect(Collectors.toList())
        .forEach(this::onStreamAvailable);
  }

  /** Sends "stream_starting" update to handler. */
  private void onStreamAvailable(SubscriptionDTO subscription) {
    logger.info(
        "[RACING FLOW][STREAM STARTING] Found available stream for subscriber: {}", subscription);
    SportsBookUpdate update = ObjectMapper.toUpdateEntity(getEvent(subscription.getEventId()));
    update.getEvent().setStreamStarted(true);
    String jsonUpdate = gson.toJson(update);
    messageHandler.handleSportsBookUpdate(jsonUpdate);
  }

  private Event getEvent(long eventId) {
    return ObjectMapper.toEvent(
        siteServerApiService.getCachedEvent(String.valueOf(eventId)).orElse(null));
  }
}
