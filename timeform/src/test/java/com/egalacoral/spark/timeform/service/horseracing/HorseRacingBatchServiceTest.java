package com.egalacoral.spark.timeform.service.horseracing;

import com.egalacoral.spark.timeform.api.DataCallback;
import com.egalacoral.spark.timeform.api.TimeFormService;
import com.egalacoral.spark.timeform.model.horseracing.HRCourseMap;
import com.egalacoral.spark.timeform.model.horseracing.HREntry;
import com.egalacoral.spark.timeform.model.horseracing.HRMeeting;
import com.egalacoral.spark.timeform.model.horseracing.HRRace;
import com.egalacoral.spark.timeform.service.ActionCalendarStorageService;
import com.egalacoral.spark.timeform.service.LockService;
import com.egalacoral.spark.timeform.service.MissingDataChecker;
import com.egalacoral.spark.timeform.service.SchedulerService;
import com.egalacoral.spark.timeform.service.horseracing.mapper.HREntriesOpenBetMapper;
import com.egalacoral.spark.timeform.service.horseracing.mapper.HRRacesOpenBetMapper;
import com.egalacoral.spark.timeform.service.horseracing.mapper.HorseRacingMeetingTypeMapper;
import com.egalacoral.spark.timeform.storage.Storage;
import java.util.*;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InOrder;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;
import org.redisson.api.RLock;

@RunWith(MockitoJUnitRunner.class)
public class HorseRacingBatchServiceTest {

  @Mock private TimeFormService timeFormService;

  @Mock private HorseRacingStorageService storageService;

  @Mock private HRRacesOpenBetMapper racesOpenBetMapper;

  @Mock private HREntriesOpenBetMapper openBetMapper;

  private LockService lockService;

  @Mock private RLock lock;

  @Mock Storage hazelcastInstance;

  @Mock private HorseRacingMeetingTypeMapper meetingTypeMapper;

  @Mock private HorseRacingPerformanceService horseRacingPerformanceService;

  @Mock private HorseRacingHorseService horseRacingHorseService;

  @Mock private HorseRacingCourseService horseRacingCourseService;

  @Mock private HorseRacingCountriesService horseRacingCountriesService;

  @Mock private MissingDataChecker missingDataChecker;

  private HorseRacingBatchService batchService;

  @Mock private ActionCalendarStorageService calendarStorageService;

  @Mock private HorseRacingCourseMapService horseRacingCourseMapService;

  @Mock private SchedulerService schedulerService;

  private List<HRMeeting> meetingsFromTimeform;

  private List<HRRace> racesFromTimeform;

  private Map<HRMeeting.HRMeetingKey, HRMeeting> storedMeetings;

  @Before
  public void setUp() throws InterruptedException {
    Mockito.when(hazelcastInstance.getLock(Mockito.anyString())).thenReturn(lock);
    Mockito.when(lock.tryLock(Mockito.anyLong(), Mockito.anyLong(), Mockito.any()))
        .thenReturn(true);

    lockService = Mockito.spy(new LockService(hazelcastInstance));

    batchService =
        new HorseRacingBatchService(
            timeFormService,
            storageService,
            horseRacingPerformanceService,
            horseRacingHorseService,
            horseRacingCourseService,
            horseRacingCountriesService,
            lockService,
            racesOpenBetMapper,
            meetingTypeMapper,
            openBetMapper,
            missingDataChecker,
            calendarStorageService,
            horseRacingCourseMapService,
            schedulerService);

    meetingsFromTimeform =
        Arrays.asList( //
            meeting(1, "D1", null), //
            meeting(2, "D2", null), //
            meeting(3, "D3", null), //
            meeting(4, "D4", null), //
            meeting(5, "D5", null) //
            );

    racesFromTimeform =
        Arrays.asList(
            race(1, 1, "D1", "HR1"), //
            race(1, 2, "D1", "HR2"), //
            race(2, 3, "D2", "HR3"), //
            race(2, 4, "D2", "HR4"), //
            race(3, 5, "D3", "HR5") //
            );

    Mockito.doAnswer(
            invoke -> {
              ((DataCallback) invoke.getArguments()[1]).onResponse(meetingsFromTimeform);
              return null;
            }) //
        .when(timeFormService)
        .getHRMeetingsForDate(Mockito.any(), Mockito.any());

    Mockito.doAnswer(
            invoke -> {
              ((DataCallback) invoke.getArguments()[1]).onResponse(racesFromTimeform);
              return null;
            }) //
        .when(timeFormService)
        .getHRRacesWithRacesByMeetingDate(Mockito.any(), Mockito.any());

    storedMeetings =
        Arrays.asList( //
                meeting(
                    1, "D1", Arrays.asList(race(1, 1, "D1", "HR1"), race(1, 2, "D1", "HR2"))), //
                meeting(5, "D5", null) //
                )
            .stream()
            .collect(Collectors.toMap(HRMeeting::getKey, Function.identity()));

    Mockito.when(storageService.getMeetingsMapForDate(Mockito.any())).thenReturn(storedMeetings);
  }

