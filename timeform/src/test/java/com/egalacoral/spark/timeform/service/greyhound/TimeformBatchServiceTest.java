package com.egalacoral.spark.timeform.service.greyhound;

import com.egalacoral.spark.timeform.api.DataCallback;
import com.egalacoral.spark.timeform.api.TimeFormService;
import com.egalacoral.spark.timeform.repository.GreyhoundEntityRepository;
import com.egalacoral.spark.timeform.service.ActionCalendarStorageService;
import com.egalacoral.spark.timeform.service.LockService;
import com.egalacoral.spark.timeform.service.MissingDataChecker;
import com.egalacoral.spark.timeform.storage.Storage;
import java.util.ArrayList;
import java.util.Date;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;
import org.redisson.api.RLock;

@RunWith(MockitoJUnitRunner.class)
public class TimeformBatchServiceTest {

  @Mock TimeformMeetingService timeformMeetingService;

  @Mock TimeformGreyhoundService timeformGreyhoundService;

  @Mock TimeFormService timeFormService;

  @Mock MeetingFilterService meetingFilterService;

  @Mock MissingDataChecker missingDataChecker;

  @Mock Storage storage;

  @Mock ActionCalendarStorageService calendarStorageService;

  @Mock GreyhoundEntityRepository greyhoundPositionRepository;

  @Mock RLock lock;

  @Mock GreyhoundUtils greyhoundUtils;

  LockService lockService;

  TimeformBatchService service;

  @Before
  public void setUp() throws InterruptedException {
    service =
        new TimeformBatchService(
            timeformMeetingService,
            timeFormService,
            meetingFilterService,
            missingDataChecker,
            greyhoundPositionRepository,
            storage,
            calendarStorageService,
            greyhoundUtils);
    Mockito.when(storage.getLock(Mockito.anyString())).thenReturn(lock);
    Mockito.when(lock.tryLock(Mockito.anyLong(), Mockito.anyLong(), Mockito.any()))
        .thenReturn(true);
    LockService lockServiceReal = new LockService(storage);
    lockService = Mockito.spy(lockServiceReal);
    service.setLockService(lockService);
    service.setTimeformGreyhoundService(timeformGreyhoundService);
  }

  @Test
  public void testConsumeGreyhoundsInLock() {
    Mockito.doAnswer(
            invocation -> {
              ((DataCallback) invocation.getArguments()[1]).onResponse(new ArrayList());
              return null;
            })
        .when(timeFormService)
        .getEntriesGreyhoundByMeetingDate(Mockito.any(), Mockito.any());

    try {
      service.consumeGreyhounds(new Date());
    } catch (Exception e) {
      e.printStackTrace();
    }
    Mockito.verify(lockService, Mockito.timeout(1000))
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.timeout(1000)).forceUnlock();
  }

  @Test
  public void testConsumeGreyhoundsInLockErrorCallback() {
    Mockito.doAnswer(
            invocation -> {
              ((DataCallback) invocation.getArguments()[1]).onError(new RuntimeException());
              return null;
            })
        .when(timeFormService)
        .getEntriesGreyhoundByMeetingDate(Mockito.any(), Mockito.any());

    try {
      service.consumeGreyhounds(new Date());
    } catch (Exception e) {
      e.printStackTrace();
    }
    Mockito.verify(lockService, Mockito.timeout(1000))
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.timeout(1000)).forceUnlock();
  }

  @Test
  public void testConsumeGreyhoundsInLockNullResult() {
    Mockito.doAnswer(
            invocation -> {
              ((DataCallback) invocation.getArguments()[1]).onResponse(null);
              return null;
            })
        .when(timeFormService)
        .getEntriesGreyhoundByMeetingDate(Mockito.any(), Mockito.any());

    try {
      service.consumeGreyhounds(new Date());
    } catch (Exception e) {
      e.printStackTrace();
    }
    Mockito.verify(lockService, Mockito.timeout(1000))
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.timeout(1000)).forceUnlock();
  }

  @Test
  public void testConsumeGreyhoundsInLockCallFailed() {
    Mockito.doThrow(new RuntimeException())
        .when(timeFormService)
        .getEntriesGreyhoundByMeetingDate(Mockito.any(), Mockito.any());

    try {
      service.consumeGreyhounds(new Date());
    } catch (Exception e) {
      e.printStackTrace();
    }
    Mockito.verify(lockService, Mockito.timeout(1000))
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.timeout(1000)).forceUnlock();
  }
}
