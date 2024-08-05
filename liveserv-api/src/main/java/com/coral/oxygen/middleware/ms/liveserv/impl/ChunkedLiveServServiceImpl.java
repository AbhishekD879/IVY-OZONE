package com.coral.oxygen.middleware.ms.liveserv.impl;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import com.newrelic.api.agent.NewRelic;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.function.Consumer;
import java.util.function.Supplier;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class ChunkedLiveServServiceImpl implements LiveServService {

  // if there is 2 chunks, we don't want to delete second one immediately
  private static final double COMPACT_FILL_FACTOR = 0.35;
  public static final int SUBSCRIPTIONS_MAP_SIZE = 10000;
  private final long chunkMaxSize;
  private final Supplier<ManagedLiveServeService> newLiveServServiceSupplier;

  private final List<ManagedLiveServeService> chunks;
  private final Map<String, ManagedLiveServeService> chunkSubscriptions;

  public ChunkedLiveServServiceImpl(
      Supplier<ManagedLiveServeService> newLiveServServiceSupplier, long chunkMaxSize) {
    this.newLiveServServiceSupplier = newLiveServServiceSupplier;
    this.chunkMaxSize = chunkMaxSize;
    this.chunks = new CopyOnWriteArrayList<>();
    this.chunks.add(newLiveServServiceSupplier.get());
    chunkSubscriptions = new ConcurrentHashMap<>(SUBSCRIPTIONS_MAP_SIZE);
  }

  @Override
  public void startConsuming() {
    chunks.forEach(LiveServService::startConsuming);
  }

  @Override
  public void stopConsuming() {
    for (LiveServService chunk : chunks) {
      stopLiveServService(chunk);
    }
  }

  @Override
  public void subscribe(String channel) {
    doSubscribe(
        getAvailableLiveServService(channel), channel, null, s -> removeSubscription(channel));
  }

  @Override
  public void subscribe(String channel, Long eventId) {
    doSubscribe(
        getAvailableLiveServService(channel), channel, eventId, s -> removeSubscription(channel));
  }

  @Override
  public void subscribe(String channel, Long eventId, Consumer<SubscriptionStats> onUnsubscribe) {
    doSubscribe(
        getAvailableLiveServService(channel),
        channel,
        eventId,
        onUnsubscribe.andThen(s -> removeSubscription(s.getChannel())));
  }

  void doSubscribe(
      ManagedLiveServeService liveServService,
      String channel,
      Long eventId,
      Consumer<SubscriptionStats> unsubscribeConsumer) {
    liveServService.subscribe(channel, eventId, unsubscribeConsumer);
    chunkSubscriptions.put(channel, liveServService);
  }

  @Override
  public void unsubscribe(String channel) {
    Optional.ofNullable(chunkSubscriptions.get(channel)).ifPresent(ls -> ls.unsubscribe(channel));
    removeSubscription(channel);
  }

  private void removeSubscription(String channel) {
    chunkSubscriptions.remove(channel);
    compactChunks();
  }

  private void compactChunks() {
    logLiveServerStatistics();
    // in case we can compact more than 1 chunk in a row
    while (canBeCompacted()) {
      int lastChunk = chunks.size() - 1;
      ManagedLiveServeService lastLiveServ = chunks.remove(lastChunk);
      lastLiveServ.getSubscriptions().forEach(this::moveToAvailableChunk);
      stopLiveServService(lastLiveServ);
      log.debug("Compressed LS chunk");
    }
  }

  private void stopLiveServService(LiveServService lastLiveServ) {
    try {
      lastLiveServ.stopConsuming();
    } catch (InterruptedException e) {
      log.error("Failed to stop LiveServService", e);
      Thread.currentThread().interrupt();
    }
  }

  private void moveToAvailableChunk(String channel, SubscriptionStats subscriptionStats) {
    chunkSubscriptions.remove(channel);
    ManagedLiveServeService availableLiveServService = getAvailableLiveServService(channel);
    chunkSubscriptions.put(channel, availableLiveServService);
    availableLiveServService.addSubscription(channel, subscriptionStats);
  }

  private boolean canBeCompacted() {
    return chunks.size() > 1
        && chunkSubscriptions.size() < COMPACT_FILL_FACTOR * chunkMaxSize * chunks.size();
  }

  private ManagedLiveServeService getAvailableLiveServService(String channel) {
    ManagedLiveServeService liveServService = chunkSubscriptions.get(channel);
    if (Objects.isNull(liveServService)) {
      liveServService =
          chunks.stream()
              .filter(c -> c.subscriptionsSize() < chunkMaxSize)
              .findAny()
              .orElseGet(this::addNewChunk);
    }
    return liveServService;
  }

  private ManagedLiveServeService addNewChunk() {
    ManagedLiveServeService newChunk = newLiveServServiceSupplier.get();
    newChunk.startConsuming();
    chunks.add(newChunk);
    log.debug("Added next chunk to serve updates");
    logLiveServerStatistics();
    return newChunk;
  }

  private void logLiveServerStatistics() {
    String chunksStats =
        chunks.stream()
            .map(ManagedLiveServeService::subscriptionsSize)
            .map(String::valueOf)
            .collect(Collectors.joining("|"));
    log.info("Chunks sizes: {}", chunksStats);
    NewRelic.getAgent()
        .getInsights()
        .recordCustomEvent(
            "LiveServeChunks",
            Collections.<String, Object>singletonMap("chunks-stats", chunksStats));
  }
}
