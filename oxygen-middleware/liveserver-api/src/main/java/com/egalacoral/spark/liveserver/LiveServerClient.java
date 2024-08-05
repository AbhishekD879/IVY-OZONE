package com.egalacoral.spark.liveserver;

import com.egalacoral.spark.liveserver.meta.EventMetaInfoRepository;
import com.egalacoral.spark.liveserver.service.LiveServerMessageHandler;
import java.util.Map;
import java.util.concurrent.atomic.AtomicBoolean;
import lombok.extern.slf4j.Slf4j;

/**
 * Main class for Live Server client API
 *
 * @author Vitalij Havryk
 */
@Slf4j
public class LiveServerClient {

  private final CallExecutor callExecutor;
  private final Payload payload;
  private final AtomicBoolean isRunning = new AtomicBoolean(false);

  private String id;

  public LiveServerClient(
      String endPoint,
      Call call,
      Long subscriptionExpire,
      LiveServerListener listener,
      EventMetaInfoRepository eventMetaInfoRepository,
      String id) {
    super();
    if (listener instanceof LiveServerMessageHandler) {
      ((LiveServerMessageHandler) listener).setEventMetaInfoRepository(eventMetaInfoRepository);
    }
    checkParameters(endPoint, listener, subscriptionExpire);
    payload = new Payload(subscriptionExpire);
    this.callExecutor = new CallExecutor(endPoint, call, payload, listener, id);
    this.id = id;
  }

  private void checkParameters(
      String endPoint, LiveServerListener listener, Long expireSubscription) {
    if (endPoint == null) {
      throw new IllegalArgumentException("Endpoint is null. Please provide endpoint");
    }
    if (listener == null) {
      throw new IllegalArgumentException("Listener is null. Please provide listener");
    }
    if (expireSubscription == null) {
      throw new IllegalArgumentException(
          "Expire subscription is null. Please provide expireSubscription");
    }
  }

  public String getId() {
    return this.id;
  }

  public void connect() {
    if (!isRunning.getAndSet(true)) {
      callExecutor.execute();
    }
  }

  public void disconnect() {
    unsubscibeAll();
    callExecutor.shutdown();
    isRunning.set(false);
  }

  public CallExecutor getCallExecutor() {
    return callExecutor;
  }

  public Payload getPayload() {
    return payload;
  }

  public Map<String, SubscriptionSubject> getPayloadItems() {
    return getPayload().getPayloadItems();
  }

  public void subscribeOnClock(String eventId) {
    subscribeOnItem(SubscriptionSubjectFactory.onClockSubscription(eventId));
  }

  public void subscribeOnEvent(String eventId) {
    subscribeOnItem(SubscriptionSubjectFactory.onEventSubscription(eventId));
  }

  public void subscribeOnMarket(String marketId) {
    subscribeOnItem(SubscriptionSubjectFactory.onMarketSubscription(marketId));
  }

  public void subscribeOnScore(String eventId) {
    subscribeOnItem(SubscriptionSubjectFactory.onScoreSubscription(eventId));
  }

  public void subscribeOnSelection(String selectionId) {
    subscribeOnItem(SubscriptionSubjectFactory.onSelectionSubscription(selectionId));
  }

  public void subscribeOnItem(SubscriptionSubject subscriptionSubject) {
    this.payload.addItem(subscriptionSubject);
    log.debug("LiveServerClient <{}> subscribed on {}", this.id, subscriptionSubject.getKeyValue());
  }

  public void unsubscibeAll() {
    this.payload.clear();
  }

  public boolean isRunning() {
    return isRunning.get();
  }
}
