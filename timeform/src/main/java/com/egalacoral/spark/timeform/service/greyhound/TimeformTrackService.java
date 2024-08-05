package com.egalacoral.spark.timeform.service.greyhound;

import com.egalacoral.spark.timeform.model.greyhound.Track;
import com.egalacoral.spark.timeform.rql.QueryStream;
import com.egalacoral.spark.timeform.storage.Storage;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/** Created by Igor.Domshchikov on 8/26/2016. */
@Service
public class TimeformTrackService {

  private static final Logger LOGGER = LoggerFactory.getLogger(TimeformTrackService.class);
  public static final String TRACK_CACHE_NAME = "track";

  private Storage storage;

  @Autowired
  public TimeformTrackService(Storage storage) {
    this.storage = storage;
  }

  // @Cacheable("trackIds::all")
  public Collection<Integer> getTracksIds() {
    Map<Integer, Track> map = storage.getMap(TRACK_CACHE_NAME);
    return map.keySet();
  }

  public void save(Map<Integer, Track> tracksMap) {
    LOGGER.info("Storing tracks to the hazelcast");
    storage.getMap(TRACK_CACHE_NAME).putAll(tracksMap);
  }

  // @Cacheable("tracks::all")
  public List<Track> getTracks() {
    Map<Integer, Track> map = storage.getMap(TRACK_CACHE_NAME);
    return map.values().stream().collect(Collectors.toList());
  }
  // @Cacheable("track::byId")
  public Optional<Track> getTrack(Integer trackId) {
    return getTracks().stream().filter(t -> t.getTrackId().equals(trackId)).findAny();
  }
  // @Cacheable("tracks::filter")
  public List<Track> getTracks(String filter, String orderby, Integer top, Integer skip) {
    return QueryStream.of(getTracks(), filter, orderby, top, skip).toList();
  }
}
