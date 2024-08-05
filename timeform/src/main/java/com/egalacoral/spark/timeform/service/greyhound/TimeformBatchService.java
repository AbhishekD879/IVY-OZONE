package com.egalacoral.spark.timeform.service.greyhound;

import static com.egalacoral.spark.timeform.service.greyhound.TimeformGreyhoundService.GREYHOUND_CACHE_NAME;
import static java.util.stream.Collectors.groupingBy;

import com.egalacoral.spark.timeform.actions.ActionCalendar;
import com.egalacoral.spark.timeform.actions.ActionCalendarImpl;
import com.egalacoral.spark.timeform.actions.ChainedAction;
import com.egalacoral.spark.timeform.actions.DatedAction;
import com.egalacoral.spark.timeform.api.DataCallback;
import com.egalacoral.spark.timeform.api.TimeFormService;
import com.egalacoral.spark.timeform.entity.GreyhoundEntity;
import com.egalacoral.spark.timeform.entity.PositionEntity;
import com.egalacoral.spark.timeform.model.greyhound.*;
import com.egalacoral.spark.timeform.model.internal.DataResponse;
import com.egalacoral.spark.timeform.repository.GreyhoundEntityRepository;
import com.egalacoral.spark.timeform.service.ActionCalendarStorageService;
import com.egalacoral.spark.timeform.service.LockService;
import com.egalacoral.spark.timeform.service.MissingDataChecker;
import com.egalacoral.spark.timeform.storage.Storage;
import com.egalacoral.spark.timeform.tools.Tools;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TimeformBatchService {

  private static final Logger LOGGER = LoggerFactory.getLogger(TimeformBatchService.class);
  private static final String TRACK_PREFIX = "GR-track";
  private static final String PERFORMANCE_PREFIX = "GR-performance";
  private static final String GREYHOUND_PREFIX = "GR-greyhound";
  private static final String RACE_ENTRIES_PREFIX = "GR-race_entries";
  private static final String MEETING_PREFIX = "GR-meeting";
  private static final String FORM_PREFIX = "GR-form";
  private static final long TRACK_LOCK_TIME = 10L * 60;
  private static final long PERFORMANCE_LOCK_TIME = 30L;
  private static final long GREYHOUND_LOCK_TIME = 6L * 60;
  private static final long RACE_ENTRIES_LOCK_TIME = 3L * 60;
  private static final long MEETING_LOCK_TIME = 3L * 60;
  private static final long FORM_LOCK_TIME = 15L * 60;
  public static final String MEETINGS_ARE_LOCKED = "Meetings are locked";

  public static final int GREYHOUND_CALL_ITEMS_COUNT = 15;

  private MeetingMappingService mappingService;

  private RacesMappingService racesMappingService;

  private TimeformMeetingService timeformMeetingService;

  private TimeformGreyhoundService timeformGreyhoundService;

  private TimeformPerformanceService timeformPerformanceService;

  private TimeformTrackService timeformTrackService;

  private TimeFormService timeFormService;

  private final MeetingFilterService meetingFilterService;

  private final MissingDataChecker missingDataChecker;

  private final GreyhoundEntityRepository greyhoundPositionDynamoRepository;

  private Storage storage;

  private LockService lockService;

  private ActionCalendar calendar;

  private GreyhoundUtils greyhoundUtils;

  @Autowired
  public TimeformBatchService(
      TimeformMeetingService timeformMeetingService,
      TimeFormService timeFormService,
      MeetingFilterService meetingFilterService,
      MissingDataChecker missingDataChecker,
      GreyhoundEntityRepository greyhoundPositionDynamoRepository,
      Storage storage,
      ActionCalendarStorageService calendarStorageService,
      GreyhoundUtils greyhoundUtils) {
    this.timeformMeetingService = timeformMeetingService;
    this.timeFormService = timeFormService;
    this.meetingFilterService = meetingFilterService;
    this.missingDataChecker = missingDataChecker;
    this.greyhoundPositionDynamoRepository = greyhoundPositionDynamoRepository;
    this.storage = storage;
    this.calendar = new ActionCalendarImpl(calendarStorageService);
    this.greyhoundUtils = greyhoundUtils;
  }

  public void fetchMeetingsByAdHocRequest(Date date) {
    LOGGER.info("Fetching meetings by Ad Hoc Request for date {}", date);
    DatedAction fetchMeetings = new FetchMeetingsAction(date);
    fetchMeetings.setAfter(new TimeformBatchService.MapMeetingWithOpenBetAction(date));
    fetchMeetings.forceSuccessRemove();
    fetchMeetings.call();
  }

  public void processMeetings(Date date) {
    ChainedAction fetchMeetings = new FetchMeetingsAction(date);
    fetchMeetings.setAfter(new TimeformBatchService.MapMeetingWithOpenBetAction(date));
    fetchMeetings.call();
  }

  public void consumeRacesWithEntries(Date date) {
    DatedAction fetchMeetings = new FetchMeetingsAction(date);
    ChainedAction fetchMeetingsIfNeeded = fetchMeetings.ifWasNotPerformed();
    DatedAction fetchRacesWithEntries = new FetchRacesWithEntriesAction(date);
    ChainedAction mapMeetingsIfNeeded =
        new MapMeetingWithOpenBetAction(date).ifWasBefore(fetchMeetings);
    DatedAction mapRacesWithEntries = new MapRacesWithEntriesToOpenBetAction(date);

    fetchMeetingsIfNeeded.setAfter(fetchRacesWithEntries);
    fetchRacesWithEntries.setAfter(mapMeetingsIfNeeded);
    mapMeetingsIfNeeded.setAfter(mapRacesWithEntries);

    fetchMeetingsIfNeeded.call();
  }

  private class FetchMeetingsAction extends DatedAction {

    public FetchMeetingsAction(Date targetDate) {
      super(targetDate, calendar, "greyhound fetch meeting");
      setAsyncMode(true);
      setAction(
          (chainedWrapper) -> {
            String lockName = generateLockName(MEETING_PREFIX, targetDate);
            lockService.tryLockWithWrapper(
                lockName,
                MEETING_LOCK_TIME,
                wrapper -> {
                  LOGGER.info(
                      "No date is available in hazelcast, therefore fetch new for {}", targetDate);
                  timeFormService.getMeetingsForDate(
                      targetDate,
                      chainedWrapper.wrap(
                          wrapper.wrap(
                              new DataCallback<List<Meeting>>() {
                                @Override
                                public void onResponse(List<Meeting> meetings) {
                                  if (meetings != null && !meetings.isEmpty()) {
                                    LOGGER.info(
                                        "Received meetings: {}"
                                            + meetings
                                                .parallelStream()
                                                .map(Meeting::getName)
                                                .collect(Collectors.joining(", ")));
                                    Set<Integer> storedMeetingIds =
                                        timeformMeetingService.getMeetingsByDate(targetDate)
                                            .stream() //
                                            .map(Meeting::getMeetingId) //
                                            .collect(Collectors.toSet());

                                    List<Meeting> newMeetings =
                                        meetings.stream() //
                                            .filter(
                                                m ->
                                                    !storedMeetingIds.contains(
                                                        m.getMeetingId())) //
                                            .filter(
                                                m ->
                                                    meetingFilterService.accept(
                                                        m.getTrackShortName())) //
                                            .collect(Collectors.toList());
                                    LOGGER.info("Fetched {} new meetings", newMeetings.size());
                                    timeformMeetingService.save(newMeetings);
                                  }
                                }

                                @Override
                                public void onError(Exception e) {
                                  LOGGER.error("Could not fetch meetings.", e);
                                }
                              })));
                });
          });
    }
  }

  private class MapMeetingWithOpenBetAction extends DatedAction {

    public MapMeetingWithOpenBetAction(Date targetDate) {
      super(targetDate, calendar, "greyhound map meetings");
      setAction(
          dataCallbackWrapper -> {
            Map<Integer, Meeting> meetingMap =
                timeformMeetingService.getMeetingsMapForDate(targetDate);
            if (meetingMap.size() > 0) {
              mappingService.initMappers();
              mappingService.map((meetingMap.values().stream().collect(Collectors.toList())));
              timeformMeetingService.updateMeetingOpenBetMapping(meetingMap);
            }
          });
    }
  }

  private class MapRacesWithEntriesToOpenBetAction extends DatedAction {

    public MapRacesWithEntriesToOpenBetAction(Date targetDate) {
      super(targetDate, calendar, "greyhound map races with entries");
      setAction(
          dataCallbackWrapper -> {
            Map<Integer, Meeting> meetingMap =
                timeformMeetingService.getMeetingsMapForDate(targetDate);
            if (meetingMap.size() > 0) {
              racesMappingService.initMappers();
              racesMappingService.map(meetingMap.values().stream().collect(Collectors.toList()));
              timeformMeetingService.updateRacesWithEntriesOpenBetMapping(meetingMap);
              missingDataChecker.validate(targetDate);
            }
          });
      addOnError(
          exception -> {
            missingDataChecker.validate(targetDate);
          });
    }
  }

  private class FetchRacesWithEntriesAction extends DatedAction {
    public FetchRacesWithEntriesAction(Date targetDate) {
      super(targetDate, calendar, "greyhound fetch races with entries ");
      setAsyncMode(true);
      setAction(
          (chainedWrapper) -> {
            String lockName = generateLockName(RACE_ENTRIES_PREFIX, targetDate);
            lockService.tryLockWithWrapper(
                lockName,
                RACE_ENTRIES_LOCK_TIME,
                wrapper -> {
                  if (!timeformMeetingService.isRacesWithEntriesExistForUpdateDate(targetDate)) {
                    Map<Integer, Meeting> meetingsMap =
                        new HashMap<>(timeformMeetingService.getMeetingsMapForDate(targetDate));
                    if (meetingsMap.size() > 0) {
                      timeFormService.getRacesWithEntriesByMeetingDate(
                          targetDate,
                          chainedWrapper.wrap(
                              wrapper.wrap(
                                  new DataCallback<List<Race>>() {
                                    @Override
                                    public void onResponse(List<Race> races) {
                                      Map<Integer, Greyhound> greyhounds =
                                          storage.getMap(GREYHOUND_CACHE_NAME);
                                      Map<Integer, Set<Race>> filteredRaces =
                                          races.stream()
                                              .filter(
                                                  race ->
                                                      meetingsMap.get(race.getMeetingId()) != null)
                                              .collect(
                                                  groupingBy(
                                                      race -> race.getMeetingId(),
                                                      Collectors.toSet()));
                                      filteredRaces
                                          .values()
                                          .forEach(
                                              set ->
                                                  set.forEach(
                                                      race -> {
                                                        race.setUpdateDate(targetDate);
                                                        setGreyhoundFormIfExists(greyhounds, race);
                                                      }));
                                      timeformMeetingService.updateRacesWithEntries(filteredRaces);
                                    }

                                    private void setGreyhoundFormIfExists(
                                        Map<Integer, Greyhound> greyhounds, Race race) {
                                      race.getEntries()
                                          .forEach(
                                              entry -> {
                                                entry.setUpdateDate(targetDate);
                                                Optional.ofNullable(
                                                        greyhounds.get(entry.getGreyhoundId()))
                                                    .ifPresent(
                                                        greyhound ->
                                                            entry.setForm(greyhound.getForm()));
                                              });
                                    }

                                    @Override
                                    public void onError(Exception e) {
                                      LOGGER.error("Consuming races with entries error", e);
                                    }
                                  })));
                    } else {
                      LOGGER.info(
                          "GreyhoundEntity meetings were not found for date {}, therefore skip races with entries fetching.",
                          targetDate);
                    }
                  } else {
                    LOGGER.info("Races with entries are already processed");
                  }
                });
          });
    }
  }

  public void consumeGreyhounds(Date date) {
    String lockName = generateLockName(GREYHOUND_PREFIX, date);
    lockService.tryLockWithWrapper(
        lockName,
        GREYHOUND_LOCK_TIME,
        (LockService.UnlockWrapper wrapper) -> {
          if (!timeformGreyhoundService.isGreyhoundsForDateExist(date)) {
            timeFormService.getEntriesGreyhoundByMeetingDate(
                date,
                wrapper.wrap(
                    new DataCallback<List<Entry>>() {
                      @Override
                      public void onResponse(List<Entry> entries) {
                        Map<Integer, Greyhound> newGreyhoundsMap =
                            entries.stream()
                                .map(Entry::getGreyhound)
                                .collect(
                                    Collectors.toMap(
                                        Greyhound::getGreyhoundId,
                                        Tools.identity(),
                                        (greyhound1, greyhound2) -> greyhound2));
                        timeformGreyhoundService.updateGreyhounds(newGreyhoundsMap, date);
                        List<GreyhoundEntity> dynamoDbGreyhounds =
                            greyhoundPositionDynamoRepository.findByGreyhoundIdIn(
                                newGreyhoundsMap.keySet());
                        Map<Integer, Greyhound> filteredGreyhounds =
                            filterNotExistedAtDb(newGreyhoundsMap, dynamoDbGreyhounds);
                        paginateFormCalls(filteredGreyhounds, GREYHOUND_CALL_ITEMS_COUNT);
                      }

                      private void paginateFormCalls(
                          Map<Integer, Greyhound> filteredGreyhounds, int greyhoundCallItemsCount) {
                        Map<Integer, Greyhound> smallMap = new HashMap<>();
                        int mapCount = 0;
                        for (Map.Entry<Integer, Greyhound> greyhoundEntry :
                            filteredGreyhounds.entrySet()) {
                          if (mapCount < greyhoundCallItemsCount) {
                            smallMap.put(greyhoundEntry.getKey(), greyhoundEntry.getValue());
                            mapCount++;
                          } else {
                            saveFormFieldDataAtDb(smallMap);
                            smallMap = new HashMap<>();
                            mapCount = 0;
                          }
                        }
                        if (!smallMap.isEmpty()) {
                          saveFormFieldDataAtDb(smallMap);
                        }
                      }

                      private Map<Integer, Greyhound> filterNotExistedAtDb(
                          Map<Integer, Greyhound> newGreyhoundsMap,
                          List<GreyhoundEntity> dynamoDbGreyhounds) {
                        List<Integer> greyhoundDynamoDbIds =
                            dynamoDbGreyhounds.stream()
                                .map(g -> g.getGreyhoundId())
                                .collect(Collectors.toList());
                        return newGreyhoundsMap.entrySet().stream()
                            .filter(e -> !greyhoundDynamoDbIds.contains(e.getKey()))
                            .collect(Collectors.toMap(e -> e.getKey(), e -> e.getValue()));
                      }

                      private void saveFormFieldDataAtDb(Map<Integer, Greyhound> newGreyhoundsMap) {
                        Calendar calendar = Calendar.getInstance();
                        calendar.set(GreyhoundUtils.getLastYear(), 0, 1);
                        Date lastNewYearDate = calendar.getTime();
                        List<Integer> greyhoundIds = new ArrayList<>(newGreyhoundsMap.keySet());
                        timeFormService.getPerformancesMeetingsAfterDateForCreatingFormField(
                            lastNewYearDate,
                            greyhoundIds,
                            new DataCallback<DataResponse<Performance>>() {
                              @Override
                              public void onResponse(DataResponse<Performance> data) {
                                List<Performance> performances = data.getEntities();
                                Set<Map.Entry<Integer, List<Performance>>> performanceEntries =
                                    performances.stream()
                                        .collect(groupingBy(Performance::getGreyhoundId))
                                        .entrySet();
                                saveGreyhoundsPositionsAtDynamoDb(performanceEntries);
                              }

                              private void saveGreyhoundsPositionsAtDynamoDb(
                                  Set<Map.Entry<Integer, List<Performance>>> performanceEntries) {
                                List<GreyhoundEntity> greyhoundEntities =
                                    performanceEntries.stream()
                                        .map(entry -> createGreyhoundPositionData(entry))
                                        .collect(Collectors.toList());
                                greyhoundPositionDynamoRepository.save(greyhoundEntities);
                              }

                              private GreyhoundEntity createGreyhoundPositionData(
                                  Map.Entry<Integer, List<Performance>> entry) {
                                return GreyhoundEntity.GreyhoundEntityBuilder.aGreyhoundEntity()
                                    .greyhoundId(entry.getKey())
                                    .lastUpdate(GreyhoundUtils.getTodayDay())
                                    .positionEntities(createPositionEntries(entry))
                                    .build();
                              }

                              private List<PositionEntity> createPositionEntries(
                                  Map.Entry<Integer, List<Performance>> entry) {
                                return entry.getValue().stream()
                                    .map(
                                        e ->
                                            PositionEntity.PositionEntityBuilder.aPositionEntity()
                                                .meetingDate(e.getMeeting().getMeetingDate())
                                                .positionStatus(e.getPositionStatus())
                                                .build())
                                    .collect(Collectors.toList());
                              }

                              @Override
                              public void onError(Exception e) {
                                LOGGER.error(
                                    "Could not fill form at greyhounds, cause {}", e.getMessage());
                              }
                            });
                      }

                      @Override
                      public void onError(Exception e) {
                        LOGGER.error("Could not fetch greyhounds, cause {}", e.getMessage());
                      }
                    }));
          } else {
            LOGGER.info("Greyhounds are already processed");
          }
        });
  }

  public void consumePerformances(Date date) {
    String lockName = generateLockName(PERFORMANCE_PREFIX, date);
    lockService.tryLockWithWrapper(
        lockName,
        PERFORMANCE_LOCK_TIME,
        wrapper -> {
          if (!timeformPerformanceService.isPerformancesForDateExist(date)) {
            timeFormService.getPerformancesByMeetingDate(
                date,
                wrapper.wrap(
                    new DataCallback<List<Performance>>() {
                      @Override
                      public void onResponse(List<Performance> performances) {
                        Map<Integer, Performance> newPerformancesMap =
                            performances.stream()
                                .collect(
                                    Collectors.toMap(
                                        Performance::getPerformanceId,
                                        v -> v,
                                        (key1, key2) -> key2));
                        timeformPerformanceService.updatePerformances(newPerformancesMap, date);
                        List<GreyhoundEntity> dynamoGreyhounds =
                            retrieveGreyhoundEntities(newPerformancesMap);
                        saveGreyhoundPositionAtDynamoDB(newPerformancesMap, dynamoGreyhounds);
                      }

                      private List<GreyhoundEntity> retrieveGreyhoundEntities(
                          Map<Integer, Performance> newPerformancesMap) {
                        List<Integer> greyhoundIds =
                            newPerformancesMap.entrySet().stream()
                                .map(e -> e.getValue().getGreyhoundId())
                                .collect(Collectors.toList());
                        return greyhoundPositionDynamoRepository.findByGreyhoundIdIn(greyhoundIds);
                      }

                      private void saveGreyhoundPositionAtDynamoDB(
                          Map<Integer, Performance> newPerformancesMap,
                          List<GreyhoundEntity> greyhounds) {
                        List<GreyhoundEntity> newGreyhounds =
                            newPerformancesMap.entrySet().stream()
                                .map(
                                    e -> {
                                      Performance performance = e.getValue();
                                      GreyhoundEntity greyhoundEntity =
                                          buildOrUpdateGreyhoundWithPositions(
                                              performance, greyhounds);
                                      return greyhoundEntity;
                                    })
                                .filter(Objects::nonNull)
                                .collect(Collectors.toList());
                        greyhoundPositionDynamoRepository.save(newGreyhounds);
                      }

                      private GreyhoundEntity buildOrUpdateGreyhoundWithPositions(
                          Performance performance, List<GreyhoundEntity> greyhounds) {
                        Optional<GreyhoundEntity> greyhoundEntity =
                            greyhounds.stream()
                                .filter(
                                    g -> g.getGreyhoundId().equals(performance.getGreyhoundId()))
                                .findAny();
                        if (greyhoundEntity.isPresent()) {
                          return updatePosititions(performance, greyhoundEntity.get());
                        }
                        return null;
                      }

                      private GreyhoundEntity updatePosititions(
                          Performance performance, GreyhoundEntity greyhoundEntity) {
                        List<PositionEntity> positionList =
                            Optional.ofNullable(greyhoundEntity.getPositionEntities())
                                .orElse(new ArrayList<>());
                        PositionEntity positionEntity =
                            PositionEntity.PositionEntityBuilder.aPositionEntity()
                                .positionStatus(performance.getPositionStatus())
                                .meetingDate(performance.getMeeting().getMeetingDate())
                                .build();
                        if (!positionList.contains(positionEntity)) {
                          positionList.add(positionEntity);
                        }
                        greyhoundEntity.setPositionEntities(positionList);
                        return greyhoundEntity;
                      }

                      @Override
                      public void onError(Exception e) {
                        LOGGER.error("Could not fetch performances, cause {}", e.getMessage());
                      }
                    }));
          } else {
            LOGGER.info("Performances are already processed");
          }
        });
  }

  public void updateForm(Date date) {
    String lockName = generateLockName(FORM_PREFIX, date);
    lockService.tryLockWithWrapper(
        lockName,
        FORM_LOCK_TIME,
        wrapper -> {
          Map<Integer, Greyhound> redisGreyhounds = storage.getMap(GREYHOUND_CACHE_NAME);
          Map<Integer, Greyhound> updatedGreyhounds =
              redisGreyhounds.entrySet().stream()
                  .map(
                      g -> {
                        Optional<GreyhoundEntity> greyhoundEntity =
                            greyhoundPositionDynamoRepository.findByGreyhoundId(g.getKey());
                        if (greyhoundEntity.isPresent()) {
                          Greyhound greyhound = g.getValue();
                          greyhound.setForm(GreyhoundUtils.regenerateForm(greyhoundEntity.get()));
                          return greyhound;
                        }
                        return null;
                      })
                  .filter(Objects::nonNull)
                  .collect(Collectors.toMap(g -> g.getGreyhoundId(), g -> g));
          timeformGreyhoundService.updateGreyhounds(updatedGreyhounds, date);
        });
  }

  public void consumeTracks(Date date) {
    DatedAction consumeTracks = new ConsumeTracksAction(date);
    ChainedAction consumeTracksIfNeeded = consumeTracks.ifWasNotPerformed();
    consumeTracksIfNeeded.call();
  }

  private class ConsumeTracksAction extends DatedAction {

    public ConsumeTracksAction(Date targetDate) {
      super(targetDate, calendar, "greyhound tracks fetch");
      setAsyncMode(true);
      setAction(
          dataCallbackWrapper -> {
            String lockName = generateLockName(TRACK_PREFIX, new Date());
            lockService.tryLockWithWrapper(
                lockName,
                TRACK_LOCK_TIME,
                wrapper -> {
                  Collection<Integer> trackIds = timeformTrackService.getTracksIds();
                  timeFormService.getTracks(
                      dataCallbackWrapper.wrap(
                          wrapper.wrap(
                              new DataCallback<List<Track>>() {
                                @Override
                                public void onResponse(List<Track> tracks) {
                                  Map<Integer, Track> tracksMap =
                                      tracks.stream()
                                          .collect(
                                              Collectors.toMap(
                                                  Track::getTrackId,
                                                  Tools.identity(),
                                                  (track1, track2) -> track1));
                                  tracksMap.entrySet().stream()
                                      .filter(element -> trackIds.contains(element.getKey()))
                                      .forEach(
                                          element -> element.getValue().setUpdateDate(new Date()));
                                  timeformTrackService.save(tracksMap);
                                }

                                @Override
                                public void onError(Exception e) {
                                  LOGGER.error("Could not fetch tracks, cause {}", e.getMessage());
                                }
                              })));
                });
          });
    }
  }

  private String generateLockName(String prefix, Date date) {
    SimpleDateFormat sdf =
        com.egalacoral.spark.timeform.api.tools.Tools.simpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
    String dateStr = sdf.format(date);

    return prefix + ":" + dateStr;
  }

  @Autowired
  public void setMappingService(MeetingMappingService mappingService) {
    this.mappingService = mappingService;
  }

  @Autowired
  public void setRacesMappingService(RacesMappingService racesMappingService) {
    this.racesMappingService = racesMappingService;
  }

  @Autowired
  public void setTimeformGreyhoundService(TimeformGreyhoundService timeformGreyhoundService) {
    this.timeformGreyhoundService = timeformGreyhoundService;
  }

  @Autowired
  public void setTimeformPerformanceService(TimeformPerformanceService timeformPerformanceService) {
    this.timeformPerformanceService = timeformPerformanceService;
  }

  @Autowired
  public void setTimeformTrackService(TimeformTrackService timeformTrackService) {
    this.timeformTrackService = timeformTrackService;
  }

  @Autowired
  public void setLockService(LockService lockService) {
    this.lockService = lockService;
  }
}
