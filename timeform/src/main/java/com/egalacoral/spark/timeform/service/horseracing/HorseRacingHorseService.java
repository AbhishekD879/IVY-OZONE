package com.egalacoral.spark.timeform.service.horseracing;

import com.egalacoral.spark.timeform.model.horseracing.HRHorse;
import com.egalacoral.spark.timeform.rql.QueryStream;
import com.egalacoral.spark.timeform.storage.Storage;
import java.util.*;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/** Created by llegkyy on 15.09.16. */
@Service
public class HorseRacingHorseService {
  private static final Logger LOGGER = LoggerFactory.getLogger(HorseRacingHorseService.class);
  public static final String HORSE_CACHE_NAME = "hr_horse";

  private Storage storage;

  @Autowired
  public HorseRacingHorseService(Storage storage) {
    this.storage = storage;
  }

  // @Cacheable("hrHorses::all")
  public List<HRHorse> getHorses() {
    Map<String, HRHorse> map = storage.getMap(HORSE_CACHE_NAME);
    return map.values().stream().collect(Collectors.toList());
  }

  // @Cacheable("hrHorses::filter")
  public List<HRHorse> getHorses(String filter, String orderBy, Integer top, Integer skip) {
    return QueryStream.of(getHorses(), filter, orderBy, top, skip).toList();
  }

  // @Cacheable("hrHorse::byHorseCode")
  public Optional<HRHorse> getHorse(String horseCode) {
    return getHorses().stream().filter(horse -> horse.getHorseCode().equals(horseCode)).findAny();
  }

  public void updateHorses(Map<String, HRHorse> retrivedMap, Date date) {
    Map<String, HRHorse> map = storage.getMap(HORSE_CACHE_NAME);
    Map<String, HRHorse> result =
        retrivedMap.entrySet().stream()
            .map(
                entry -> {
                  if (map.containsKey(entry.getKey())) {
                    entry.getValue().setUpdateDate(date);
                  }
                  return entry;
                })
            .collect(Collectors.toMap(e -> e.getKey(), e -> e.getValue()));
    LOGGER.info("Save {} horses to hazelcast", result.size());
    map.putAll(result);
  }

  public void clearHorses() {
    LOGGER.info("Cleared horses");
    storage.getMap(HORSE_CACHE_NAME).clear();
  }

  public Boolean isNewHorsesForDateExist(Date date) {
    return !getHorsesByUpdatedDate(date).isEmpty();
  }

  private Collection<String> getHorsesByUpdatedDate(Date date) {
    Map<String, HRHorse> horseMap = storage.getMap(HORSE_CACHE_NAME);
    return horseMap.entrySet().stream()
        .filter(
            e ->
                e.getValue().getUpdateDate() != null
                    && e.getValue().getUpdateDate().compareTo(date) == 0)
        .map(e -> e.getKey())
        .collect(Collectors.toList());
  }
}
