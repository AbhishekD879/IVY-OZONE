package com.ladbrokescoral.oxygen.trendingbets.context;

import com.ladbrokescoral.oxygen.trendingbets.dto.PopularBets;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingBetsDto;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import java.time.Duration;
import java.util.*;
import java.util.concurrent.*;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

@Getter
@Component
@Slf4j
public class TrendingBetsContext {

  // ttl is in seconds
  @Autowired
  private TrendingBetsContext(
      @Value("${trendingbets.max.items.count:5000}") Integer maxItemsCount,
      @Value("${trendingbets.ttl.inSeconds:172800}") Integer timeToExpire,
      @Value("${trendingbets.max.queue.capacity:500}") Integer queueSize) {
    initContext(queueSize, maxItemsCount, timeToExpire);
  }

  private static void onDeleteListener(String key, List<TrendingEvent> value) {
    uploadPendingItems.put(key, value);
    try {
      uploadPendingQueue.put(key);
    } catch (InterruptedException e) {
      Thread.currentThread().interrupt();
      log.error("Interrupted while uploading to queue :: {}", e.getMessage());
    }
  }

  private static void initContext(int queueSize, int maxItemsCount, int timeToExpire) {
    uploadPendingItems = new ConcurrentHashMap<>(queueSize);
    uploadPendingQueue = new ArrayBlockingQueue<>(queueSize);
    personalizedSelections =
        new PersonalizedBetsMap<>(
            maxItemsCount, Duration.ofSeconds(timeToExpire), TrendingBetsContext::onDeleteListener);
  }

  /** map maintains trendingBets position for the WebSocket channel* */
  @Getter private static Map<String, TrendingBetsDto> trendingBets = new ConcurrentHashMap<>();

  /**
   * map maintains the event/market/selection channels as keys with list of trending selection.
   * event and market channel may have multiple TrendingSelections; selection channel will have only
   * one TrendingSelection
   */
  @Getter
  private static TrendingEventMap<String, List<TrendingEvent>> popularSelections =
      new PopularBetsMap<>(new ConcurrentHashMap<>());
  /** map maintains set 0f Popular bet channels as values for each TrendingSelection* */
  @Getter
  private static Map<TrendingEvent, Set<String>> selectionMappings = new ConcurrentHashMap<>();
  /** set maintains subscribed channels* */
  private static ConcurrentMap<String, String> subscribedChannels = new ConcurrentHashMap<>();

  @Getter private static BlockingQueue<String> uploadPendingQueue;

  @Getter private static Map<String, List<TrendingEvent>> uploadPendingItems;

  private static final String DEFAULT = "default";

  @Getter private static TrendingEventMap<String, List<TrendingEvent>> personalizedSelections;

  public static ConcurrentMap<String, String> getSubscribedChannels() {
    return subscribedChannels;
  }

  public static String setSubscribedChannels(String channel) {
    return subscribedChannels.put(channel, DEFAULT);
  }

  public static List<TrendingEvent> clearEventContextForLiveEvents(List<TrendingEvent> events) {

    Arrays.stream(PopularBets.values())
        .forEach(
            betType -> events.forEach(trendingEvent -> cleanSelections(trendingEvent, betType)));

    return events;
  }

  public static void cleanSelections(TrendingEvent selection, PopularBets betType) {
    if (PopularBets.TRENDING_BETS.equals(betType)) {
      getSelectionMappings().remove(selection);
      CompletableFuture.runAsync(() -> purgePopularAcca(selection));
    }
    removeTrendingSelections(selection, betType);
  }

  private static void removeTrendingSelections(TrendingEvent selection, PopularBets betType) {
    TrendingEventMap<String, List<TrendingEvent>> selections = getSelectionByBetsType(betType);
    selection
        .getStreamChannels()
        .forEach(
            (String liveServChannel) -> {
              if (selections.getOrDefault(liveServChannel, new ArrayList<>()).remove(selection)
                  && CollectionUtils.isEmpty(selections.get(liveServChannel)))
                selections.remove(liveServChannel);
            });
  }

  private static void purgePopularAcca(TrendingEvent selection) {
    PopularAccaContext.purgeSelectionAcca(selection.getSelectionId());
    PopularAccaContext.purgeAccas(selection);
  }

  public static void updateOrSaveLivesChannels(TrendingEvent selection, PopularBets betType) {
    selection
        .getStreamChannels()
        .forEach(channel -> updateOrSaveLivesChannel(selection, channel, betType));
  }

  public static void updateOrSaveLivesChannel(
      TrendingEvent selection, String channel, PopularBets betType) {

    TrendingEventMap<String, List<TrendingEvent>> selections = getSelectionByBetsType(betType);
    selections.computeIfAbsent(channel, value -> new ArrayList<>());
    selections.get(channel).add(selection);
  }

  public static TrendingEventMap<String, List<TrendingEvent>> getSelectionByBetsType(
      PopularBets betType) {
    if (PopularBets.TRENDING_BETS.equals(betType)) return popularSelections;
    else return personalizedSelections;
  }

  public static List<TrendingEvent> getItemToPurge() throws InterruptedException {
    return uploadPendingItems.remove(uploadPendingQueue.take());
  }
}
