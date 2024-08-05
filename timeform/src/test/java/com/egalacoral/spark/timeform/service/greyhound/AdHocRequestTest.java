package com.egalacoral.spark.timeform.service.greyhound;

import com.egalacoral.spark.timeform.api.DataCallback;
import com.egalacoral.spark.timeform.api.TimeFormService;
import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import com.egalacoral.spark.timeform.repository.GreyhoundEntityRepository;
import com.egalacoral.spark.timeform.service.ActionCalendarStorageService;
import com.egalacoral.spark.timeform.service.LockService;
import com.egalacoral.spark.timeform.service.MissingDataChecker;
import com.egalacoral.spark.timeform.storage.Storage;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.function.Consumer;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.invocation.InvocationOnMock;
import org.mockito.runners.MockitoJUnitRunner;
import org.mockito.stubbing.Answer;
import org.redisson.api.RLock;

@RunWith(MockitoJUnitRunner.class)
public class AdHocRequestTest {

  @Mock private TimeformMeetingService timeformMeetingService;

  @Mock private TimeFormService timeFormService;

  @Mock private MeetingFilterService meetingFilterService;

  @Mock private MissingDataChecker missingDataChecker;

  @Mock private MeetingMappingService meetingMappingService;

  @Mock GreyhoundEntityRepository greyhoundPositionRepository;

  @Mock private LockService lockService;

  @Mock private Storage storage;

  @Mock private RLock lock;

  @Mock ActionCalendarStorageService calendarStorageService;

  private TimeformBatchService timeformBatchService;
  @Mock private GreyhoundUtils greyhoundUtils;

  @Test
  public void test() {
    TimeformBatchService timeformBatchService =
        new TimeformBatchService(
            timeformMeetingService,
            timeFormService,
            meetingFilterService,
            missingDataChecker,
            greyhoundPositionRepository,
            storage,
            calendarStorageService,
            greyhoundUtils);
    timeformBatchService.setMappingService(meetingMappingService);
    timeformBatchService.setLockService(lockService);
    Mockito.when(meetingFilterService.accept(Mockito.anyString())).thenReturn(true);
    Mockito.doAnswer(
            invocation -> {
              ((Consumer) invocation.getArguments()[2]).accept(new LockService.UnlockWrapper(lock));
              return null;
            })
        .when(lockService)
        .tryLockWithWrapper(Mockito.anyString(), Mockito.anyLong(), Mockito.any(Consumer.class));

    Date date = new Date();

    Meeting m1 = new Meeting();
    m1.setMeetingId(1);
    Meeting m2 = new Meeting();
    m2.setMeetingId(2);
    Meeting m3 = new Meeting();
    m3.setMeetingId(3);
    List<Meeting> storedMetings = new ArrayList<>();
    storedMetings.add(m1);
    storedMetings.add(m2);

    List<Meeting> receivedMetings = new ArrayList<>();
    receivedMetings.add(m1);
    receivedMetings.add(m2);
    receivedMetings.add(m3);

    List<Meeting> newMetings = new ArrayList<>();
    newMetings.add(m3);

    Mockito.when(timeformMeetingService.getMeetingsByDate(date)).thenReturn(storedMetings);
    Mockito.doAnswer(
            new Answer<Void>() {
              @Override
              public Void answer(InvocationOnMock invocation) throws Throwable {
                ((DataCallback<List<Meeting>>) invocation.getArguments()[1])
                    .onResponse(receivedMetings);
                return null;
              }
            }) //
        .when(timeFormService)
        .getMeetingsForDate(Mockito.eq(date), Mockito.any());

    timeformBatchService.fetchMeetingsByAdHocRequest(date);

    Mockito.verify(timeformMeetingService).save(newMetings);
  }
}
