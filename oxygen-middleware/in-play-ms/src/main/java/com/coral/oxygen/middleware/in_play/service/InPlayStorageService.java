package com.coral.oxygen.middleware.in_play.service;

import static com.coral.oxygen.middleware.common.configuration.DistributedKey.*;
import static com.coral.oxygen.middleware.common.service.GenerationKeyType.INPLAY_GENERATION;

import com.coral.oxygen.middleware.common.configuration.DistributedKey;
import com.coral.oxygen.middleware.common.imdg.DistributedAtomicLong;
import com.coral.oxygen.middleware.common.imdg.DistributedInstance;
import com.coral.oxygen.middleware.common.service.ErrorsStorageService;
import com.coral.oxygen.middleware.common.service.GenerationStorageService;
import com.coral.oxygen.middleware.in_play.service.model.InPlayCache;
import com.coral.oxygen.middleware.in_play.service.model.InPlayCacheBuilder;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportsRibbon;
import com.google.gson.Gson;
import com.newrelic.api.agent.NewRelic;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/** Created by azayats on 11.01.17. */
@Slf4j
@Component
public class InPlayStorageService {

  public static final String INPLAY_ERROR_KEY = "inplay_error";
  private static final long ATOMIC_DELTA = 1;
  private static final String DELIMITER = "::";

  private final DistributedInstance distributedInstance;
  private final GenerationStorageService generationStorage;
  private final ErrorsStorageService errorsStorage;

  private final Gson gson;

  @Autowired
  public InPlayStorageService(
      DistributedInstance distributedInstance,
      GenerationStorageService generationStorage,
      ErrorsStorageService errorsStorage,
      Gson gson) {
    this.distributedInstance = distributedInstance;
    this.generationStorage = generationStorage;
    this.errorsStorage = errorsStorage;
    this.gson = gson;
  }

  public void saveError(Throwable e) {
    Map<String, Object> error = buildError(e);
    error.put("time", System.currentTimeMillis());
    errorsStorage.saveError(INPLAY_ERROR_KEY, gson.toJson(error));
  }

  public void clearError() {
    errorsStorage.removeError(INPLAY_ERROR_KEY);
  }

  private Map<String, Object> buildError(Throwable e) {
    Map<String, Object> result = new HashMap<>();
    result.put("class", e.getClass().getName());
    result.put("message", e.getMessage());
    ByteArrayOutputStream baos = new ByteArrayOutputStream();
    PrintWriter pw = new PrintWriter(baos);
    e.printStackTrace(pw);
    pw.flush();
    try {
      baos.flush();
      result.put("trace", baos.toString());
      pw.close();
      baos.close();
    } catch (IOException e1) {
      NewRelic.noticeError(e);
      log.warn("Unexpected exception on tools stream operation");
    }
    if (Objects.nonNull(e.getCause())) {
      result.put("cause", buildError(e.getCause()));
    }
    return result;
  }

  public long save(
      InPlayData structure, List<SportSegment> sportSegments, SportsRibbon sportsRibbon) {
    long generation = generateVersionId();
    String key = String.valueOf(generation);

    // New sport structure
    structure.setGeneration(generation);
    distributedInstance.updateExpirableValue(INPLAY_STRUCTURE_MAP, key, gson.toJson(structure));

    // New sport ribbon
    distributedInstance.updateExpirableValue(
        INPLAY_SPORTS_RIBBON_MAP, key, gson.toJson(sportsRibbon));

    /** Virtual sports Data */
    distributedInstance.updateExpirableValue(
        VIRTUAL_SPORTS_STRUCTURE_MAP, key, gson.toJson(structure.getVirtualSportEvents()));

    // New sport segment
    sportSegments.forEach(
        sportSegment -> {
          log.debug(
              "storage _ CACHE key# {} selector# {} ",
              SportSegment.getKey(sportSegment),
              sportSegment.getMarketSelector());
          distributedInstance.updateExpirableValue(
              INPLAY_SPORT_SEGMENT_MAP,
              createSportSegmentKey(generation, sportSegment),
              gson.toJson(sportSegment));
        });

    // New inplay cache
    InPlayCacheBuilder builder = new InPlayCacheBuilder();
    InPlayCache cache = builder.sportSegments(sportSegments).build();

    String newCache = gson.toJson(cache);
    log.debug("new cache =================== \n{}\n", newCache);
    distributedInstance.updateExpirableValue(INPLAY_CACHED_STRUCTURE_MAP, key, newCache);

    // Publish new version of the data
    log.info("InPlay model with {} ID was stored", key);
    generationStorage.putLatest(INPLAY_GENERATION, key);

    return generation;
  }

