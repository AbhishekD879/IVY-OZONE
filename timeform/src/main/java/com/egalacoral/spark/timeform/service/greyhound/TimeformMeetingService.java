package com.egalacoral.spark.timeform.service.greyhound;

import com.egalacoral.spark.timeform.model.OBRelatedEntity;
import com.egalacoral.spark.timeform.model.greyhound.Entry;
import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import com.egalacoral.spark.timeform.model.greyhound.Race;
import com.egalacoral.spark.timeform.model.greyhound.TimeformMeeting;
import com.egalacoral.spark.timeform.rql.QueryStream;
import com.egalacoral.spark.timeform.storage.Storage;
import com.egalacoral.spark.timeform.tools.Tools;
import java.io.Serializable;
import java.text.DateFormat;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TimeformMeetingService implements Serializable, MeetingService {

  private static final Logger LOGGER = LoggerFactory.getLogger(TimeformMeetingService.class);
  public static final String MEETING_CACHE_NAME = "meeting";
  private static final long serialVersionUID = 6365403238645421349L;
  private transient Storage storage;
  public static final DateFormat DATE_FORMAT =
      com.egalacoral.spark.timeform.api.tools.Tools.simpleDateFormat("yyyy-MM-dd");

  @Autowired
  public TimeformMeetingService(Storage storage) {
    this.storage = storage;
  }

  public TimeformMeeting save(Meeting meeting) {
    LOGGER.info("Save meeting to cache Name:{}, Id:{} ", meeting.getName(), meeting.getMeetingId());
    Map<Object, Meeting> map = storage.getMap(MEETING_CACHE_NAME);
    map.put(meeting.getMeetingId(), meeting);
    return meeting;
  }

  public void save(List<Meeting> meetings) {
    Map<Object, Meeting> map = storage.getMap(MEETING_CACHE_NAME);
    meetings.stream()
        .forEach(
            item -> {
              LOGGER.info(
                  "Save meeting to cache Name:{}, Id:{} ", item.getName(), item.getMeetingId());
              map.put(item.getMeetingId(), item);
            });
  }

  public void updateMeetingOpenBetMapping(Map<Integer, Meeting> meetingMap) {
    Map<Integer, Meeting> map = storage.getMap(MEETING_CACHE_NAME);
    Map<Integer, Meeting> result =
        map.entrySet().stream()
            .filter(e -> meetingMap.containsKey(e.getKey()))
            .map(
                e -> {
                  e.getValue().setName(meetingMap.get(e.getKey()).getName());
                  e.getValue().getOpenBetIds().addAll(meetingMap.get(e.getKey()).getOpenBetIds());
                  return e;
                })
            .collect(Collectors.toMap(e -> e.getKey(), e -> e.getValue()));
    map.putAll(result);
  }

  public void updateRacesWithEntriesOpenBetMapping(Map<Integer, Meeting> meetingMap) {
    Map<Integer, Meeting> map = storage.getMap(MEETING_CACHE_NAME);
    Map<Integer, Meeting> result =
        map.entrySet().stream()
            .filter(mapEntry -> meetingMap.containsKey(mapEntry.getKey()))
            .map(
                entry -> {
                  entry
                      .getValue()
                      .getRaces()
                      .forEach(
                          race -> {
                            LOGGER.info(
                                "Update meeting {} race {} with entries",
                                entry.getValue().getName(),
                                race.getRaceId());
                            Optional<Race> optionalRace =
                                meetingMap.get(entry.getKey()).getRaces().stream()
                                    .filter(r -> r.getRaceId().equals(race.getRaceId()))
                                    .findFirst();
                            Race updatedRace = optionalRace.get();
                            if (optionalRace.isPresent()) {
                              if (race.getEntries() != null) {
                                race.getEntries()
                                    .forEach(
                                        e -> {
                                          Optional<Entry> newEntry =
                                              optionalRace.get().getEntries().stream()
                                                  .filter(
                                                      entry1 ->
                                                          entry1
                                                              .getEntryId()
                                                              .equals(e.getEntryId()))
                                                  .findFirst();
                                          newEntry.ifPresent(
                                              nEntry ->
                                                  e.getOpenBetIds().addAll(nEntry.getOpenBetIds()));
                                        });
                              }
                              race.setOpenBetIds(updatedRace.getOpenBetIds());
                            }
                          });
                  return entry;
                })
            .collect(Collectors.toMap(e -> e.getKey(), e -> e.getValue()));
    map.putAll(result);
  }

  public void updateRacesWithEntries(Map<Integer, Set<Race>> filteredRaces) {
    Map<Integer, Meeting> map = storage.getMap(MEETING_CACHE_NAME);
    Map<Integer, Meeting> result =
        map.entrySet().stream()
            .filter(mapEntry -> filteredRaces.containsKey(mapEntry.getKey()))
            .map(
                entry -> {
                  LOGGER.info(
                      "Update meeting: {} {} races with entries",
                      entry.getKey(),
                      entry.getValue().getName());
                  if (entry.getValue().getRaces() == null
                      || entry.getValue().getRaces().isEmpty()) {
                    entry.getValue().setRaces(filteredRaces.get(entry.getKey()));
                  } else {
                    filteredRaces
                        .get(entry.getKey())
                        .forEach(
                            race ->
                                race.getEntries()
                                    .addAll(
                                        entry.getValue().getRaces().stream()
                                            .filter(
                                                originRace ->
                                                    originRace.getRaceId().equals(race.getRaceId()))
                                            .findFirst()
                                            .get()
                                            .getEntries()));
                    filteredRaces.get(entry.getKey()).addAll(entry.getValue().getRaces());
                    entry.getValue().getRaces().clear();
                    entry.getValue().getRaces().addAll(filteredRaces.get(entry.getKey()));
                  }
                  return entry;
                })
            .collect(Collectors.toMap(e -> e.getKey(), e -> e.getValue()));
    map.putAll(result);
  }

  // @Cacheable("meetings::all")
  public List<Meeting> getMeetings() {
    long time = System.currentTimeMillis();
    LOGGER.info("HFREEZING_getMeetings - get Map values");
    Collection<Object> values = storage.getMap(MEETING_CACHE_NAME).values();
    LOGGER.info(
        "HFREEZING_getMeetings - time to get Map values - {}", System.currentTimeMillis() - time);
    LOGGER.info("Get meetings from cache size - " + values.size());
    LOGGER.info(
        "HFREEZING_getMeetings - first call values - {}", System.currentTimeMillis() - time);
    List<Meeting> meetings =
        values.parallelStream().map(v -> (Meeting) v).collect(Collectors.toList());
    LOGGER.info("HFREEZING_getMeetings - return meetings - {}", System.currentTimeMillis() - time);
    return meetings;
  }

  // @Cacheable("meetings::byId")
  public Meeting getMeeting(Integer meetingId) {
    long time = System.currentTimeMillis();
    LOGGER.info("HFREEZING_getMeetings - get meeting by id");
    Meeting value = (Meeting) storage.getMap(MEETING_CACHE_NAME).get(meetingId);
    LOGGER.info(
        "HFREEZING_getMeetings - return meeting by id - {}", System.currentTimeMillis() - time);
    return value;
  }

  // @Cacheable("meetings::byDate")
  public Collection<Meeting> getMeetingsByDate(Date date) {
    Map<Object, Meeting> map = storage.getMap(MEETING_CACHE_NAME);
    String strDate = DATE_FORMAT.format(date);
    return map.entrySet().stream()
        .filter(entry -> entry.getValue().getMeetingDate().contains(strDate))
        .map(e -> e.getValue())
        .collect(Collectors.toList());
  }

  // @Cacheable("meetingsMap::byDate")
  public Map<Integer, Meeting> getMeetingsMapForDate(Date date) {
    LOGGER.info("Get all stored meetings map for date");
    String strDate = DATE_FORMAT.format(date);
    Map<Integer, Meeting> map = storage.getMap(MEETING_CACHE_NAME);
    return map.entrySet().stream()
        .filter(e -> e.getValue().getMeetingDate().contains(strDate))
        .collect(Collectors.toMap(e -> e.getKey(), e -> e.getValue()));
  }

  // @Cacheable("meetings::filter")
  public List<Meeting> getMeetings(String filter, String orderby, Integer top, Integer skip) {
    return QueryStream.of(getMeetings(), filter, orderby, top, skip).toList();
  }

  // @Cacheable("meetings::byOpenBetId")
  public List<Meeting> getMeetingByOpenbetId(List<Integer> openbetId) {
    return getMeetings().stream()
        .filter(m -> containsOpenbetId(openbetId, m))
        .collect(Collectors.toList());
  }

  public boolean isRacesWithEntriesExistForUpdateDate(Date date) {
    return !getRacesWithEntriesByUpdatedDate(date).isEmpty();
  }

  private Collection<Race> getRacesWithEntriesByUpdatedDate(Date date) {
    Map<Integer, Meeting> meetingMap = getMeetingsMapForDate(date);
    return meetingMap.values().stream()
        .filter(meeting -> meeting.getRaces() != null)
        .map(meeting -> meeting.getRaces())
        .flatMap(list -> list.stream())
        .collect(Collectors.toList())
        .stream()
        .filter(race -> race.getUpdateDate() != null && race.getUpdateDate().compareTo(date) == 0)
        .collect(Collectors.toList());
  }

  protected Stream<Entry> getEntriesStream(Race v) {
    Set<Entry> entries = v.getEntries();
    return entries != null ? entries.stream() : Tools.emptyStream();
  }

  public boolean containsOpenbetId(List<Integer> openbetId, OBRelatedEntity e) {
    return openbetId != null
        && openbetId.stream()
                .filter(id -> e.getOpenBetIds() != null && e.getOpenBetIds().contains(id))
                .count()
            > 0;
  }
}
