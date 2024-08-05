package com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve;

import com.coral.oxygen.middleware.ms.liveserv.newclient.LiveUpdatesChannel;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import java.util.Map;
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
  private volatile boolean isRunning;

  private String id;

  public LiveServerClient(
      String endPoint, Long subscriptionExpire, LiveServerListener listener, String id, Call call) {
    super();
    checkParameters(endPoint, listener, subscriptionExpire);
    payload = new Payload(subscriptionExpire);
    this.callExecutor = new CallExecutor(endPoint, payload, listener, id, call);
    this.id = id;
  }

  private void checkParameters(
      String endPoint, LiveServerListener listener, Long expireSubscription) {
    if (endPoint == null) {
      NewRelic.noticeError("Endpoint is null. Please provide endpoint");
      throw new IllegalArgumentException("Endpoint is null. Please provide endpoint");
    }
    if (listener == null) {
      NewRelic.noticeError("Listener is null. Please provide listener");
      throw new IllegalArgumentException("Listener is null. Please provide listener");
    }
    if (expireSubscription == null) {
      NewRelic.noticeError("Expire subscription is null. Please provide expireSubscription");
      throw new IllegalArgumentException(
          "Expire subscription is null. Please provide expireSubscription");
    }
  }

  public String getId() {
    return this.id;
  }

  @Trace(metricName = "LiveServerClient/Connect", dispatcher = true)
  public void connect() {
    synchronized (this) {
      if (!isRunning) {
        callExecutor.execute();
        this.isRunning = true;
      }
    }
  }

  @Trace(metricName = "LiveServerClient/Disconnect", dispatcher = true)
  public void disconnect() {
    synchronized (this) {
      unsubscibeAll();
      callExecutor.shutdown();
      isRunning = false;
    }
  }

  public CallExecutor getCallExecutor() {
    return callExecutor;
  }

  public String getEndPoint() {
    return callExecutor.getEndPoint();
  }

  public Payload getPayload() {
    return payload;
  }

  public Map<String, LiveUpdatesChannel> getPayloadItems() {
    return getPayload().getPayloadItems();
  }

  public void subscribeOnItem(LiveUpdatesChannel subscriptionSubject) {
    this.payload.addItem(subscriptionSubject);
    log.info("LiveServerClient {} subscribed on {}", this.id, subscriptionSubject.getKeyValue());
    log.debug("LiveServerClient <{}> subscribed on {}", this.id, subscriptionSubject.getKeyValue());
  }

  public void unsubscibeAll() {
    log.info("LiveServerClient {} unsubscribed on all", this.id);
    this.payload.clear();
  }

  public boolean isRunning() {
    return isRunning;
  }

  public void unsubscribe(LiveUpdatesChannel subject) {

    log.info("LiveServerClient {} unsubscribed on {}", this.id, subject.messageHashKey());
    this.payload.invalidate(subject.messageHashKey());
  }
}
