package com.egalacoral.spark.timeform.service.greyhound.mapper;

import static java.util.Collections.singletonList;
import static org.mockito.Matchers.any;
import static org.mockito.Matchers.anyListOf;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.egalacoral.spark.timeform.model.greyhound.Entry;
import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import com.egalacoral.spark.timeform.model.greyhound.Race;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

/** Created by llegkyy on 12.08.16. */
public class MeetingSelectionMapperTest {

  private SiteServerAPI siteServerAPI;
  private Outcome outcome1;
  private Outcome outcome2;
  private Market market;
  private Event event;

  @Before
  public void init() {
    siteServerAPI = Mockito.mock(SiteServerAPI.class);
    outcome1 = Mockito.mock(Outcome.class);
    outcome2 = Mockito.mock(Outcome.class);
    market = Mockito.mock(Market.class);
    event = Mockito.mock(Event.class);
  }

  /**
   * Test for mapEntriesData(Entry entry, Outcome outcome)
   *
   * @throws Exception
   */
  @Test
  public void mapEntriesData() throws Exception {
    Entry entry = new Entry();
    entry.setGreyHoundFullName("Gold Winner Test");
    Outcome outcome = new Outcome();
    Field f = Outcome.class.getDeclaredField("name");
    f.setAccessible(true);
    f.set(outcome, "Gold Winner Test");
    Field fieldId = Outcome.class.getDeclaredField("id");
    fieldId.setAccessible(true);
    fieldId.set(outcome, "47");
    MeetingSelectionMapper mapper = new MeetingSelectionMapper(Mockito.mock(SiteServerAPI.class));
    mapper.mapEntriesData(entry, outcome);
    Assert.assertEquals(
        "Object name is not parset right",
        new Integer(47),
        entry.getObSelectionIds().iterator().next());
  }

  @Test
  public void mapEntriesDataMoreData() throws Exception {
    Entry entry = new Entry();
    entry.setGreyHoundFullName("Mays Fiddlefadle");
    Outcome outcome = new Outcome();
    Field f = Outcome.class.getDeclaredField("name");
    f.setAccessible(true);
    f.set(outcome, "Mays Fiddlefadle N/R");
    Field fieldId = Outcome.class.getDeclaredField("id");
    fieldId.setAccessible(true);
    fieldId.set(outcome, "47");
    MeetingSelectionMapper mapper = new MeetingSelectionMapper(Mockito.mock(SiteServerAPI.class));
    mapper.mapEntriesData(entry, outcome);
    Assert.assertEquals(
        "Object name is not parset right",
        new Integer(47),
        entry.getObSelectionIds().iterator().next());
  }

  @Test
  public void mapEntriesDataSpaces() throws Exception {
    Entry entry = new Entry();
    entry.setGreyHoundFullName("Westberry Memoir ");
    Outcome outcome = new Outcome();
    Field f = Outcome.class.getDeclaredField("name");
    f.setAccessible(true);
    f.set(outcome, "Westberry Memoir");
    Field fieldId = Outcome.class.getDeclaredField("id");
    fieldId.setAccessible(true);
    fieldId.set(outcome, "47");
    MeetingSelectionMapper mapper = new MeetingSelectionMapper(Mockito.mock(SiteServerAPI.class));
    mapper.mapEntriesData(entry, outcome);
    Assert.assertEquals(
        "Object name is not parset right",
        new Integer(47),
        entry.getObSelectionIds().iterator().next());
  }

  @Test
  public void mapEntriesDataSpacesReverse() throws Exception {
    Entry entry = new Entry();
    entry.setGreyHoundFullName("Westberry Memoir");
    Outcome outcome = new Outcome();
    Field f = Outcome.class.getDeclaredField("name");
    f.setAccessible(true);
    f.set(outcome, "Westberry Memoir ");
    Field fieldId = Outcome.class.getDeclaredField("id");
    fieldId.setAccessible(true);
    fieldId.set(outcome, "47");
    MeetingSelectionMapper mapper = new MeetingSelectionMapper(Mockito.mock(SiteServerAPI.class));
    mapper.mapEntriesData(entry, outcome);
    Assert.assertEquals(
        "Object name is not parset right",
        new Integer(47),
        entry.getObSelectionIds().iterator().next());
  }

