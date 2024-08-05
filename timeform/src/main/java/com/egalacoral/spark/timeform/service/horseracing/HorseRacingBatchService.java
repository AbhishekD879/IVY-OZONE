package com.egalacoral.spark.timeform.service.horseracing;

import com.egalacoral.spark.timeform.actions.ActionCalendar;
import com.egalacoral.spark.timeform.actions.ActionCalendarImpl;
import com.egalacoral.spark.timeform.actions.ChainedAction;
import com.egalacoral.spark.timeform.actions.DatedAction;
import com.egalacoral.spark.timeform.api.DataCallback;
import com.egalacoral.spark.timeform.api.TimeFormService;
import com.egalacoral.spark.timeform.model.horseracing.*;
import com.egalacoral.spark.timeform.model.horseracing.key.HRPerformanceKey;
import com.egalacoral.spark.timeform.service.ActionCalendarStorageService;
import com.egalacoral.spark.timeform.service.LockService;
import com.egalacoral.spark.timeform.service.MissingDataChecker;
import com.egalacoral.spark.timeform.service.SchedulerService;
import com.egalacoral.spark.timeform.service.horseracing.mapper.HREntriesOpenBetMapper;
import com.egalacoral.spark.timeform.service.horseracing.mapper.HRRacesOpenBetMapper;
import com.egalacoral.spark.timeform.service.horseracing.mapper.HorseRacingMeetingTypeMapper;
import com.egalacoral.spark.timeform.tools.Tools;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

@Component
public class HorseRacingBatchService {

  private static final transient Logger LOGGER =
      LoggerFactory.getLogger(HorseRacingBatchService.class);

  private static final String MEETING_PREFIX = "HR-Meetings-Fetch";
  private static final String RACES_ENTRIES_PREFFIX = "HR-Races-Entries-Fetch";
  private static final String HR_PERFORMANCE_PREFIX = "HR-Performances-Fetch";
  private static final String HR_HORSES_PREFIX = "HR-Horses-Fetch";
  private static final String HR_COURSES_PREFIX = "HR-Courses-Fetch";
  private static final String HR_COUNTRIES_PREFIX = "HR-Countries-Fetch";
  private static final String HR_COURSE_MAPS_PREFIX = "HR-CourseRaces-Fetch";

  private static final long MEETING_LOCK_TIME = 3L * 60;
  private static final long RACES_ENTRIES_LOCK_TIME = 3L * 60;
  private static final long HR_PERFORMANCE_LOCK_TIME = 3L * 60;
  private static final long HR_HORSES_LOCK_TIME = 3L * 60;
  private static final long HR_COURSES_LOCK_TIME = 3L * 60;
  private static final long HR_COUNTRIES_LOCK_TIME = 3L * 60;
  private static final long HR_COURSE_MAPS_LOCK_TIME = 3L * 60 * 1000;

  private final LockService lockService;

  private final TimeFormService timeFormService;

  private HorseRacingPerformanceService horseRacingPerformanceService;

  private HorseRacingHorseService horseRacingHorseService;

  private HorseRacingCourseService horseRacingCourseService;

  private HorseRacingCountriesService horseRacingCountriesService;

  private HorseRacingCourseMapService horseRacingCourseMapService;

  private final HorseRacingStorageService storageService;

  private final HorseRacingMeetingTypeMapper meetingTypeMapper;

  private final HRRacesOpenBetMapper hrRacesOpenBetMapper;

  private final HREntriesOpenBetMapper hrEntriesOpenBetMapper;

  private final MissingDataChecker missingDataChecker;

  private ActionCalendar calendar;

  private SchedulerService schedulerService;

