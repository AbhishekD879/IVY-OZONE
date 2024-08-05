package com.coral.oxygen.edp.tracking;

import com.newrelic.api.agent.NewRelic;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/** Created by azayats on 28.12.17. */
public abstract class AbstractTracker<T, D> implements Tracker<T, D> {

  private static final Logger LOGGER = LoggerFactory.getLogger(AbstractTracker.class);

  private final Object subscriptionsLock = new Object();

  // Key - eventId, Value - Map of clients subscribed to this event (where key is client id)
  private final Map<T, Map<String, Subscription<T, D>>> subscriptions = new ConcurrentHashMap<>();

  private final DataStorage<T, D> storage;

  private final DataConsumer<T, D> consumer;

  private final ChangeDetector<D> changeDetector;

  public AbstractTracker(
      DataStorage<T, D> storage, DataConsumer<T, D> consumer, ChangeDetector<D> changeDetector) {
    this.storage = storage;
    this.consumer = consumer;
    this.changeDetector = changeDetector;
    this.consumer.setListener(
        new ConsumingListener<T, D>() {
          @Override
          public void onResponse(Map<T, D> response) {
            processNewData(response);
          }

          @Override
          public void onError(String message, Throwable t) {
            LOGGER.error("Error during data consuming. " + message, t);
            NewRelic.noticeError(t);
          }
        });
  }

  @Override
  public void addSubscription(Subscription<T, D> client) {
    addSubscriptionInternal(client);
    D data = storage.get(client.getTicket());
    if (Objects.isNull(data)) {
      requestData(Collections.singleton(client.getTicket()));
    } else {
      client.emit(data);
    }
  }

  @Override
  public void removeSubscription(String clientId, T ticket) {
    removeSubscriptionInternal(clientId, ticket);
  }

  @Override
  public void refreshData() {
    synchronizedDataRefresh();
  }

  private void synchronizedDataRefresh() {
    synchronized (subscriptionsLock) {
      requestData(subscriptions.keySet());
    }
  }

  protected boolean addSubscriptionInternal(Subscription<T, D> client) {
    T ticket = client.getTicket();
    synchronized (subscriptionsLock) {
      Map<String, Subscription<T, D>> clients = subscriptions.get(ticket);
      if (clients == null) {
        clients = new HashMap<>();
      } else {
        clients = new HashMap<>(clients);
      }
      Subscription<T, D> oldClient = clients.put(client.getClientId(), client);
      subscriptions.put(ticket, clients);
      return oldClient == null;
    }
  }

  private boolean removeSubscriptionInternal(String clientId, T ticket) {
    synchronized (subscriptionsLock) {
      Map<String, Subscription<T, D>> consumers = subscriptions.get(ticket);
      if (consumers != null) {
        consumers = new HashMap<>(consumers);
        Subscription<T, D> oldClient = consumers.remove(clientId);
        if (consumers.isEmpty()) {
          subscriptions.remove(ticket);
        } else {
          subscriptions.put(ticket, consumers);
        }
        return oldClient != null;
      } else {
        return false;
      }
    }
  }

  protected void requestData(Set<T> ticketsToRequest) {
    consumer.consume(ticketsToRequest);
  }

  protected void processNewData(Map<T, D> newData) {
    newData.keySet().parallelStream()
        .forEach(
            ticket -> {
              D data = newData.get(ticket);
              D oldData = storage.replace(ticket, data);
              if (changeDetector.dataIsChanged(data, oldData)) {
                emitData(ticket, data);
              }
            });
  }

  protected void emitData(T ticket, D data) {
    Map<String, Subscription<T, D>> subscriptionMap = subscriptions.get(ticket);
    subscriptionMap.values().parallelStream().forEach(subscription -> subscription.emit(data));
  }
}
