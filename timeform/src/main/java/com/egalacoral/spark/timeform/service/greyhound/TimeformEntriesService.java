package com.egalacoral.spark.timeform.service.greyhound;

import com.egalacoral.spark.timeform.model.greyhound.Entry;
import com.egalacoral.spark.timeform.rql.QueryStream;
import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;
import java.io.Serializable;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TimeformEntriesService implements Serializable {

  private static final Logger LOGGER = LoggerFactory.getLogger(TimeformEntriesService.class);

  private TimeformMeetingService timeformMeetingService;
  private TimeformRacesService timeformRacesService;

  Cache<Integer, List<Entry>> cache =
      Caffeine.newBuilder().expireAfterWrite(30, TimeUnit.SECONDS).maximumSize(1).build();

  @Autowired
  public TimeformEntriesService(
      TimeformMeetingService timeformMeetingService, TimeformRacesService timeformRacesService) {
    this.timeformMeetingService = timeformMeetingService;
    this.timeformRacesService = timeformRacesService;
  }

  public List<Entry> getEntries(String filter, String orderby, Integer top, Integer skip) {
    return QueryStream.of(getEntries(), filter, orderby, top, skip).toList();
  }

  public Optional<Entry> getEntry(Integer entryId) {
    return getEntries().stream().filter(e -> e.getEntryId().equals(entryId)).findAny();
  }

  public List<Entry> getEntryByOpenbetId(List<Integer> openbetId) {
    return getEntries().stream()
        .filter(e -> timeformMeetingService.containsOpenbetId(openbetId, e))
        .collect(Collectors.toList());
  }

  private List<Entry> getEntries() {
    Integer key = 1;
    return cache.get(key, s -> this.load());
  }

  private List<Entry> load() {
    return timeformRacesService.getRaces().stream()
        .flatMap(v -> timeformMeetingService.getEntriesStream(v))
        .collect(Collectors.toList());
  }
}
