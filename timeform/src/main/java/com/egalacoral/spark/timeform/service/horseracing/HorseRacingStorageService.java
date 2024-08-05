package com.egalacoral.spark.timeform.service.horseracing;

import com.egalacoral.spark.timeform.api.tools.Tools;
import com.egalacoral.spark.timeform.model.OBRelatedEntity;
import com.egalacoral.spark.timeform.model.greyhound.TimeformMeeting;
import com.egalacoral.spark.timeform.model.horseracing.HREntry;
import com.egalacoral.spark.timeform.model.horseracing.HRMeeting;
import com.egalacoral.spark.timeform.model.horseracing.HRRace;
import com.egalacoral.spark.timeform.rql.QueryStream;
import com.egalacoral.spark.timeform.service.greyhound.MeetingService;
import com.egalacoral.spark.timeform.storage.Storage;
import com.egalacoral.spark.timeform.timer.TimerService;
import etm.core.monitor.EtmPoint;
import java.text.DateFormat;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class HorseRacingStorageService implements MeetingService {

  private static final transient Logger LOGGER =
      LoggerFactory.getLogger(HorseRacingStorageService.class);

  public static final String HR_MEETING_CACHE_NAME = "hr_meeting";

  private final Storage storage;

  @Autowired private TimerService timerService = new TimerService();

  @Autowired
  public HorseRacingStorageService(Storage storage) {
    this.storage = storage;
  }

  public void save(List<HRMeeting> meetings) {
    Map<HRMeeting.HRMeetingKey, HRMeeting> map = getMap();
    meetings.stream()
        .forEach(
            item -> {
              LOGGER.info("Save meeting to cache Key:{}", item.getKey());
              map.put(item.getKey(), item);
            });
  }

  public void update(Map<HRMeeting.HRMeetingKey, HRMeeting> meetings) {
    Map<HRMeeting.HRMeetingKey, HRMeeting> map = getMap();
    if (map.size() > 0) {
      Map<HRMeeting.HRMeetingKey, HRMeeting> result =
          map.entrySet().stream()
              .filter(mapEntry -> meetings.containsKey(mapEntry.getKey()))
              .map(
                  entry -> {
                    LOGGER.info("Update horse race meeting: " + entry.getKey());
                    entry
                        .getValue()
                        .getOpenBetIds()
                        .addAll(meetings.get(entry.getKey()).getOpenBetIds());
                    return entry;
                  })
              .collect(Collectors.toMap(e -> e.getKey(), e -> e.getValue()));
      map.putAll(result);
    }
  }

  public Map<HRMeeting.HRMeetingKey, HRMeeting> getMeetingsMapForDate(Date date) {
    LOGGER.debug("Get all stored HR meetings map for date {}", date);
    DateFormat df = Tools.simpleDateFormat("yyyy-MM-dd");
    String strDate = df.format(date);
    return getMap().entrySet().stream()
        .filter(e -> e.getValue().getMeetingDate().contains(strDate))
        .collect(Collectors.toMap(e -> e.getKey(), e -> e.getValue()));
  }

  public void clear() {
    LOGGER.info("Clearing meetings");
    getMap().clear();
  }

  public boolean isRacesWithEntriesExistForDate(Date date) {
    return !getRacesWithEntriesForDate(date).isEmpty();
  }

  private List<HRRace> getRacesWithEntriesForDate(Date date) {
    Map<HRMeeting.HRMeetingKey, HRMeeting> meetings = getMeetingsMapForDate(date);
    return meetings.values().stream()
        .filter(meeting -> meeting.getRaces() != null)
        .map(meeting -> meeting.getRaces())
        .flatMap(races -> races.stream())
        .collect(Collectors.toList())
        .stream()
        .filter(
            hrRace -> hrRace.getUpdateDate() != null && hrRace.getUpdateDate().compareTo(date) == 0)
        .collect(Collectors.toList());
  }

  private Map<HRMeeting.HRMeetingKey, HRMeeting> getMap() {
    return storage.getMap(HR_MEETING_CACHE_NAME);
  }

  public List<HRMeeting> getMeetings() {
    EtmPoint point = timerService.createPoint(this, "getMeetingsFromHazelcast");
    List<HRMeeting> meetings = getMap().values().stream().collect(Collectors.toList());
    timerService.submit(point);
    return meetings;
  }

  public void updateMeetingRacesWithEntries(List<HRRace> races, Date date) {
    DateFormat df = Tools.simpleDateFormat("yyyy-MM-dd");
    String strDate = df.format(date);
    Map<HRMeeting.HRMeetingKey, HRMeeting> map = getMap();
    Map<HRMeeting.HRMeetingKey, HRMeeting> result =
        map.entrySet().stream()
            .filter(
                mapEntry -> {
                  HRMeeting meeting = (HRMeeting) mapEntry.getValue();
                  return meeting.getMeetingDate().contains(strDate);
                })
            .map(
                entry -> {
                  HRMeeting meeting = entry.getValue();
                  races.stream()
                      .filter(
                          race ->
                              entry
                                  .getKey()
                                  .equals(
                                      new HRMeeting.HRMeetingKey(
                                          race.getMeetingDate(), race.getCourseId())))
                      .forEach(
                          newRace -> {
                            Optional<HRRace> matchedRace =
                                meeting.getRaces().stream()
                                    .filter(origin -> origin.getKey().equals(newRace.getKey()))
                                    .findFirst();
                            if (newRace.getEntries() != null && matchedRace.isPresent()) {
                              newRace.setUpdateDate(date);
                              newRace.getEntries().stream()
                                  .filter(
                                      hrEntry ->
                                          matchedRace.get().getEntries().stream()
                                              .map(el -> el.getKey())
                                              .collect(Collectors.toList())
                                              .contains(hrEntry.getKey()))
                                  .forEach(hrEntry -> hrEntry.setUpdateDate(date));
                              matchedRace.get().getEntries().retainAll(newRace.getEntries());
                              newRace.getEntries().addAll(matchedRace.get().getEntries());
                              // keep courseMapId during races update
                              newRace.setCourseMapId(matchedRace.get().getCourseMapId());
                            }
                            meeting
                                .getRaces()
                                .removeIf(
                                    hrRace ->
                                        matchedRace.isPresent()
                                            && matchedRace.get().getKey().equals(hrRace.getKey()));
                            meeting.getRaces().add(newRace);
                          });
                  return entry;
                })
            .collect(Collectors.toMap(e -> e.getKey(), e -> e.getValue()));
    map.putAll(result);
  }

  @Override
  public Collection<? extends TimeformMeeting> getMeetingsByDate(Date date) {
    return getMeetingsMapForDate(date).values();
  }

  public void updateMeetingRacesWithEntries(Map<HRMeeting, List<HRRace>> updatedRacesWithEntries) {
    Map<HRMeeting.HRMeetingKey, HRMeeting> map = getMap();
    Map<HRMeeting.HRMeetingKey, HRMeeting> result =
        map.entrySet().stream()
            .filter(mapEntry -> updatedRacesWithEntries.containsKey(mapEntry.getValue()))
            .map(
                entry -> {
                  LOGGER.info("Update meeting {} races and entries", entry.getKey());
                  entry
                      .getValue()
                      .getRaces()
                      .forEach(
                          race -> {
                            HRRace mergedRace =
                                updatedRacesWithEntries.get(entry.getValue()).stream()
                                    .filter(r -> r.getKey().equals(race.getKey()))
                                    .findFirst()
                                    .get();
                            race.getOpenBetIds().addAll(mergedRace.getOpenBetIds());
                            race.getEntries()
                                .forEach(
                                    e -> {
                                      HREntry resultEntry =
                                          mergedRace.getEntries().stream()
                                              .filter(
                                                  mergedEntry ->
                                                      mergedEntry.getKey().equals(e.getKey()))
                                              .findFirst()
                                              .get();
                                      e.getOpenBetIds().addAll(resultEntry.getOpenBetIds());
                                    });
                          });
                  return entry;
                })
            .collect(Collectors.toMap(e -> e.getKey(), e -> e.getValue()));
    map.putAll(result);
  }

  // @Cacheable("hrMeetings::filter")
  public List<HRMeeting> getMeetings(Integer top, Integer skip, String orderby, String filter) {
    return QueryStream.of(getMeetings(), filter, orderby, top, skip).toList();
  }

  // @Cacheable("hrMeetings::byOpenbetIds")
  public List<HRMeeting> getMeetingsByOpenbetIds(List<Integer> openbetId) {
    return getMeetings().stream()
        .filter(m -> filterByOpenbetIds(openbetId, m))
        .collect(Collectors.toList());
  }

  protected boolean filterByOpenbetIds(List<Integer> openbetId, OBRelatedEntity m) {
    return openbetId.stream()
            .filter(id -> m.getOpenBetIds() != null && m.getOpenBetIds().contains(id))
            .count()
        > 0;
  }

  // @Cacheable("hrRaces::byOpenbetIds")
  public List<HRRace> getRacesByOpenbetIds(List<Integer> openbetId) {
    return getRaces().stream()
        .filter(m -> filterByOpenbetIds(openbetId, m))
        .collect(Collectors.toList());
  }

  // @Cacheable("hrRaces::filter")
  public List<HRRace> getRaces(Integer top, Integer skip, String orderby, String filter) {
    return QueryStream.of(getRaces(), filter, orderby, top, skip).toList();
  }

  private List<HRRace> getRaces() {
    return getMeetings().stream().flatMap(v -> getRacesStream(v)).collect(Collectors.toList());
  }

  private Stream<HRRace> getRacesStream(HRMeeting v) {
    Collection<HRRace> races = v.getRaces();
    return races != null ? races.stream() : com.egalacoral.spark.timeform.tools.Tools.emptyStream();
  }

  // @Cacheable("hrEntries::filter")
  public List<HREntry> getEntries(Integer top, Integer skip, String orderby, String filter) {
    return QueryStream.of(getEntries(), filter, orderby, top, skip).toList();
  }

  // @Cacheable("hrEntries::byOpenbetIds")
  public List<HREntry> getEntriesByOpenbetId(List<Integer> openbetId) {
    return getEntries().stream()
        .filter(m -> filterByOpenbetIds(openbetId, m))
        .collect(Collectors.toList());
  }

  private List<HREntry> getEntries() {
    return getRaces().stream().flatMap(v -> getEntriesStream(v)).collect(Collectors.toList());
  }

  private Stream<HREntry> getEntriesStream(HRRace v) {
    Collection<HREntry> entries = v.getEntries();
    return entries != null
        ? entries.stream()
        : com.egalacoral.spark.timeform.tools.Tools.emptyStream();
  }

  public void updateRaceCourseMapId(HRMeeting meeting, HRRace race, String courseMapId) {
    Map<HRMeeting.HRMeetingKey, HRMeeting> map = getMap();
    Map<HRMeeting.HRMeetingKey, HRMeeting> result =
        map.entrySet().stream()
            .filter(mapEntry -> mapEntry.getKey().equals(meeting.getKey()))
            .map(
                entry -> {
                  Optional<HRRace> first =
                      entry.getValue().getRaces().stream()
                          .filter(r -> r.getKey().equals(race.getKey()))
                          .findFirst();
                  if (first.isPresent()) {
                    first.get().setCourseMapId(courseMapId);
                  }
                  return entry;
                })
            .collect(Collectors.toMap(e -> e.getKey(), e -> e.getValue()));
    map.putAll(result);
  }
}
