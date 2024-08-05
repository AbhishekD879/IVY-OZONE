package com.egalacoral.spark.timeform.service.horseracing;

import com.egalacoral.spark.timeform.model.horseracing.HRPerformance;
import com.egalacoral.spark.timeform.model.horseracing.key.HRPerformanceKey;
import com.egalacoral.spark.timeform.rql.QueryStream;
import com.egalacoral.spark.timeform.storage.Storage;
import java.util.*;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/** Created by llegkyy on 31.08.16. */
@Service
public class HorseRacingPerformanceService {

  private static final Logger LOGGER = LoggerFactory.getLogger(HorseRacingPerformanceService.class);
  public static final String HR_PERFORMANCE_CACHE_NAME = "hr_performance";

  private Storage storage;

  @Autowired
  public HorseRacingPerformanceService(Storage storage) {
    this.storage = storage;
  }

  public void updatePerformances(Map<HRPerformanceKey, HRPerformance> performancesMap, Date date) {
    Map<HRPerformanceKey, HRPerformance> map = storage.getMap(HR_PERFORMANCE_CACHE_NAME);
    Map<HRPerformanceKey, HRPerformance> result =
        performancesMap.entrySet().stream()
            .map(
                entry -> {
                  if (map.containsKey(entry.getKey())) {
                    entry.getValue().setUpdateDate(date);
                  }
                  return entry;
                })
            .collect(Collectors.toMap(e -> e.getKey(), e -> e.getValue()));
    LOGGER.info("Save new horse racing performances {}", result.size());
    map.putAll(result);
  }

  // @Cacheable("hrPerformances::all")
  public List<HRPerformance> getHRPerformances() {
    Map<HRPerformanceKey, HRPerformance> map = storage.getMap(HR_PERFORMANCE_CACHE_NAME);
    return map.values().stream().collect(Collectors.toList());
  }

  // @Cacheable("hrPerformances::filter")
  public List<HRPerformance> getHRPerformances(
      Integer top, Integer skip, String orderby, String filter) {
    return QueryStream.of(getHRPerformances(), filter, orderby, top, skip).toList();
  }

  // @Cacheable("hrPerformance::byId")
  public Optional<HRPerformance> getPerfomance(String performanceId) {
    return getHRPerformances().stream()
        .filter(p -> p.getPerfomanceId().equals(performanceId))
        .findAny();
  }

  public boolean isHRPerformancesForDateExist(Date date) {
    return !getHRPerformancesByUpdatedDate(date).isEmpty();
  }

  public void clearPerformances() {
    LOGGER.info("Cleared performances");
    getPerfomanceMap().clear();
  }

  private Collection<HRPerformanceKey> getHRPerformancesByUpdatedDate(Date date) {
    Map<HRPerformanceKey, HRPerformance> map = storage.getMap(HR_PERFORMANCE_CACHE_NAME);
    return map.entrySet().stream()
        .filter(e -> e.getValue().getUpdateDate() != null)
        .filter(e -> e.getValue().getUpdateDate().compareTo(date) == 0)
        .map(e -> e.getKey())
        .collect(Collectors.toList());
  }

  private Map<Object, Object> getPerfomanceMap() {
    return storage.getMap(HR_PERFORMANCE_CACHE_NAME);
  }
}
