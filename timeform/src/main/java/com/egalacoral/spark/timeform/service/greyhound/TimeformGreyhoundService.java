package com.egalacoral.spark.timeform.service.greyhound;

import com.egalacoral.spark.timeform.model.greyhound.Greyhound;
import com.egalacoral.spark.timeform.rql.QueryStream;
import com.egalacoral.spark.timeform.storage.Storage;
import java.util.*;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TimeformGreyhoundService {

  private static final Logger LOGGER = LoggerFactory.getLogger(TimeformGreyhoundService.class);
  public static final String GREYHOUND_CACHE_NAME = "greyhound";

  private Storage storage;

  @Autowired
  public TimeformGreyhoundService(Storage storage) {
    this.storage = storage;
  }

  public void updateGreyhounds(Map<Integer, Greyhound> greyhoundMap, Date date) {
    Map<Integer, Greyhound> map = storage.getMap(GREYHOUND_CACHE_NAME);
    if (map.size() > 0) {
      Map<Integer, Greyhound> newPerformances =
          greyhoundMap.entrySet().stream()
              .map(
                  entry -> {
                    if (map.containsKey(entry.getKey())) {
                      entry.getValue().setUpdateDate(date);
                      Greyhound greyhound = map.get(entry.getKey());
                      if (entry.getValue().getForm() == null) {
                        entry.getValue().setForm(greyhound.getForm());
                      }
                    }
                    return entry;
                  })
              .collect(Collectors.toMap(entry -> entry.getKey(), entry -> entry.getValue()));
      LOGGER.info("Save new greyhounds {}", newPerformances.size());
      map.putAll(newPerformances);
    } else {
      LOGGER.info("Save {} greyhounds to the hazelcast", greyhoundMap.size());
      map.putAll(greyhoundMap);
    }
  }

  // @Cacheable("greyhoungs::all")
  public List<Greyhound> getGreyhoundsCached() {
    return getGreyhounds();
  }

  public List<Greyhound> getGreyhounds() {
    Map<Integer, Greyhound> map = storage.getMap(GREYHOUND_CACHE_NAME);
    return map.values().stream().collect(Collectors.toList());
  }

  public Map<Integer, Greyhound> getGreyhoundMap() {
    return storage.getMap(GREYHOUND_CACHE_NAME);
  }

  // @Cacheable("greyhoungs::filter")
  public List<Greyhound> getGreyhounds(String filter, String orderby, Integer top, Integer skip) {
    return QueryStream.of(getGreyhounds(), filter, orderby, top, skip).toList();
  }

  // @Cacheable("greyhoung::byId")
  public Optional<Greyhound> getGreyhound(Integer greyhoundId) {
    return getGreyhounds().stream().filter(g -> g.getGreyhoundId().equals(greyhoundId)).findAny();
  }

  public boolean isGreyhoundsForDateExist(Date date) {
    return !getGreyhoundsByUpdatedDate(date).isEmpty();
  }

  private Collection<Integer> getGreyhoundsByUpdatedDate(Date date) {
    Map<Integer, Greyhound> map = storage.getMap(GREYHOUND_CACHE_NAME);
    return map.entrySet().stream()
        .filter(e -> e.getValue().getUpdateDate().compareTo(date) == 0)
        .map(e -> e.getKey())
        .collect(Collectors.toList());
  }
}
