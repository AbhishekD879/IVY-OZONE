package com.egalacoral.spark.timeform.service.horseracing.mapper;

import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.timeform.model.horseracing.HRMeeting;
import com.egalacoral.spark.timeform.model.horseracing.HRRace;
import java.util.*;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

public class HRRacesOpenBetMapperTest {

  private SiteServerAPI siteServerAPI;
  private Event event;

  private HRRacesOpenBetMapper racesOpenBetMapper;

  @Before
  public void init() {
    siteServerAPI = Mockito.mock(SiteServerAPI.class);
    event = Mockito.mock(Event.class);
    racesOpenBetMapper = new HRRacesOpenBetMapper(siteServerAPI);
  }

  @Test
  public void testMapRaces() {
    Map<HRMeeting, List<HRRace>> map = create();
    Mockito.when(siteServerAPI.getEventForType(Mockito.anyList(), Mockito.any()))
        .thenReturn(Optional.of(new ArrayList<>(Arrays.asList(event))));
    Mockito.when(event.getStartTime()).thenReturn("2016-09-06T13:30:00Z");
    Mockito.when(event.getId()).thenReturn("777");
    racesOpenBetMapper.mapRaces(map);

    Assert.assertEquals(
        Integer.valueOf(777),
        map.values().iterator().next().get(0).getOpenBetIds().iterator().next());
    Assert.assertEquals(0, map.values().iterator().next().get(1).getOpenBetIds().size());
  }

  @Test(expected = RuntimeException.class)
  public void testMapRacesEventsNotPresent() {
    Map<HRMeeting, List<HRRace>> map = create();
    Mockito.when(siteServerAPI.getEventForType(Mockito.anyList(), Mockito.any()))
        .thenReturn(Optional.empty());

    racesOpenBetMapper.mapRaces(map);

    Assert.assertEquals(0, map.values().iterator().next().get(0).getOpenBetIds().size());
    Assert.assertEquals(0, map.values().iterator().next().get(1).getOpenBetIds().size());
  }

  @Test
  public void testMapRacesRaceStartDateInvalid() {
    Map<HRMeeting, List<HRRace>> map = create();
    map.values().iterator().next().get(0).setStartTimeGMTScheduled("1990-01-01T00:00:00.000");

    Mockito.when(siteServerAPI.getEventForType(Mockito.anyList(), Mockito.any()))
        .thenReturn(Optional.of(new ArrayList<>(Arrays.asList(event))));

    Mockito.when(event.getStartTime()).thenReturn("2016-09-06T14:30:00Z");
    Mockito.when(event.getId()).thenReturn("777");
    racesOpenBetMapper.mapRaces(map);

    Assert.assertEquals(
        Integer.valueOf(777),
        map.values().iterator().next().get(1).getOpenBetIds().iterator().next());
    Assert.assertEquals(0, map.values().iterator().next().get(0).getOpenBetIds().size());
  }

  private Map<HRMeeting, List<HRRace>> create() {
    HRRace hrRace1 = new HRRace();
    hrRace1.setCourseId(1);
    hrRace1.setMeetingDate("2016-09-06T00:00:00");
    hrRace1.setRaceNumber(1);
    hrRace1.setStartTimeGMTScheduled("2016-09-06T13:30:00");

    HRRace hrRace2 = new HRRace();
    hrRace2.setCourseId(1);
    hrRace2.setMeetingDate("2016-09-06T00:00:00");
    hrRace2.setRaceNumber(2);
    hrRace2.setStartTimeGMTScheduled("2016-09-06T14:30:00");

    HRMeeting meeting = new HRMeeting();
    meeting.setMeetingDate("2016-09-06T00:00:00");
    meeting.setCourseId(1);
    meeting.getOpenBetIds().add(1);
    meeting.getOpenBetIds().add(2);
    Map<HRMeeting, List<HRRace>> map = new HashMap<>();
    map.put(meeting, Arrays.asList(hrRace1, hrRace2));
    return map;
  }
}
