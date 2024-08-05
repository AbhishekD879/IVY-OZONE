package com.egalacoral.spark.timeform.service.greyhound;

import com.egalacoral.spark.timeform.model.greyhound.Entry;
import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import com.egalacoral.spark.timeform.model.greyhound.Race;
import com.egalacoral.spark.timeform.storage.Storage;
import java.util.*;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

public class TimeformMeetingServiceTest {

  private TimeformMeetingService timeformMeetingService;
  private TimeformRacesService timeformRacesService;
  private TimeformEntriesService timeformEntriesService;

  @Before
  public void init() {
    Storage instance = Mockito.mock(Storage.class);
    ArrayList<Object> list = new ArrayList<>();
    addMeeting(list, null);
    addMeeting(list, Collections.singleton(2));
    Map<Object, Object> map = Mockito.mock(Map.class);
    Mockito.when(map.values()).thenReturn(list);
    Mockito.when(instance.getMap("meeting")).thenReturn(map);
    timeformMeetingService = new TimeformMeetingService(instance);
    timeformRacesService = new TimeformRacesService(timeformMeetingService);
    timeformEntriesService =
        new TimeformEntriesService(timeformMeetingService, timeformRacesService);
  }

  protected void addMeeting(ArrayList<Object> list, Set<Integer> obIds) {
    Meeting meeting = new Meeting();
    meeting.setOpenBetIds(obIds);
    HashSet<Race> races = new HashSet<>();
    addRace(1, races, null);
    addRace(2, races, Collections.singleton(1));
    addRace(3, races, null);
    meeting.setRaces(races);
    list.add(meeting);
  }

  @Test
  public void testGetRaceByOpenbetId() {
    List<Race> optional = timeformRacesService.getRaceByOpenbetId(Arrays.asList(1));
    Assert.assertTrue(!optional.isEmpty());
  }

  @Test
  public void testGetRaceByNullOpenbetId() {
    List<Race> optional = timeformRacesService.getRaceByOpenbetId(null);
    Assert.assertTrue(optional.isEmpty());
  }

  @Test
  public void testGetMeetingByOpenbetId() {
    List<Meeting> optional = timeformMeetingService.getMeetingByOpenbetId(Arrays.asList(2));
    Assert.assertTrue(!optional.isEmpty());
  }

  @Test
  public void testGetEntryMeetingByOpenbetId() {
    List<Entry> optional = timeformEntriesService.getEntryByOpenbetId(Arrays.asList(11));
    Assert.assertTrue(!optional.isEmpty());
  }

  protected void addRace(int id, HashSet<Race> races, Set<Integer> obIds) {
    Race race = new Race();
    race.setRaceId(id);
    race.setOpenBetIds(obIds);
    races.add(race);

    Entry entry = new Entry();
    entry.setOpenBetIds(Collections.singleton(11));
    race.setEntries(Collections.singleton(entry));
  }
}
