package com.egalacoral.spark.timeform.service.greyhound;

import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import com.egalacoral.spark.timeform.model.greyhound.Race;
import com.egalacoral.spark.timeform.rql.QueryStream;
import com.egalacoral.spark.timeform.tools.Tools;
import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;
import java.io.Serializable;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TimeformRacesService implements Serializable {

  private TimeformMeetingService timeformMeetingService;

  Cache<Integer, List<Race>> cache =
      Caffeine.newBuilder().expireAfterWrite(30, TimeUnit.SECONDS).maximumSize(1).build();

  @Autowired
  public TimeformRacesService(TimeformMeetingService timeformMeetingService) {
    this.timeformMeetingService = timeformMeetingService;
  }

  public List<Race> getRaces(String filter, String orderby, Integer top, Integer skip) {
    return QueryStream.of(getRaces(), filter, orderby, top, skip).toList();
  }

  public Optional<Race> getRace(Integer raceId) {
    return getRaces().stream().filter(r -> r.getRaceId().equals(raceId)).findAny();
  }

  public List<Race> getRaceByOpenbetId(List<Integer> openbetId) {
    return getRaces().stream()
        .filter(r -> timeformMeetingService.containsOpenbetId(openbetId, r))
        .collect(Collectors.toList());
  }

  public List<Race> getRaces() {
    Integer key = 2;
    return cache.get(key, s -> this.load());
  }

  private List<Race> load() {
    return timeformMeetingService.getMeetings().stream()
        .flatMap(v -> getRacesStream(v))
        .collect(Collectors.toList());
  }

  protected Stream<Race> getRacesStream(Meeting v) {
    Set<Race> races = v.getRaces();
    return races != null ? races.stream() : Tools.emptyStream();
  }
}