  @Autowired
  public HorseRacingBatchService(
      TimeFormService timeFormService,
      HorseRacingStorageService storageService,
      HorseRacingPerformanceService horseRacingPerformanceService,
      HorseRacingHorseService horseRacingHorseService,
      HorseRacingCourseService horseRacingCourseService,
      HorseRacingCountriesService horseRacingCountriesService,
      LockService lockService,
      HRRacesOpenBetMapper hrRacesOpenBetMapper,
      HorseRacingMeetingTypeMapper meetingTypeMapper,
      HREntriesOpenBetMapper hrEntriesOpenBetMapper,
      @Qualifier("horses") MissingDataChecker missingDataChecker,
      ActionCalendarStorageService calendarStorageService,
      HorseRacingCourseMapService horseRacingCourseMapService,
      SchedulerService schedulerService) {
    this.timeFormService = timeFormService;
    this.storageService = storageService;
    this.horseRacingPerformanceService = horseRacingPerformanceService;
    this.horseRacingHorseService = horseRacingHorseService;
    this.horseRacingCourseService = horseRacingCourseService;
    this.horseRacingCountriesService = horseRacingCountriesService;
    this.lockService = lockService;
    this.hrRacesOpenBetMapper = hrRacesOpenBetMapper;
    this.meetingTypeMapper = meetingTypeMapper;
    this.calendar = new ActionCalendarImpl(calendarStorageService);
    this.hrEntriesOpenBetMapper = hrEntriesOpenBetMapper;
    this.missingDataChecker = missingDataChecker;
    this.horseRacingCourseMapService = horseRacingCourseMapService;
    this.schedulerService = schedulerService;
  }

  public void fetchMeetingsForDate(Date date) {
    ChainedAction action = new FetchMeetingForDateAction(date);
    action.setAfter(new MapMeetingWithOpenBet(date));
    action.call();
  }

  private class FetchMeetingForDateAction extends DatedAction {

    public FetchMeetingForDateAction(Date targetDate) {
      super(targetDate, calendar, "horse racing fetch meetings");
      setAsyncMode(true);
      setAction(
          (chainedWrapper) -> {
            String lockName = generateLockName(MEETING_PREFIX, targetDate);
            lockService.tryLockWithWrapper(
                lockName,
                MEETING_LOCK_TIME,
                (wrapper) -> {
                  LOGGER.info("Fetching HorseRacing meetings for date {}", targetDate);
                  timeFormService.getHRMeetingsForDate(
                      targetDate,
                      chainedWrapper.wrap(
                          wrapper.wrap(
                              new DataCallback<List<HRMeeting>>() {
                                @Override
                                public void onResponse(List<HRMeeting> meetings) {
                                  List<HRMeeting> newMeetings =
                                      filterNewMeeting(meetings, targetDate);
                                  LOGGER.info(
                                      "For date {} received {} meetings. New meetings {}",
                                      targetDate,
                                      meetings.size(),
                                      newMeetings.size());
                                  storageService.save(newMeetings);
                                }

                                @Override
                                public void onError(Exception e) {
                                  LOGGER.error(
                                      "Could not fetch meetings, cause {}", e.getMessage());
                                }
                              })));
                });
          });
    }
  }

  private class MapMeetingWithOpenBet extends DatedAction {

    public MapMeetingWithOpenBet(Date targetDate) {
      super(targetDate, calendar, "horse racing map meetings");
      setAction(
          dataCallbackWrapper -> {
            Map<HRMeeting.HRMeetingKey, HRMeeting> meetingMap =
                storageService.getMeetingsMapForDate(targetDate);
            if (meetingMap.size() > 0) {
              meetingTypeMapper.loadTypesFromOB();
              meetingMap
                  .values()
                  .forEach(
                      m -> {
                        Set<Integer> obIds = meetingTypeMapper.getOBIdsForMeeting(m);
                        if (!obIds.isEmpty()) {
                          m.setOpenBetIds(obIds);
                        }
                      });
              storageService.update(meetingMap);
            }
          });
    }
  }

  private class MapRacesWithEntriesToOpenBet extends DatedAction {

    public MapRacesWithEntriesToOpenBet(Date targetDate) {
      super(targetDate, calendar, "horse racing map races and entries");
      setAction(
          dataCallbackWrapper -> {
            Map<HRMeeting.HRMeetingKey, HRMeeting> meetingMap =
                storageService.getMeetingsMapForDate(targetDate);
            if (meetingMap.size() > 0) {
              Map<HRMeeting, List<HRRace>> map =
                  meetingMap.values().stream()
                      .collect(
                          Collectors.toMap(
                              value -> value, value -> (List<HRRace>) value.getRaces()));
              hrRacesOpenBetMapper.mapRaces(map);
              hrEntriesOpenBetMapper.mapEntries(map);
              storageService.updateMeetingRacesWithEntries(map);
              missingDataChecker.validate(targetDate);
            }
          });
      addOnError(
          exception -> {
            missingDataChecker.validate(targetDate);
          });
    }
  }

