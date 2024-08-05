package com.ladbrokescoral.oxygen.trendingbets.context;

import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingPosition;
import java.util.*;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ConcurrentHashMap;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.util.CollectionUtils;

@Slf4j
public class PopularAccaContext {

  private PopularAccaContext() {}

  private static final int INITIAL_CAPACITY = 100;
  @Getter private static Map<String, TrendingPosition> selectionAccas = new ConcurrentHashMap<>();
  @Getter private static Map<String, Set<TrendingPosition>> eventAccas = new ConcurrentHashMap<>();
  @Getter private static Map<String, Set<TrendingPosition>> leagueAccas = new ConcurrentHashMap<>();

  @Getter
  private static BlockingQueue<String> uploadPendingQueue =
      new ArrayBlockingQueue<>(INITIAL_CAPACITY);

  @Getter
  private static Map<String, Set<TrendingPosition>> uploadPendingItems =
      new ConcurrentHashMap<>(INITIAL_CAPACITY);

  public static void updateSelectionAcca(TrendingPosition trendingPosition) {
    selectionAccas.put(trendingPosition.getEvent().getSelectionId(), trendingPosition);
  }

  public static void updateEventAcca(TrendingPosition trendingPosition) {
    Optional.ofNullable(eventAccas.get(trendingPosition.getEvent().getId()))
        .ifPresentOrElse(
            (Set<TrendingPosition> trendingPositions) -> {
              trendingPositions.remove(trendingPosition);
              trendingPositions.add(trendingPosition);
            },
            () ->
                eventAccas.put(trendingPosition.getEvent().getId(), addPostions(trendingPosition)));
  }

  public static void updateLeagueAcca(TrendingPosition trendingPostion) {
    Optional.ofNullable(leagueAccas.get(trendingPostion.getEvent().getTypeId()))
        .ifPresentOrElse(
            (Set<TrendingPosition> trendingPositions) -> {
              trendingPositions.remove(trendingPostion);
              trendingPositions.add(trendingPostion);
            },
            () ->
                leagueAccas.put(
                    trendingPostion.getEvent().getTypeId(), addPostions(trendingPostion)));
  }

  public static void purgeSelectionAcca(String selectionId) {
    selectionAccas.remove(selectionId);
  }

  public static void purgeAcca(
      Map<String, Set<TrendingPosition>> accas, String id, TrendingPosition exTrendingPosition) {
    Optional.ofNullable(accas.get(id))
        .ifPresent(
            (Set<TrendingPosition> positions) -> {
              positions.remove(exTrendingPosition);
              if (CollectionUtils.isEmpty(positions)) {
                accas.remove(id);
              }
            });
  }

  public static void purgeAccas(TrendingEvent trendingevent) {
    TrendingPosition postion = new TrendingPosition();
    postion.setEvent(trendingevent);
    purgeAcca(eventAccas, trendingevent.getId(), postion);
    purgeAcca(leagueAccas, trendingevent.getTypeId(), postion);
  }

  private static Set<TrendingPosition> addPostions(TrendingPosition selectionAdded) {
    Set<TrendingPosition> trendingPostions = new HashSet<>();
    trendingPostions.add(selectionAdded);
    return trendingPostions;
  }

  public static void addItemsToQueue(String key, Set<TrendingPosition> postions) {

    uploadPendingItems.put(key, postions);
    try {
      uploadPendingQueue.put(key);
    } catch (InterruptedException e) {
      Thread.currentThread().interrupt();
      log.error("Interrupted while uploading to queue :: {}", e.getMessage());
    }
  }

  public static Set<TrendingPosition> getItemToExecute() throws InterruptedException {
    return uploadPendingItems.remove(uploadPendingQueue.take());
  }
}