  private HRMeeting meeting(int courseId, String meetingDate, List<HRRace> races) {
    HRMeeting m = new HRMeeting();
    m.setMeetingDate(meetingDate);
    m.setCourseId(courseId);
    if (races != null) {
      m.setRaces(races);
    }
    return m;
  }

  private HRRace race(int courseId, int raceNumber, String meetingDate, String horseCode) {
    HREntry e = new HREntry();
    e.setCourseId(courseId);
    e.setRaceNumber(raceNumber);
    e.setMeetingDate(meetingDate);
    e.setHorseCode(horseCode);

    HRRace r = new HRRace();
    r.setCourseId(courseId);
    r.setRaceNumber(raceNumber);
    r.setMeetingDate(meetingDate);

    r.setEntries(Arrays.asList(e));
    return r;
  }

  @Test
  public void testFetchRacesWithEntriesForDateSuccess() {
    Mockito.when(storageService.isRacesWithEntriesExistForDate(Mockito.any())).thenReturn(false);
    Mockito.when(storageService.getMeetingsMapForDate(Mockito.any())).thenReturn(storedMeetings);
    Date date = new Date();
    batchService.fetchRacesWithEntriesForDate(date);

    ArgumentCaptor<Date> dateArgumentCaptor = ArgumentCaptor.forClass(Date.class);
    ArgumentCaptor<DataCallback> callbackArgumentCaptor =
        ArgumentCaptor.forClass(DataCallback.class);

    List<HRRace> filteredList =
        racesFromTimeform.stream()
            .filter(
                race ->
                    storedMeetings.containsKey(
                            new HRMeeting.HRMeetingKey(race.getMeetingDate(), race.getCourseId()))
                        == true)
            .collect(Collectors.toList());

    Mockito.verify(storageService).updateMeetingRacesWithEntries(filteredList, date);
    Mockito.verify(timeFormService)
        .getHRRacesWithRacesByMeetingDate(
            dateArgumentCaptor.capture(), callbackArgumentCaptor.capture());
    Assert.assertEquals(date, dateArgumentCaptor.getValue());
  }

  @Test
  public void testFetchRacesWithEntriesForDateIsLocked() throws InterruptedException {
    Date date = new Date();
    Mockito.when(lock.tryLock(Mockito.anyLong(), Mockito.anyLong(), Mockito.any()))
        .thenReturn(false);

    batchService.fetchRacesWithEntriesForDate(date);
    Mockito.verify(storageService, Mockito.never())
        .updateMeetingRacesWithEntries(racesFromTimeform, date);
    Mockito.verify(timeFormService, Mockito.never())
        .getHRRacesWithRacesByMeetingDate(Mockito.any(), Mockito.any());
  }

  @Test
  public void testFetchRacesWithEntriesForDateRacesAlreadyExist() {
    Date date = new Date();
    Mockito.when(storageService.isRacesWithEntriesExistForDate(Mockito.any())).thenReturn(true);

    batchService.fetchRacesWithEntriesForDate(date);

    Mockito.verify(storageService, Mockito.never())
        .updateMeetingRacesWithEntries(racesFromTimeform, date);
    Mockito.verify(timeFormService, Mockito.never())
        .getHRRacesWithRacesByMeetingDate(Mockito.any(), Mockito.any());
  }

  @Test
  public void testFetchRacesWithEntriesForDateMeetingIsNotExist() {
    Date date = new Date();
    Mockito.when(storageService.isRacesWithEntriesExistForDate(Mockito.any())).thenReturn(false);
    Mockito.when(storageService.getMeetingsMapForDate(Mockito.any())).thenReturn(null);

    batchService.fetchRacesWithEntriesForDate(date);

    Mockito.verify(storageService, Mockito.never())
        .updateMeetingRacesWithEntries(racesFromTimeform, date);
    Mockito.verify(timeFormService, Mockito.never())
        .getHRRacesWithRacesByMeetingDate(Mockito.any(), Mockito.any());
  }