  private class FetchRacesWithEntriesForDateAction extends DatedAction {

    public FetchRacesWithEntriesForDateAction(Date targetDate) {
      super(targetDate, calendar, "horse racing fetch races/entries");
      setAsyncMode(true);
      setAction(
          (chainedWrapper) -> {
            String lockName = generateLockName(RACES_ENTRIES_PREFFIX, targetDate);
            lockService.tryLockWithWrapper(
                lockName,
                RACES_ENTRIES_LOCK_TIME,
                wrapper -> {
                  if (!storageService.isRacesWithEntriesExistForDate(targetDate)) {
                    Map<HRMeeting.HRMeetingKey, HRMeeting> meetingMap =
                        storageService.getMeetingsMapForDate(targetDate);
                    if (meetingMap != null && meetingMap.size() > 0) {
                      timeFormService.getHRRacesWithRacesByMeetingDate(
                          targetDate,
                          chainedWrapper.wrap(
                              wrapper.wrap(
                                  new DataCallback<List<HRRace>>() {
                                    @Override
                                    public void onResponse(List<HRRace> races) {
                                      LOGGER.info(
                                          "{} races have been fetched for {}",
                                          races.size(),
                                          targetDate);
                                      List<HRRace> filteredRaces =
                                          races.stream()
                                              .filter(
                                                  race ->
                                                      meetingMap.containsKey(
                                                          new HRMeeting.HRMeetingKey(
                                                              race.getMeetingDate(),
                                                              race.getCourseId())))
                                              .collect(Collectors.toList());
                                      storageService.updateMeetingRacesWithEntries(
                                          filteredRaces, targetDate);
                                    }

                                    @Override
                                    public void onError(Exception e) {
                                      LOGGER.error(
                                          "Could not fetch races with entries for date {}",
                                          targetDate);
                                    }
                                  })));
                    } else {
                      LOGGER.info(
                          "HR meetings were not found for date {}, therefore skip races with entries fetching.",
                          targetDate);
                    }
                  } else {
                    LOGGER.info("Races with entries already processed");
                  }
                });
          });
    }
  }

  public void fetchRacesWithEntriesForDate(Date date) {
    DatedAction fetchMeetings = new FetchMeetingForDateAction(date);
    ChainedAction fetchMeetingsIfNecessary = fetchMeetings.ifWasNotPerformed();
    DatedAction fetchRacesWithEntries = new FetchRacesWithEntriesForDateAction(date);
    ChainedAction mapMeetingsIfNecessary =
        new MapMeetingWithOpenBet(date).ifWasBefore(fetchMeetings);
    DatedAction mapRacesWithEntriesToOpenBet = new MapRacesWithEntriesToOpenBet(date);

    fetchMeetingsIfNecessary.setAfter(fetchRacesWithEntries);
    fetchRacesWithEntries.setAfter(mapMeetingsIfNecessary);
    mapMeetingsIfNecessary.setAfter(mapRacesWithEntriesToOpenBet);

    fetchMeetingsIfNecessary.call();
  }

  public void consumeHRPerformances(Date date) {
    String lockName = generateLockName(HR_PERFORMANCE_PREFIX, date);
    lockService.tryLockWithWrapper(
        lockName,
        HR_PERFORMANCE_LOCK_TIME,
        wrapper -> {
          if (!horseRacingPerformanceService.isHRPerformancesForDateExist(date)) {
            timeFormService.getHRPerformancesByMeetingDate(
                date,
                wrapper.wrap(
                    new DataCallback<List<HRPerformance>>() {
                      @Override
                      public void onResponse(List<HRPerformance> hrPerformances) {
                        LOGGER.info(
                            "{} horse racing performances have been fetched for {}",
                            hrPerformances.size(),
                            date);
                        Map<HRPerformanceKey, HRPerformance> newHRPerformancesMap =
                            hrPerformances.stream()
                                .collect(
                                    Collectors.toMap(
                                        hrPerformance -> new HRPerformanceKey(hrPerformance),
                                        Tools.identity()));
                        horseRacingPerformanceService.updatePerformances(
                            newHRPerformancesMap, date);
                      }

                      @Override
                      public void onError(Exception e) {
                        LOGGER.error(
                            "Could not fetch horse racing performances, cause {}", e.getMessage());
                      }
                    }));
          } else {
            LOGGER.info("Performances are already processed");
          }
        });
  }

