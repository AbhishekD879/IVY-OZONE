package com.egalacoral.spark.timeform.service.horseracing;

import com.egalacoral.spark.timeform.model.horseracing.HRMeeting;
import com.egalacoral.spark.timeform.storage.Storage;
import java.util.*;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class HorseRacingStorageServiceTest {

  @Mock private Storage storage;

  @Mock private Map map;

  private HorseRacingStorageService storageService;

  @Before
  public void setUp() {
    System.setProperty("hazelcast.test.use.network", "true");
    Mockito.when(storage.getMap(Mockito.anyString())).thenReturn(map);

    storageService = new HorseRacingStorageService(storage);
  }

  private HRMeeting meeting(int courseId, String meetingDate, Integer... obIds) {
    HRMeeting m = new HRMeeting();
    m.setMeetingDate(meetingDate);
    m.setCourseId(courseId);
    if (obIds != null) {
      m.setOpenBetIds(new HashSet<>(Arrays.asList(obIds)));
    }
    return m;
  }

  @Test
  public void testClear() {
    storageService.clear();

    Mockito.verify(map).clear();
  }

  @Test
  public void testSave() {
    List<HRMeeting> meetings =
        Arrays.asList( //
            meeting(1, "A", null), //
            meeting(2, "B", null), //
            meeting(3, "C", null));

    storageService.save(meetings);

    for (HRMeeting m : meetings) {
      Mockito.verify(map).put(m.getKey(), m);
    }
  }

  @Test
  public void testGetMeetingsByOpenbetIds() {
    Collection<Object> meetings =
        Arrays.asList( //
            meeting(1, "2016-01-02T00:00:00", 12, 11), //
            meeting(2, "2016-01-02T23:59:59", 13, 14), //
            meeting(3, "2016-01-03T00:00:00", 15, 16), //
            meeting(4, "2016-01-01T23:59:59", 17, 18));

    Map<Object, Object> map = Mockito.mock(Map.class);
    Mockito.when(map.values()).thenReturn(meetings);
    Mockito.when(storage.getMap(Mockito.anyString())).thenReturn(map);

    List<HRMeeting> hrMeetings = storageService.getMeetingsByOpenbetIds(Arrays.asList(18, 12));
    Assert.assertTrue(hrMeetings.size() == 2);
    Assert.assertEquals(Integer.valueOf(1), hrMeetings.get(0).getCourseId());
    Assert.assertEquals(Integer.valueOf(4), hrMeetings.get(1).getCourseId());
  }
}
