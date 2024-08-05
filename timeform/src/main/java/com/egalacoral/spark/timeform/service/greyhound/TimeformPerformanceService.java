package com.egalacoral.spark.timeform.service.greyhound;

import com.egalacoral.spark.timeform.model.greyhound.Performance;
import com.egalacoral.spark.timeform.rql.QueryStream;
import com.egalacoral.spark.timeform.storage.Storage;
import java.util.*;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/** Created by Igor.Domshchikov on 8/23/2016. */
@Service
public class TimeformPerformanceService {

  private static final Logger LOGGER = LoggerFactory.getLogger(TimeformPerformanceService.class);
  public static final String PERFORMANCE_CACHE_NAME = "performance";

  private Storage storage;

  @Autowired
  public TimeformPerformanceService(Storage storage) {
    this.storage = storage;
  }

  public void updatePerformances(Map<Integer, Performance> newPerformancesMap, Date date) {
    Map<Integer, Performance> map = storage.getMap(PERFORMANCE_CACHE_NAME);
    Map<Integer, Performance> newPerformances =
        newPerformancesMap.entrySet().stream()
            .map(
                entry -> {
                  if (map.containsKey(entry.getKey())) {
                    entry.getValue().setUpdateDate(date);
                  }
                  return entry;
                })
            .collect(Collectors.toMap(entry -> entry.getKey(), entry -> entry.getValue()));
    LOGGER.info("Save new greyhound performances {}", newPerformances.size());
    map.putAll(newPerformances);
  }

  public List<Performance> getPerformances() {
    Map<Integer, Performance> map = storage.getMap(PERFORMANCE_CACHE_NAME);
    return new ArrayList<>(map.values());
  }

  // @Cacheable("performances::filter")
  public List<Performance> getPerformances(
      String filter, String orderby, Integer top, Integer skip) {
    return QueryStream.of(getPerformances(), filter, orderby, top, skip).toList();
  }

  public boolean isPerformancesForDateExist(Date date) {
    return !getPerformancesByUpdatedDate(date).isEmpty();
  }

  // @Cacheable("performance::byId")
  public Optional<Performance> getPerformance(Integer performanceId) {
    return getPerformances().stream()
        .filter(p -> p.getPerformanceId() != null && p.getPerformanceId().equals(performanceId))
        .findAny();
  }

  // @Cacheable("performance::byRaceId")
  public List<Performance> getPerformanceByRaceId(Integer raceId) {
    return getPerformances().stream()
        .filter(p -> p.getRaceId() != null && p.getRaceId().equals(raceId))
        .collect(Collectors.toList());
  }

  // @Cacheable("performance::byMeetingId")
  public List<Performance> getPerformanceByMeetingId(Integer paMeetingId) {
    return getPerformances().stream()
        .filter(p -> p.getPaMeetingId() != null && p.getPaMeetingId().equals(paMeetingId))
        .collect(Collectors.toList());
  }

  // @Cacheable("performance::byGreyhoundId")
  public List<Performance> getPerformanceByGreyhoundId(Integer greyhoundId) {
    return getPerformances().stream()
        .filter(p -> p.getGreyhoundId() != null && p.getGreyhoundId().equals(greyhoundId))
        .collect(Collectors.toList());
  }

  private Collection<Integer> getPerformancesByUpdatedDate(Date date) {
    Map<Integer, Performance> map = storage.getMap(PERFORMANCE_CACHE_NAME);
    return map.entrySet().stream()
        .filter(
            e ->
                e.getValue().getUpdateDate() == null
                    && e.getValue().getUpdateDate().compareTo(date) == 0)
        .map(e -> e.getKey())
        .collect(Collectors.toList());
  }
}
