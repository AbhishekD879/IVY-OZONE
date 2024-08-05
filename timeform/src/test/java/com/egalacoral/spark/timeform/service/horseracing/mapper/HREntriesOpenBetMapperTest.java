package com.egalacoral.spark.timeform.service.horseracing.mapper;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.egalacoral.spark.timeform.model.horseracing.HREntry;
import com.egalacoral.spark.timeform.model.horseracing.HRMeeting;
import com.egalacoral.spark.timeform.model.horseracing.HRRace;
import java.util.*;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

public class HREntriesOpenBetMapperTest {

  private SiteServerAPI siteServerAPI;
  private Outcome outcome1;
  private Outcome outcome2;
  private Market market;
  private Event event;

  private HREntriesOpenBetMapper entriesOpenBetMapper;

  @Before
  public void init() {
    siteServerAPI = Mockito.mock(SiteServerAPI.class);
    event = Mockito.mock(Event.class);
    entriesOpenBetMapper = new HREntriesOpenBetMapper(siteServerAPI);
    outcome1 = Mockito.mock(Outcome.class);
    outcome2 = Mockito.mock(Outcome.class);
    market = Mockito.mock(Market.class);
    event = Mockito.mock(Event.class);
  }

  @Test
  public void testMapEntriesSuccess() {
    Mockito.when(
            siteServerAPI.getEventToOutcomeForType(
                Mockito.anyList(), Mockito.any(SimpleFilter.class)))
        .thenReturn(Optional.of(new ArrayList<>(Arrays.asList(event))));
    Mockito.when(event.getId()).thenReturn("1").thenReturn("2").thenReturn("3");
    Mockito.when(event.getMarkets()).thenReturn(Arrays.asList(market));
    Mockito.when(market.getOutcomes()).thenReturn(Arrays.asList(outcome1, outcome2));
    Mockito.when(outcome1.getName()).thenReturn("test horse");
    Mockito.when(outcome1.getId()).thenReturn("777");
    Mockito.when(outcome2.getName()).thenReturn("test horse2");
    Mockito.when(outcome2.getId()).thenReturn("888");

    HRMeeting meeting = createMeeting();
    Map<HRMeeting, List<HRRace>> map = new HashMap<>();
    map.put(meeting, (List<HRRace>) meeting.getRaces());

    HREntriesOpenBetMapper mapper = new HREntriesOpenBetMapper(siteServerAPI);
    mapper.mapEntries(map);

    Assert.assertEquals(
        1,
        meeting.getRaces().iterator().next().getEntries().iterator().next().getOpenBetIds().size());
    Assert.assertTrue(
        meeting
            .getRaces()
            .iterator()
            .next()
            .getEntries()
            .iterator()
            .next()
            .getOpenBetIds()
            .containsAll(new HashSet<>(777)));
  }

  @Test(expected = RuntimeException.class)
  public void testMapEntriesEventsNotPresent() {
    Mockito.when(
            siteServerAPI.getEventToOutcomeForType(
                Mockito.anyList(), Mockito.any(SimpleFilter.class)))
        .thenReturn(Optional.empty());

    HRMeeting meeting = createMeeting();
    Map<HRMeeting, List<HRRace>> map = new HashMap<>();
    map.put(meeting, (List<HRRace>) meeting.getRaces());

    HREntriesOpenBetMapper mapper = new HREntriesOpenBetMapper(siteServerAPI);
    mapper.mapEntries(map);

    Assert.assertTrue(
        meeting
            .getRaces()
            .iterator()
            .next()
            .getEntries()
            .iterator()
            .next()
            .getOpenBetIds()
            .isEmpty());
  }

  @Test
  public void testMapEntriesEventsEventMarketsIsNull() {
    Mockito.when(
            siteServerAPI.getEventToOutcomeForType(
                Mockito.anyList(), Mockito.any(SimpleFilter.class)))
        .thenReturn(Optional.of(new ArrayList<>(Arrays.asList(event))));
    Mockito.when(event.getId()).thenReturn("1").thenReturn("2").thenReturn("3");
    Mockito.when(event.getMarkets()).thenReturn(Arrays.asList(market));
    Mockito.when(market.getOutcomes()).thenReturn(null);

    HRMeeting meeting = createMeeting();
    Map<HRMeeting, List<HRRace>> map = new HashMap<>();
    map.put(meeting, (List<HRRace>) meeting.getRaces());

    HREntriesOpenBetMapper mapper = new HREntriesOpenBetMapper(siteServerAPI);
    mapper.mapEntries(map);

    Assert.assertTrue(
        meeting
            .getRaces()
            .iterator()
            .next()
            .getEntries()
            .iterator()
            .next()
            .getOpenBetIds()
            .isEmpty());
  }

  @Test
  public void testMapEntriesEventsEventOutcomesIsNull() {
    Mockito.when(
            siteServerAPI.getEventToOutcomeForType(
                Mockito.anyList(), Mockito.any(SimpleFilter.class)))
        .thenReturn(Optional.of(new ArrayList<>(Arrays.asList(event))));
    Mockito.when(event.getId()).thenReturn("1").thenReturn("2").thenReturn("3");
    Mockito.when(event.getMarkets()).thenReturn(null);

    HRMeeting meeting = createMeeting();
    Map<HRMeeting, List<HRRace>> map = new HashMap<>();
    map.put(meeting, (List<HRRace>) meeting.getRaces());

    HREntriesOpenBetMapper mapper = new HREntriesOpenBetMapper(siteServerAPI);
    mapper.mapEntries(map);

    Assert.assertTrue(
        meeting
            .getRaces()
            .iterator()
            .next()
            .getEntries()
            .iterator()
            .next()
            .getOpenBetIds()
            .isEmpty());
  }

  private HRMeeting createMeeting() {
    HREntry entry = new HREntry();
    entry.setCourseId(1);
    entry.setRaceNumber(1);
    entry.setHorseCode("1");

    entry.setHorseName("test horse (UKR)");
    HRRace race = new HRRace();
    race.setRaceNumber(1);
    race.setCourseId(1);

    race.setEntries(new HashSet<>(Arrays.asList(entry)));
    race.setOpenBetIds(new HashSet<>(Arrays.asList(1, 2, 3)));

    HRMeeting meeting = new HRMeeting();
    meeting.setMeetingDate("2016-09-15T00:00:00");
    meeting.setCourseId(1);
    meeting.setOpenBetIds(new HashSet<>(Arrays.asList(1, 2, 3)));
    meeting.setRaces(Arrays.asList(race));
    return meeting;
  }
}
