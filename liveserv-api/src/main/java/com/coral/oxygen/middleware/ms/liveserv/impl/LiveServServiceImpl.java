package com.coral.oxygen.middleware.ms.liveserv.impl;

import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.client.Call;
import com.coral.oxygen.middleware.ms.liveserv.client.CallExecutor;
import com.coral.oxygen.middleware.ms.liveserv.client.LiveServerListener;
import com.coral.oxygen.middleware.ms.liveserv.client.model.Message;
import com.coral.oxygen.middleware.ms.liveserv.exceptions.ServiceException;
import com.coral.oxygen.middleware.ms.liveserv.model.CacheSubscriptionStatsMapImpl;
import com.coral.oxygen.middleware.ms.liveserv.model.MapSubscriptionStatsMapImpl;
import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStatsMap;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.ErrorMessage;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Expired;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.SubscriptionAck;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.SubscriptionError;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Unsubscribed;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ScheduledExecutorService;
import java.util.function.Consumer;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class LiveServServiceImpl implements ManagedLiveServeService {

  private static final Consumer<SubscriptionStats> DEFAULT_UNSUBSCRIBE_CONSUMER =
      s -> log.debug("Subscription removed {}", s);
  private static final int MESSAGE_KEY_END_INDEX = 17;
  private static final int MESSAGE_HASH_END_INDEX = 27;
  private static final int MESSAGE_HASH_START_INDEX = 17;
  private static final int LIVE_SERVE_CHANNEL_LENGTH = 16;
  private final SubscriptionStatsMap subscriptions;
  private final EventIdResolver eventIdResolver;
  private final MessageHandler messageHandler;
  private final CallExecutor callExecutor;

  public LiveServServiceImpl(
      Call call, MessageHandler messageHandler, EventIdResolver eventIdResolver) {
    this.eventIdResolver = eventIdResolver;
    this.messageHandler = messageHandler;
    this.subscriptions = new MapSubscriptionStatsMapImpl(new ConcurrentHashMap<>());
    this.callExecutor = newCallExecutor(call, messageHandler);
  }

  public LiveServServiceImpl(
      Call call,
      MessageHandler messageHandler,
      EventIdResolver eventIdResolver,
      long maxItemsCount,
      Duration ttl,
      ScheduledExecutorService scheduledExecutor) {
    this.subscriptions =
        new CacheSubscriptionStatsMapImpl(
            maxItemsCount, ttl, this::notifyExpired, scheduledExecutor);
    this.eventIdResolver = eventIdResolver;
    this.messageHandler = messageHandler;
    this.callExecutor = newCallExecutor(call, messageHandler);
  }

  private CallExecutor newCallExecutor(Call call, MessageHandler messageHandler) {
    return new CallExecutor(
        call,
        () -> new ArrayList<>(subscriptions.values()),
        new LiveServerListener() {
          @Override
          public void onMessages(List<Message> messages) {
            messages.stream()
                .map(LiveServServiceImpl.this::toMessageEnvelope)
                .filter(Objects::nonNull)
                .forEach(messageHandler::handle);
          }

          @Override
          public void onError(Collection<SubscriptionStats> subscriptions, Throwable e) {
            subscriptions.stream()
                .map(
                    subscription ->
                        new ErrorMessage(
                            subscription.getChannel(),
                            subscription.getEventId(),
                            e.getMessage(),
                            e))
                .forEach(messageHandler::handle);
          }
        });
  }

  private MessageEnvelope toMessageEnvelope(Message message) {
    String channel = message.getMessageCode().substring(1, MESSAGE_KEY_END_INDEX);
    SubscriptionStats stats = subscriptions.get(channel);
    if (stats != null) {
      String hash =
          message.getMessageCode().substring(MESSAGE_HASH_START_INDEX, MESSAGE_HASH_END_INDEX);
      stats.setWaterMark(hash);
      stats.setLasSuccessUpdate(System.currentTimeMillis());
      stats.setUpdatesCount(stats.getUpdatesCount() + 1);
      return new MessageEnvelope(channel, stats.getEventId(), message);
    }
    return null;
  }

  @Override
  public void startConsuming() {
    callExecutor.execute();
  }

  @Override
  public void stopConsuming() throws InterruptedException {
    subscriptions.clear();
    callExecutor.shutdown();
  }

  @Override
  public void subscribe(String channel) {
    subscribe(channel, null, DEFAULT_UNSUBSCRIBE_CONSUMER);
  }

  @Override
  public void subscribe(String channel, Long eventId) {
    subscribe(channel, eventId, DEFAULT_UNSUBSCRIBE_CONSUMER);
  }

  @Override
  public void subscribe(String channel, Long eventId, Consumer<SubscriptionStats> onUnsubscribe) {
    validateChannel(channel);
    SubscriptionStats stats = subscriptions.get(channel);
    if (stats != null) {
      addSubscription(channel, stats);
      messageHandler.handle(new SubscriptionAck(channel, stats.getEventId()));
    } else {
      addNewSubscription(channel, eventId, onUnsubscribe);
    }
  }

  @Override
  public void addSubscription(String channel, SubscriptionStats subscription) {
    subscriptions.put(channel, subscription);
    log.debug(channel + " subscription refreshed");
  }

  @Override
  public void unsubscribe(String channel) {
    Objects.requireNonNull(channel, "channel");
    SubscriptionStats stats = subscriptions.remove(channel);
    if (stats != null && !stats.getUnsubscribeNotified().getAndSet(true)) {
      stats.getOnUnsubscribe().accept(stats);
      messageHandler.handle(new Unsubscribed(channel, stats.getEventId()));
    } else {
      messageHandler.handle(new ErrorMessage(channel, null, "Subscription not found"));
    }
  }

  private void notifyExpired(String channel, SubscriptionStats stats) {
    if (!stats.getExpireNotified().getAndSet(true)) {
      stats.getOnUnsubscribe().accept(stats);
      messageHandler.handle(new Expired(channel, stats.getEventId()));
    }
  }

  @Override
  public int subscriptionsSize() {
    return subscriptions.size();
  }

  @Override
  public Map<String, SubscriptionStats> getSubscriptions() {
    return subscriptions.asMap();
  }

  void addNewSubscription(String channel, Long eventId, Consumer<SubscriptionStats> onUnsubscribe) {
    SubscriptionStats stats;
    try {
      if (Objects.isNull(eventId)) {
        eventId = eventIdResolver.resolveEventId(channel);
      }
      stats = new SubscriptionStats(channel, eventId, onUnsubscribe);
      subscriptions.put(channel, stats);
      messageHandler.handle(new SubscriptionAck(channel, eventId));
      callExecutor.notifyAboutNewSubscription();
      log.debug(channel + " subscription added");
    } catch (ServiceException e) {
      log.error(channel + " subscription failed.", e);
      messageHandler.handle(new SubscriptionError(channel, e));
    } catch (Exception e) {
      log.error(channel + " subscription failed.", e);
      messageHandler.handle(
          new SubscriptionError(
              channel, new ServiceException("Unexpected error during subscription", e)));
    }
  }

  private void validateChannel(String channel) {
    Objects.requireNonNull(channel, "channel");
    if (channel.length() != LIVE_SERVE_CHANNEL_LENGTH) {
      throw new IllegalArgumentException(
          channel + " channel length must be " + LIVE_SERVE_CHANNEL_LENGTH);
    }
  }
}
