package com.ladbrokescoral.oxygen.notification.controllers;

import static org.springframework.http.HttpStatus.INTERNAL_SERVER_ERROR;
import static org.springframework.http.MediaType.APPLICATION_JSON_VALUE;
import static org.springframework.http.ResponseEntity.accepted;
import static org.springframework.http.ResponseEntity.status;

import com.ladbrokescoral.oxygen.notification.entities.Item;
import com.ladbrokescoral.oxygen.notification.entities.ItemEmpty;
import com.ladbrokescoral.oxygen.notification.entities.ItemEmptys;
import com.ladbrokescoral.oxygen.notification.entities.Items;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.services.NotificationSubscriptionService;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import com.newrelic.api.agent.NewRelic;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
public class NativeNotifications {

  @Autowired private NotificationSubscriptionService service;

  @Qualifier("StringRedisTemplate")
  @Autowired
  private StringRedisTemplate redisTemplate;

  @Autowired private Events events;

  @Autowired private Subscriptions subscriptions;

  /**
   * Receives requests for football and racing notifications Empty list of type will tell the system
   * to unsubscribe this user from all types by platform and token.
   *
   * @param request contains token, platform, eventId and list of types (of notifications). Types
   *     could be: Racing: - going_down - race_off - results - non_runner - stream_starting
   *     <p>Football: - cards - goals - kick_off - periods
   * @return the request that was sent to this call with filled fields: 'listOfChannelId' and
   *     sportUri
   */
  @PutMapping(
      path = "/subscribe",
      produces = APPLICATION_JSON_VALUE,
      consumes = APPLICATION_JSON_VALUE)
  public ResponseEntity<?> createSubscription(@RequestBody @Validated final Item request) {
    logger.info("Request: " + request.toString());
    try {
      Item response = service.save(request);
      logger.info("Response: " + response.toString());
      return accepted().body(response);
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
      NewRelic.noticeError(ex);
      return status(INTERNAL_SERVER_ERROR).body(request);
    }
  }

  /**
   * A call to view existing types of subscriptions for given subscriber.
   *
   * @param request has to have token, platform, eventId.
   * @return the same request with filled 'types' list
   */
  @PostMapping(
      path = "/subscribe",
      produces = APPLICATION_JSON_VALUE,
      consumes = APPLICATION_JSON_VALUE)
  public ResponseEntity<?> vewSubscription(@RequestBody @Validated final ItemEmpty request) {
    logger.info("Request: " + request.toString());
    final Item response = service.get(request);
    logger.info("Response: " + response.toString());
    return accepted().body(response);
  }

  @PostMapping(
      path = "/eventsubscribe",
      produces = APPLICATION_JSON_VALUE,
      consumes = APPLICATION_JSON_VALUE)
  public ResponseEntity<List<Items>> viewEventSubscription(
      @RequestBody @Validated final ItemEmptys request) {
    logger.info(" viewEventSubscription Request: {} ", request.toString());
    final List<Items> response = service.get(request);
    logger.info(" viewEventSubscription Response: {} ", response.toString());
    return accepted().body(response);
  }

  @InitBinder
  public void populateRequest(WebDataBinder binder) {
    binder.setDisallowedFields(binder.getDisallowedFields());
  }

  /**
   * This API was disabled as part of Penetration testing BMA-61131 An utility call to obtain
   * subscribes in debugging and monitoring purposes.
   *
   * @return list of subscribers currently stored in Redis.
   */

  /*
  @GetMapping(path = "/getSubscribers", produces = APPLICATION_JSON_VALUE)
  public ResponseEntity<List<SubscriptionDTO>> getSubscribers() {
    List<SubscriptionDTO> subscriptions = (List<SubscriptionDTO>) this.subscriptions.findAll();
    return accepted().body(subscriptions);
  }*/

  /**
   * An utility call to obtain cached events in debugging and monitoring purposes.
   *
   * @return a litt of events, that are stored in Redis cache.
   */
  @GetMapping(path = "/cachedEvents", produces = "application/json")
  public ResponseEntity<List<Event>> getCachedEvents() {
    List<Event> events = (List<Event>) this.events.findAll();
    return accepted().body(events);
  }

  /**
   * A call to clear cache, in case of corrupted cached events, which could possibly cause errors.
   * It is save to use, since it will not affect any functionality, except for removing corrupted
   * data. Does not clear subscriptions, so users will still receive their notifications.
   */
  @DeleteMapping(path = "/clearEventsCache")
  public void clearEventsCache() {
    events.deleteAll();
    logger.warn("Cleared events cache");
  }

  /**
   * DO NOT USE THIS ON PROD. WILL CANCEL ALL CURRENT USER SUBSCRIPTIONS FOR NOTIFICATIONS. Only for
   * emergency, in case of corrupted subscribers data. This method will clear everything from
   * storage and restart the microservice.
   */
  @DeleteMapping(
      path = "/runtime/exit",
      produces = APPLICATION_JSON_VALUE,
      consumes = APPLICATION_JSON_VALUE)
  public void vewSubscription() {
    redisTemplate.getConnectionFactory().getConnection().flushAll();
    logger.warn("Redis have been flushed");
    redisTemplate.convertAndSend("system", "");
  }

  @GetMapping(path = "/noExpirySubscriptions/{page}/{size}", produces = "application/json")
  public ResponseEntity<Long> getNonExpiredSub(@PathVariable int page, @PathVariable int size) {
    Long expiredSub = this.service.getNoTTLRecords(page, size);
    return accepted().body(expiredSub);
  }
}