  @Test
  public void mapEntriesDataSymbol_() throws Exception {
    Entry entry = new Entry();
    entry.setGreyHoundFullName("Westberry_Memoir");
    Outcome outcome = new Outcome();
    Field f = Outcome.class.getDeclaredField("name");
    f.setAccessible(true);
    f.set(outcome, "Westberry Memoir");
    Field fieldId = Outcome.class.getDeclaredField("id");
    fieldId.setAccessible(true);
    fieldId.set(outcome, "47");
    MeetingSelectionMapper mapper = new MeetingSelectionMapper(Mockito.mock(SiteServerAPI.class));
    mapper.mapEntriesData(entry, outcome);
    Assert.assertEquals(
        "Object name is not parset right",
        new Integer(47),
        entry.getObSelectionIds().iterator().next());
  }

  @Test
  public void mapEntriesDataSymbol2() throws Exception {
    Entry entry = new Entry();
    entry.setGreyHoundFullName("Westberry Memoir");
    Outcome outcome = new Outcome();
    Field f = Outcome.class.getDeclaredField("name");
    f.setAccessible(true);
    f.set(outcome, "Westberry-Memoir");
    Field fieldId = Outcome.class.getDeclaredField("id");
    fieldId.setAccessible(true);
    fieldId.set(outcome, "47");
    MeetingSelectionMapper mapper = new MeetingSelectionMapper(Mockito.mock(SiteServerAPI.class));
    mapper.mapEntriesData(entry, outcome);
    Assert.assertEquals(
        "Object name is not parset right",
        new Integer(47),
        entry.getObSelectionIds().iterator().next());
  }

  @Test
  public void mapEntriesDataSomeSymbolsInName() throws Exception {
    Entry entry = new Entry();
    entry.setGreyHoundFullName("Lanrigg Sheena");
    Outcome outcome = new Outcome();
    Field f = Outcome.class.getDeclaredField("name");
    f.setAccessible(true);
    f.set(outcome, "Lanrigg Sheena (RES)");
    Field fieldId = Outcome.class.getDeclaredField("id");
    fieldId.setAccessible(true);
    fieldId.set(outcome, "47");
    MeetingSelectionMapper mapper = new MeetingSelectionMapper(Mockito.mock(SiteServerAPI.class));
    mapper.mapEntriesData(entry, outcome);
    Assert.assertEquals(
        "Object name is not parset right",
        new Integer(47),
        entry.getObSelectionIds().iterator().next());
  }

  @Test
  public void mapEntriesDataSomeSymbolsInName2() throws Exception {
    Entry entry = new Entry();
    entry.setGreyHoundFullName("Lanrigg Sheena (RES)");
    Outcome outcome = new Outcome();
    Field f = Outcome.class.getDeclaredField("name");
    f.setAccessible(true);
    f.set(outcome, "Lanrigg Sheena ");
    Field fieldId = Outcome.class.getDeclaredField("id");
    fieldId.setAccessible(true);
    fieldId.set(outcome, "47");
    MeetingSelectionMapper mapper = new MeetingSelectionMapper(Mockito.mock(SiteServerAPI.class));
    mapper.mapEntriesData(entry, outcome);
    Assert.assertEquals(
        "Object name is not parset right",
        new Integer(47),
        entry.getObSelectionIds().iterator().next());
  }

  @Test
  public void testMapOpenBetEventTypeIsNull() {
    Meeting meeting = createMeeting();
    meeting.setOpenBetIds(null);

    MeetingSelectionMapper mapper = new MeetingSelectionMapper(siteServerAPI);

    mapper.map(meeting);
    Assert.assertEquals(
        0,
        meeting
            .getRaces()
            .iterator()
            .next()
            .getEntries()
            .iterator()
            .next()
            .getObSelectionIds()
            .size());
  }

  @Test(expected = RuntimeException.class)
  public void testMapEventsNotPresent() {
    Mockito.when(
            siteServerAPI.getEventToOutcomeForType(
                Mockito.anyList(), Mockito.any(SimpleFilter.class)))
        .thenReturn(Optional.empty());
    Meeting meeting = createMeeting();

    MeetingSelectionMapper mapper = new MeetingSelectionMapper(siteServerAPI);

    mapper.map(meeting);
    Assert.assertEquals(
        0,
        meeting
            .getRaces()
            .iterator()
            .next()
            .getEntries()
            .iterator()
            .next()
            .getObSelectionIds()
            .size());
  }