  @Test
  public void testSuccessFetchAndFilterExists() {
    Date date = new Date();

    batchService.fetchMeetingsForDate(date);

    ArgumentCaptor<Date> dateArgumentCaptor = ArgumentCaptor.forClass(Date.class);
    ArgumentCaptor<DataCallback> callbackArgumentCaptor =
        ArgumentCaptor.forClass(DataCallback.class);
    Mockito.verify(storageService)
        .save(
            meetingsFromTimeform.stream()
                .filter(m -> !storedMeetings.containsKey(m.getKey()))
                .collect(Collectors.toList()));
    Mockito.verify(timeFormService)
        .getHRMeetingsForDate(dateArgumentCaptor.capture(), callbackArgumentCaptor.capture());
    Assert.assertEquals(date, dateArgumentCaptor.getValue());
  }

  @Test
  public void testNotFetchMeetingsIfLocked() throws InterruptedException {
    Date date = new Date();
    Mockito.when(lock.tryLock(Mockito.anyLong(), Mockito.anyLong(), Mockito.any()))
        .thenReturn(false);

    batchService.fetchMeetingsForDate(date);

    Mockito.verify(storageService, Mockito.never())
        .save(
            meetingsFromTimeform.stream()
                .filter(m -> !storedMeetings.containsKey(m.getKey()))
                .collect(Collectors.toList()));
    Mockito.verify(timeFormService, Mockito.never())
        .getHRMeetingsForDate(Mockito.any(), Mockito.any());
  }

  @Test
  public void testUnlock() {
    Date date = new Date();

    batchService.fetchMeetingsForDate(date);

    InOrder inOrder = Mockito.inOrder(lockService, lock);
    inOrder
        .verify(lockService)
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any(Consumer.class));
    inOrder.verify(lock).forceUnlock();

    batchService.fetchRacesWithEntriesForDate(date);