  private class ConsumeHRHorsesAction extends DatedAction {

    public ConsumeHRHorsesAction(Date targetDate) {
      super(targetDate, calendar, "horse racing fetch horses");
      setAsyncMode(true);
      setAction(
          dataCallbackWrapper -> {
            String lockName = generateLockName(HR_HORSES_PREFIX, targetDate);
            lockService.tryLockWithWrapper(
                lockName,
                HR_HORSES_LOCK_TIME,
                wrapper -> {
                  if (!horseRacingHorseService.isNewHorsesForDateExist(targetDate)) {
                    timeFormService.getHREntriesHorsesByMeetingDate(
                        targetDate,
                        dataCallbackWrapper.wrap(
                            wrapper.wrap(
                                new DataCallback<List<HREntry>>() {
                                  @Override
                                  public void onResponse(List<HREntry> hrEntries) {
                                    Map<String, HRHorse> retrievedHorses =
                                        hrEntries.stream()
                                            .map(HREntry::getHorse)
                                            .collect(
                                                Collectors.toMap(
                                                    HRHorse::getHorseCode,
                                                    t -> t,
                                                    (horse1, horse2) -> horse2));
                                    horseRacingHorseService.updateHorses(
                                        retrievedHorses, targetDate);
                                  }

                                  @Override
                                  public void onError(Exception throwable) {
                                    LOGGER.error(
                                        "Could not fetch greyhounds, cause {}",
                                        throwable.getMessage());
                                  }
                                })));
                  }
                });
          });
    }
  }

  public void consumeHRHorses(Date date) {
    DatedAction consumeHRHorses = new ConsumeHRHorsesAction(date);
    ChainedAction consumeHRHorsesIfNeed = consumeHRHorses.ifWasNotPerformed();
    consumeHRHorsesIfNeed.call();
  }

  public void consumeHRCourses(Date date) {
    DatedAction consumeHRCourses = new ConsumeHRCoursesAction(date);
    ChainedAction consumeHRCoursesIfNeed = consumeHRCourses.ifWasNotPerformed();
    consumeHRCoursesIfNeed.call();
  }

  private class ConsumeHRCoursesAction extends DatedAction {

    public ConsumeHRCoursesAction(Date targetDate) {
      super(targetDate, calendar, "horse racing fetch courses");
      setAsyncMode(true);
      setAction(
          dataCallbackWrapper -> {
            String lockName = generateLockName(HR_COURSES_PREFIX, targetDate);
            lockService.tryLockWithWrapper(
                lockName,
                HR_COURSES_LOCK_TIME,
                unlockWrapper -> {
                  if (!horseRacingCourseService.isNewHRCoursesForDateExists(targetDate)) {
                    timeFormService.getHRCourses(
                        dataCallbackWrapper.wrap(
                            unlockWrapper.wrap(
                                new DataCallback<List<HRCourse>>() {
                                  @Override
                                  public void onResponse(List<HRCourse> mCourses) {
                                    Map<Integer, HRCourse> retrievedCourseMap =
                                        mCourses.stream()
                                            .collect(
                                                Collectors.toMap(
                                                    course -> course.getCourseId(),
                                                    course -> course,
                                                    (key1, key2) -> {
                                                      LOGGER.info(
                                                          "Duplicates for course key {} ", key1);
                                                      return key1;
                                                    }));
                                    horseRacingCourseService.updateCourses(
                                        retrievedCourseMap, targetDate);
                                  }

                                  @Override
                                  public void onError(Exception e) {
                                    LOGGER.error(
                                        "Could not fetch courses, cause {}", e.getMessage());
                                  }
                                })));
                  }
                });
          });
    }
  }