  @Test
  public void testMapEventMarketIsNull() {
    Mockito.when(
            siteServerAPI.getEventToOutcomeForType(
                Mockito.anyList(), Mockito.any(SimpleFilter.class)))
        .thenReturn(Optional.of(new ArrayList<>(Arrays.asList(event))));
    Mockito.when(event.getId()).thenReturn("1").thenReturn("2").thenReturn("3");
    Mockito.when(event.getMarkets()).thenReturn(null);
    Meeting meeting = createMeeting();

    MeetingSelectionMapper mapper = new MeetingSelectionMapper(siteServerAPI);

    mapper.map(meeting);
    Assert.assertEquals(
        0,
        meeting
            .getRaces()
            .iterator()
            .next()
            .getEntries()
            .iterator()
            .next()
            .getObSelectionIds()
            .size());
  }

  @Test
  public void testMapEventMarketOutcomeIsNull() {
    Mockito.when(
            siteServerAPI.getEventToOutcomeForType(
                Mockito.anyList(), Mockito.any(SimpleFilter.class)))
        .thenReturn(Optional.of(new ArrayList<>(Arrays.asList(event))));
    Mockito.when(event.getId()).thenReturn("1").thenReturn("2").thenReturn("3");
    Mockito.when(event.getMarkets()).thenReturn(Arrays.asList(market));
    Mockito.when(market.getOutcomes()).thenReturn(null);

    Meeting meeting = createMeeting();
    MeetingSelectionMapper mapper = new MeetingSelectionMapper(siteServerAPI);

    mapper.map(meeting);
    Assert.assertEquals(
        0,
        meeting
            .getRaces()
            .iterator()
            .next()
            .getEntries()
            .iterator()
            .next()
            .getObSelectionIds()
            .size());
  }

  @Test
  public void testMapEventMarketOutcomeIsEmpty() {
    Mockito.when(
            siteServerAPI.getEventToOutcomeForType(
                anyListOf(String.class), any(SimpleFilter.class)))
        .thenReturn(Optional.of(new ArrayList<>(singletonList(event))));
    Mockito.when(event.getId()).thenReturn("1").thenReturn("2").thenReturn("3");
    Mockito.when(event.getMarkets()).thenReturn(singletonList(market));
    Mockito.when(market.getOutcomes()).thenReturn(new ArrayList<Outcome>());

    Meeting meeting = createMeeting();
    MeetingSelectionMapper mapper = new MeetingSelectionMapper(siteServerAPI);

    mapper.map(meeting);
    Assert.assertEquals(
        0,
        meeting
            .getRaces()
            .iterator()
            .next()
            .getEntries()
            .iterator()
            .next()
            .getObSelectionIds()
            .size());
  }

  @Test
  public void testMapSuccess() {
    Mockito.when(
            siteServerAPI.getEventToOutcomeForType(
                Mockito.anyList(), Mockito.any(SimpleFilter.class)))
        .thenReturn(Optional.of(new ArrayList<>(Arrays.asList(event))));
    Mockito.when(event.getId()).thenReturn("1").thenReturn("2").thenReturn("3");
    Mockito.when(event.getMarkets()).thenReturn(Arrays.asList(market));
    Mockito.when(market.getOutcomes()).thenReturn(Arrays.asList(outcome1, outcome2));
    Mockito.when(outcome1.getName()).thenReturn("test greyhound");
    Mockito.when(outcome1.getId()).thenReturn("777");
    Mockito.when(outcome2.getName()).thenReturn("test greyhound");
    Mockito.when(outcome2.getId()).thenReturn("888");

    Meeting meeting = createMeeting();

    MeetingSelectionMapper mapper = new MeetingSelectionMapper(siteServerAPI);

    mapper.map(meeting);
    Assert.assertEquals(
        2,
        meeting
            .getRaces()
            .iterator()
            .next()
            .getRaceEntries()
            .iterator()
            .next()
            .getObSelectionIds()
            .size());
    Assert.assertTrue(
        meeting
            .getRaces()
            .iterator()
            .next()
            .getRaceEntries()
            .iterator()
            .next()
            .getObSelectionIds()
            .containsAll(new HashSet<>(777, 888)));
  }

  private Meeting createMeeting() {
    Entry entry = new Entry();
    entry.setEntryId(1);
    entry.setGreyHoundFullName("test greyhound");
    Race race = new Race();
    race.setRaceId(1);
    race.setEntries(new HashSet<>(Arrays.asList(entry)));
    race.setOpenBetIds(new HashSet<>(Arrays.asList(1, 2, 3)));

    Meeting meeting = new Meeting();
    meeting.setName("test meeting");
    meeting.setOpenBetIds(new HashSet<>(Arrays.asList(1, 2, 3)));
    meeting.setRaces(new HashSet<>(Arrays.asList(race)));
    return meeting;
  }
}