    inOrder = Mockito.inOrder(lockService, lock);
    inOrder
        .verify(lockService)
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any(Consumer.class));
    inOrder.verify(lock).forceUnlock();
  }

  @Test
  public void testUnlockWhenTimeFormErrorReturned() {
    Date date = new Date();
    Mockito.doAnswer(
            invoke -> {
              ((DataCallback) invoke.getArguments()[1]).onError(new RuntimeException());
              return null;
            })
        .when(timeFormService)
        .getHRMeetingsForDate(Mockito.any(), Mockito.any());

    batchService.fetchMeetingsForDate(date);

    InOrder inOrder = Mockito.inOrder(lockService, lock);
    inOrder
        .verify(lockService)
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any(Consumer.class));
    inOrder.verify(lock).forceUnlock();

    Mockito.doAnswer(
            invoke -> {
              ((DataCallback) invoke.getArguments()[1]).onError(new RuntimeException());
              return null;
            })
        .when(timeFormService)
        .getHRRacesWithRacesByMeetingDate(Mockito.any(), Mockito.any());

    batchService.fetchRacesWithEntriesForDate(date);

    inOrder = Mockito.inOrder(lockService, lock);
    inOrder
        .verify(lockService)
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any(Consumer.class));
    inOrder.verify(lock).forceUnlock();
  }

  @Test
  public void testUnlockWhenProcessingError() {
    Date date = new Date();
    Mockito.doThrow(new RuntimeException()).when(storageService).save(Mockito.any());

    try {
      batchService.fetchMeetingsForDate(date);
    } catch (Exception e) {
      // simulated exception
    }

    InOrder inOrder = Mockito.inOrder(lockService, lock);
    inOrder
        .verify(lockService)
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any(Consumer.class));
    inOrder.verify(lock, Mockito.atLeastOnce()).forceUnlock();
  }

  @Test
  public void testUnlockWhenTimeFormErrorThrown() {
    Date date = new Date();
    Mockito.doThrow(new RuntimeException())
        .when(timeFormService)
        .getHRMeetingsForDate(Mockito.any(), Mockito.any());

    try {
      batchService.fetchMeetingsForDate(date);
    } catch (Exception e) {
      // simulated exception
    }

    InOrder inOrder = Mockito.inOrder(lockService, lock);
    inOrder
        .verify(lockService)
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any(Consumer.class));
    inOrder.verify(lock).forceUnlock();
  }

  @Test
  public void testConsumingHorsesInLock() {
    Mockito.doAnswer(
            invocation -> {
              ((DataCallback) invocation.getArguments()[1]).onResponse(new ArrayList());
              return null;
            })
        .when(timeFormService)
        .getHREntriesHorsesByMeetingDate(Mockito.any(), Mockito.any());

    try {
      batchService.consumeHRHorses(new Date());
    } catch (Exception e) {
      e.printStackTrace();
    }
    Mockito.verify(lockService, Mockito.timeout(1000))
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.timeout(1000)).forceUnlock();
  }

  @Test
  public void testConsumeHorsesInLockErrorCallback() {
    Mockito.doAnswer(
            invocation -> {
              ((DataCallback) invocation.getArguments()[1]).onError(new RuntimeException());
              return null;
            })
        .when(timeFormService)
        .getHREntriesHorsesByMeetingDate(Mockito.any(), Mockito.any());

    try {
      batchService.consumeHRHorses(new Date());
    } catch (Exception e) {
      e.printStackTrace();
    }
    Mockito.verify(lockService, Mockito.timeout(1000))
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.timeout(1000)).forceUnlock();
  }

  @Test
  public void testConsumeHorsesInLockNullResult() {
    Mockito.doAnswer(
            invocation -> {
              ((DataCallback) invocation.getArguments()[1]).onResponse(null);
              return null;
            })
        .when(timeFormService)
        .getHREntriesHorsesByMeetingDate(Mockito.any(), Mockito.any());

    try {
      batchService.consumeHRHorses(new Date());
    } catch (Exception e) {
      e.printStackTrace();
    }
    Mockito.verify(lockService, Mockito.timeout(1000))
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.timeout(1000)).forceUnlock();
  }

  @Test
  public void testConsumeHorsesInLockCallFailed() {
    Mockito.doThrow(new RuntimeException())
        .when(timeFormService)
        .getHREntriesHorsesByMeetingDate(Mockito.any(), Mockito.any());

    try {
      batchService.consumeHRHorses(new Date());
    } catch (Exception e) {
      e.printStackTrace();
    }
    Mockito.verify(lockService, Mockito.timeout(1000))
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.timeout(1000)).forceUnlock();
  }

  @Test
  public void testConsumingCoursesInLock() {
    Mockito.doAnswer(
            invocation -> {
              ((DataCallback) invocation.getArguments()[1]).onResponse(new ArrayList());
              return null;
            })
        .when(timeFormService)
        .getHRCourses(Mockito.any());

    try {
      batchService.consumeHRCourses(new Date());
    } catch (Exception e) {
      e.printStackTrace();
    }
    Mockito.verify(lockService, Mockito.timeout(1000))
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.timeout(1000)).forceUnlock();
  }

  @Test
  public void testConsumeCoursesInLockErrorCallback() {
    Mockito.doAnswer(
            invocation -> {
              ((DataCallback) invocation.getArguments()[1]).onError(new RuntimeException());
              return null;
            })
        .when(timeFormService)
        .getHRCourses(Mockito.any());

    try {
      batchService.consumeHRCourses(new Date());
    } catch (Exception e) {
      e.printStackTrace();
    }
    Mockito.verify(lockService, Mockito.timeout(1000))
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.timeout(1000)).forceUnlock();
  }

  @Test
  public void testConsumeCoursesInLockNullResult() {
    Mockito.doAnswer(
            invocation -> {
              ((DataCallback) invocation.getArguments()[1]).onResponse(null);
              return null;
            })
        .when(timeFormService)
        .getHRCourses(Mockito.any());

    try {
      batchService.consumeHRCourses(new Date());
    } catch (Exception e) {
      e.printStackTrace();
    }
    Mockito.verify(lockService, Mockito.timeout(1000))
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.timeout(1000)).forceUnlock();
  }

  @Test
  public void testConsumeCoursesInLockCallFailed() {
    Mockito.doThrow(new RuntimeException()).when(timeFormService).getHRCourses(Mockito.any());

    try {
      batchService.consumeHRCourses(new Date());
    } catch (Exception e) {
      e.printStackTrace();
    }
    Mockito.verify(lockService, Mockito.timeout(1000))
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.timeout(1000)).forceUnlock();
  }

  @Test
  public void testConsumingCountriesInLock() {
    Mockito.doAnswer(
            invocation -> {
              ((DataCallback) invocation.getArguments()[1]).onResponse(new ArrayList());
              return null;
            })
        .when(timeFormService)
        .getHRCountries(Mockito.any());

    try {
      batchService.consumeHRCountries(new Date());
    } catch (Exception e) {
      e.printStackTrace();
    }
    Mockito.verify(lockService, Mockito.timeout(1000))
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.timeout(1000)).forceUnlock();
  }

  @Test
  public void testConsumeCountriesInLockErrorCallback() {
    Mockito.doAnswer(
            invocation -> {
              ((DataCallback) invocation.getArguments()[1]).onError(new RuntimeException());
              return null;
            })
        .when(timeFormService)
        .getHRCountries(Mockito.any());

    try {
      batchService.consumeHRCountries(new Date());
    } catch (Exception e) {
      e.printStackTrace();
    }
    Mockito.verify(lockService, Mockito.timeout(1000))
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.timeout(1000)).forceUnlock();
  }

  @Test
  public void testConsumeCountriesInLockNullResult() {
    Mockito.doAnswer(
            invocation -> {
              ((DataCallback) invocation.getArguments()[1]).onResponse(null);
              return null;
            })
        .when(timeFormService)
        .getHRCountries(Mockito.any());

    try {
      batchService.consumeHRCountries(new Date());
    } catch (Exception e) {
      e.printStackTrace();
    }
    Mockito.verify(lockService, Mockito.timeout(1000))
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.timeout(1000)).forceUnlock();
  }

  @Test
  public void testConsumeCountriesInLockCallFailed() {
    Mockito.doThrow(new RuntimeException()).when(timeFormService).getHRCountries(Mockito.any());

    try {
      batchService.consumeHRCountries(new Date());
    } catch (Exception e) {
      e.printStackTrace();
    }
    Mockito.verify(lockService, Mockito.timeout(1000))
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.timeout(1000)).forceUnlock();
  }

  @Test
  public void testConsumeCourseMapSaveAndUpdate() {
    HRRace r1 = race(1, 1, "D1", "HR1");
    r1.setCourseMapId("CMID1");
    HRRace r2 = race(1, 2, "D1", "HR2");

    HRMeeting meeting = meeting(1, "D1", Arrays.asList(r1, r2));

    HRCourseMap hrCourseMap = new HRCourseMap();
    hrCourseMap.setBytes(new byte[] {1, 2});

    Mockito.doAnswer(
            invoke -> {
              ((DataCallback) invoke.getArguments()[1]).onResponse(hrCourseMap);
              return null;
            }) //
        .when(timeFormService)
        .getHRCourseMapByRace(Mockito.any(), Mockito.any());

    Mockito.when(horseRacingCourseMapService.getHRCourseMap("CMID1")).thenReturn(hrCourseMap);

    storedMeetings =
        Arrays.asList(meeting).stream()
            .collect(Collectors.toMap(HRMeeting::getKey, Function.identity()));

    Mockito.when(storageService.getMeetingsMapForDate(Mockito.any())).thenReturn(storedMeetings);

    Date d = new Date();
    batchService.consumeCourseMaps(d);

    Mockito.verify(horseRacingCourseMapService, Mockito.timeout(500)).save(hrCourseMap);
    Mockito.verify(horseRacingCourseMapService, Mockito.timeout(500)).update("CMID1", hrCourseMap);
    Mockito.verify(storageService, Mockito.timeout(500))
        .updateRaceCourseMapId(meeting, r2, hrCourseMap.getUUID());
  }

  @Test
  public void testConsumeCourseMapUpdateLost() {
    HRRace r1 = race(1, 1, "D1", "HR1");
    r1.setCourseMapId("CMID1");

    HRMeeting meeting = meeting(1, "D1", Arrays.asList(r1));

    HRCourseMap hrCourseMap = new HRCourseMap();
    hrCourseMap.setBytes(new byte[] {1, 2});

    Mockito.doAnswer(
            invoke -> {
              ((DataCallback) invoke.getArguments()[1]).onResponse(hrCourseMap);
              return null;
            }) //
        .when(timeFormService)
        .getHRCourseMapByRace(Mockito.any(), Mockito.any());

    // course map not found for existing id
    Mockito.when(horseRacingCourseMapService.getHRCourseMap("CMID1")).thenReturn(null);

    storedMeetings =
        Arrays.asList(meeting).stream()
            .collect(Collectors.toMap(HRMeeting::getKey, Function.identity()));

    Mockito.when(storageService.getMeetingsMapForDate(Mockito.any())).thenReturn(storedMeetings);

    Date d = new Date();
    batchService.consumeCourseMaps(d);

    Mockito.verify(horseRacingCourseMapService, Mockito.timeout(500)).save(hrCourseMap);
    Mockito.verify(storageService, Mockito.timeout(500))
        .updateRaceCourseMapId(meeting, r1, hrCourseMap.getUUID());
  }
}