  public void consumeHRCountries(Date date) {
    String lockName = generateLockName(HR_COUNTRIES_PREFIX, date);
    lockService.tryLockWithWrapper(
        lockName,
        HR_COUNTRIES_LOCK_TIME,
        unlockWrapper -> {
          if (!horseRacingCountriesService.isNewCountriesForDateExists(date)) {
            timeFormService.getHRCountries(
                unlockWrapper.wrap(
                    new DataCallback<List<HRCountry>>() {
                      @Override
                      public void onResponse(List<HRCountry> mCountries) {
                        Map<String, HRCountry> retrievedCountryMap =
                            mCountries.stream()
                                .collect(
                                    Collectors.toMap(
                                        country -> country.getCountryCode(),
                                        Tools.identity(),
                                        (country1, country2) -> country1));
                        horseRacingCountriesService.updateCountries(retrievedCountryMap, date);
                        schedulerService.unscheduleHRCountriesRetry();
                      }

                      @Override
                      public void onError(Exception e) {
                        schedulerService.scheduleHRCountriesRetry();
                        LOGGER.error("Could not fetch countries, cause {}", e.getMessage());
                      }
                    }));
          }
        });
  }

  private List<HRMeeting> filterNewMeeting(List<HRMeeting> meetings, Date date) {
    Set<HRMeeting.HRMeetingKey> keys = storageService.getMeetingsMapForDate(date).keySet();
    return meetings.stream() //
        .filter(m -> !keys.contains(m.getKey())) //
        .collect(Collectors.toList());
  }

  private String generateLockName(String prefix, Date date) {
    SimpleDateFormat sdf =
        com.egalacoral.spark.timeform.api.tools.Tools.simpleDateFormat("yyyy-MM-dd");
    return prefix + ":" + sdf.format(date);
  }

  public void meetingsAdHocRequest(Date date) {
    LOGGER.info("meetingsAdHocRequest for {}", date);
    DatedAction action = new FetchMeetingForDateAction(date);
    action.setAfter(new MapMeetingWithOpenBet(date));
    action.forceSuccessRemove();
    action.call();
  }

  public void consumeCourseMaps(Date date) {
    String lockName = generateLockName(HR_COURSE_MAPS_PREFIX, date);
    try {
      lockService.doInLockOrSkip(
          lockName,
          HR_COURSE_MAPS_LOCK_TIME,
          () -> {
            Collection<HRMeeting> meetings = storageService.getMeetingsMapForDate(date).values();
            int racesCount = meetings.stream().mapToInt(m -> m.getRaces().size()).sum();
            CountDownLatch countDownLatch = new CountDownLatch(racesCount);

            meetings.stream()
                .forEach(
                    meeting -> {
                      meeting.getRaces().stream() //
                          .forEach(
                              race -> {
                                timeFormService.getHRCourseMapByRace(
                                    race,
                                    new DataCallback<HRCourseMap>() {
                                      @Override
                                      public void onResponse(HRCourseMap data) {
                                        countDownLatch.countDown();
                                        if (race.getCourseMapId() == null
                                            || horseRacingCourseMapService.getHRCourseMap(
                                                    race.getCourseMapId())
                                                == null) {
                                          horseRacingCourseMapService.save(data);
                                          storageService.updateRaceCourseMapId(
                                              meeting, race, data.getUUID());
                                        } else {
                                          horseRacingCourseMapService.update(
                                              race.getCourseMapId(), data);
                                        }
                                      }

                                      @Override
                                      public void onError(Exception throwable) {
                                        countDownLatch.countDown();
                                        LOGGER.error("Error consuming course map", throwable);
                                      }
                                    });
                              });
                    });

            try {
              countDownLatch.await(HR_COURSE_MAPS_LOCK_TIME / 2, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
              LOGGER.error("Consuming course maps await implemented", e);
            }
          });
    } catch (InterruptedException e) {
      LOGGER.error("Failed consuming course maps", e);
    }
  }
}