  public static String createSportSegmentKey(long generation, SportSegment sportSegment) {
    return createSportSegmentKey(String.valueOf(generation), SportSegment.getKey(sportSegment));
  }

  private static String createSportSegmentKey(String generation, String segmentKey) {
    return generation + DELIMITER + segmentKey;
  }

  public String getLatestInPlayData() {
    return distributedInstance.getValue(
        INPLAY_STRUCTURE_MAP, generationStorage.getLatest(INPLAY_GENERATION));
  }

  public InPlayData getLatestInPlayDataObject() {
    String latestJson = getLatestInPlayData();
    if (latestJson == null) {
      return null;
    }
    try {
      return gson.fromJson(latestJson, InPlayData.class);
    } catch (Exception e) {
      NewRelic.noticeError(e);
      log.error("Error parsing InPlayModel. Suppressed and returned null", e);
      return null;
    }
  }

  private Long generateVersionId() {
    DistributedAtomicLong atomicLong =
        distributedInstance.getAtomicLong(DistributedKey.ATOMIC_INPLAY_DATA);
    return atomicLong.addAndGet(ATOMIC_DELTA);
  }

  public String getLatestSportsRibbon() {
    String lastVersion = generationStorage.getLatest(INPLAY_GENERATION);
    return distributedInstance.getValue(INPLAY_SPORTS_RIBBON_MAP, lastVersion);
  }

  public String getLatestSportSegment(String key) {
    String lastGeneration = generationStorage.getLatest(INPLAY_GENERATION);
    return distributedInstance.getValue(
        INPLAY_SPORT_SEGMENT_MAP, createSportSegmentKey(lastGeneration, key));
  }

  public Collection<SportSegment> getLatestSportSegmentsObjects() {
    String lastGeneration = generationStorage.getLatest(INPLAY_GENERATION);
    List<String> searchKeys =
        InPlayData.allSportSegmentsStream(getLatestInPlayDataObject())
            .map(SportSegment::getAllMarketSelectorKeys)
            .flatMap(Collection::stream)
            .map(key -> lastGeneration + "::" + key)
            .collect(Collectors.toList());

    return distributedInstance.getValues(INPLAY_SPORT_SEGMENT_MAP, searchKeys).stream()
        .map(this::safeParseSportSegment)
        .filter(Objects::nonNull)
        .collect(Collectors.toList());
  }

  private SportSegment safeParseSportSegment(String json) {
    if (json == null) {
      return null;
    }
    try {
      return gson.fromJson(json, SportSegment.class);
    } catch (Exception e) {
      NewRelic.noticeError(e);
      log.error("Error parsing SportSegment. Suppressed and returned null", e);
      return null;
    }
  }

  public SportsRibbon getLatestSportsRibbonObject() {
    String json = getLatestSportsRibbon();
    if (json == null) {
      return null;
    }
    try {
      return gson.fromJson(json, SportsRibbon.class);
    } catch (Exception e) {
      NewRelic.noticeError(e);
      log.error("Error parsing SportsRibbon. Suppressed and returned null", e);
      return null;
    }
  }

  public InPlayCache getLatestInPlayCache() {
    try {
      String lastGeneration = generationStorage.getLatest(INPLAY_GENERATION);
      String strCache = distributedInstance.getValue(INPLAY_CACHED_STRUCTURE_MAP, lastGeneration);
      if (strCache == null) {
        return null;
      }
      return gson.fromJson(strCache, InPlayCache.class);
    } catch (Exception e) {
      NewRelic.noticeError(e);
      log.error("Error parsing InPlay. Suppressed and returned null", e);
      return null;
    }
  }
}
