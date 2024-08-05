package com.egalacoral.spark.timeform.service;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.siteserver.model.Type;
import com.egalacoral.spark.timeform.model.MissingTimeFormData;
import com.egalacoral.spark.timeform.model.greyhound.Entry;
import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import com.egalacoral.spark.timeform.model.greyhound.Race;
import com.egalacoral.spark.timeform.service.SiteServerDataWrappers.EntryForTest;
import com.egalacoral.spark.timeform.service.SiteServerDataWrappers.EventForTest;
import com.egalacoral.spark.timeform.service.SiteServerDataWrappers.MarketForTest;
import com.egalacoral.spark.timeform.service.SiteServerDataWrappers.OutcomeForTest;
import com.egalacoral.spark.timeform.service.SiteServerDataWrappers.TypeForTest;
import com.egalacoral.spark.timeform.service.greyhound.MeetingFilterService;
import com.egalacoral.spark.timeform.service.greyhound.TimeformMeetingService;
import java.util.*;
import java.util.function.Consumer;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class MissingDataCheckerTest {

  @Mock private SiteServerAPI siteServerAPI;

  @Mock private TimeformMeetingService timeformMeetingService;

  @Mock private MeetingFilterService meetingFilterService;

  @Mock private Consumer<MissingTimeFormData> listener;

  @Mock private LockService lockService;

  @Mock private MissingDataValidationCalendarService validationCalendarService;

  private MissingDataChecker missingDataChecker;

  @Before
  public void setUp() throws InterruptedException {
    Mockito.when(siteServerAPI.getClassToSubTypeForClass(Mockito.anyString(), Mockito.any()))
        .thenReturn(Optional.of(new ArrayList<>()));
    Mockito.when(siteServerAPI.getEventToOutcomeForType(Mockito.any(List.class), Mockito.any()))
        .thenReturn(Optional.of(new ArrayList<>()));

    Mockito.when(meetingFilterService.accept(Mockito.anyString())).thenReturn(true);
    Mockito.when(timeformMeetingService.getMeetingsByDate(Mockito.any()))
        .thenReturn(new ArrayList<Meeting>());

    missingDataChecker =
        new MissingDataChecker(
            validationCalendarService,
            lockService,
            siteServerAPI,
            timeformMeetingService,
            meetingFilterService,
            "");

    List<Consumer<MissingTimeFormData>> listeners = new ArrayList<>();
    listeners.add(listener);
    missingDataChecker.setListeners(listeners);

    Mockito.doAnswer(
            i -> {
              ((Runnable) i.getArguments()[2]).run();
              return null;
            })
        .when(lockService)
        .doInLockOrSkip(Mockito.anyString(), Mockito.anyLong(), Mockito.any());

    Mockito.when(validationCalendarService.isDateValidated(Mockito.any())).thenReturn(false);
  }

  @Test
  public void testEmptyTypeIsNotLost() {
    Type t = new TypeForTest(1, "A");

    Mockito.when(siteServerAPI.getClassToSubTypeForClass(Mockito.anyString(), Mockito.any())) //
        .thenReturn(prepareOptional(t));

    missingDataChecker.validate(new Date());
    Mockito.verify(listener, Mockito.never()).accept(Mockito.any());
  }

  @Test
  public void testNotEmptyTypeIsLost() {
    Type type1 = new TypeForTest(1, "A");

    Mockito.when(siteServerAPI.getClassToSubTypeForClass(Mockito.anyString(), Mockito.any())) //
        .thenReturn(prepareOptional(type1));
    Mockito.when(siteServerAPI.getEventToOutcomeForType(Mockito.any(List.class), Mockito.any())) //
        .thenReturn(prepareOptional(new EventForTest("11", "E1", type1.getId())));

    missingDataChecker.validate(new Date());
    ArgumentCaptor<MissingTimeFormData> captor = ArgumentCaptor.forClass(MissingTimeFormData.class);
    Mockito.verify(listener).accept(captor.capture());

    MissingTimeFormData missingData = captor.getValue();
    Assert.assertEquals(1, missingData.getLostTypes().size());
    Assert.assertEquals(1, missingData.getLostEvents().size());

    Assert.assertEquals("A", missingData.getLostTypes().get(0).getName());
    Assert.assertEquals("A", missingData.getLostEvents().get(0).getType().getName());
    Assert.assertEquals("E1", missingData.getLostEvents().get(0).getEvent().getName());
  }

  @Test
  public void testOneValidationPerDate() {
    Type type1 = new TypeForTest(1, "A");

    Mockito.when(siteServerAPI.getClassToSubTypeForClass(Mockito.anyString(), Mockito.any())) //
        .thenReturn(prepareOptional(type1));
    Mockito.when(siteServerAPI.getEventToOutcomeForType(Mockito.any(List.class), Mockito.any())) //
        .thenReturn(
            prepareOptional( //
                new EventForTest(
                    "11",
                    "E1",
                    type1.getId(), //
                    new MarketForTest(
                        "111",
                        "M11", //
                        new OutcomeForTest("1111", "O111") //
                        ) //
                    ) //
                ));

    Date date = new Date();
    // first call
    missingDataChecker.validate(date);
    // mark data as validated
    Mockito.when(validationCalendarService.isDateValidated(Mockito.any())).thenReturn(true);
    // second call for the same date
    missingDataChecker.validate(new Date(date.getTime() + 1));
    ArgumentCaptor<MissingTimeFormData> captor = ArgumentCaptor.forClass(MissingTimeFormData.class);
    Mockito.verify(listener, Mockito.times(1)).accept(captor.capture());

    MissingTimeFormData missingData = captor.getValue();
    Assert.assertEquals(1, missingData.getLostTypes().size());

    // mark data as not validated
    Mockito.when(validationCalendarService.isDateValidated(Mockito.any())).thenReturn(false);
    // third call for next day
    missingDataChecker.validate(new Date(date.getTime() + 1000L * 60 * 60 * 24));
    Mockito.verify(listener, Mockito.times(2)).accept(captor.capture());
  }

  @Test
  public void testFilteringTypes() {
    Type type1 = new TypeForTest(1, "A");

    // not accept type as interested
    Mockito.when(meetingFilterService.accept(Mockito.anyString())).thenReturn(false);

    Mockito.when(siteServerAPI.getClassToSubTypeForClass(Mockito.anyString(), Mockito.any())) //
        .thenReturn(prepareOptional(type1));
    Mockito.when(siteServerAPI.getEventToOutcomeForType(Mockito.any(List.class), Mockito.any())) //
        .thenReturn(prepareOptional());

    Date date = new Date();
    missingDataChecker.validate(date);

    ArgumentCaptor<List> listArgumentCaptor = ArgumentCaptor.forClass(List.class);
    Mockito.verify(siteServerAPI)
        .getEventToOutcomeForType(
            listArgumentCaptor.capture(), ArgumentCaptor.forClass(SimpleFilter.class).capture());
    // type is filtered
    Assert.assertTrue(listArgumentCaptor.getValue().isEmpty());
  }

  @Test
  public void testIgnoringTypes() {
    Type type1 = new TypeForTest(1, "A");

    // ignore type
    missingDataChecker.setIgnoredTypes(new HashSet<>(Arrays.asList("a")));

    Mockito.when(siteServerAPI.getClassToSubTypeForClass(Mockito.anyString(), Mockito.any())) //
        .thenReturn(prepareOptional(type1));
    Mockito.when(siteServerAPI.getEventToOutcomeForType(Mockito.any(List.class), Mockito.any())) //
        .thenReturn(prepareOptional());

    Date date = new Date();
    missingDataChecker.validate(date);

    ArgumentCaptor<List> listArgumentCaptor = ArgumentCaptor.forClass(List.class);
    Mockito.verify(siteServerAPI)
        .getEventToOutcomeForType(
            listArgumentCaptor.capture(), ArgumentCaptor.forClass(SimpleFilter.class).capture());
    // type is ignored
    Assert.assertTrue(listArgumentCaptor.getValue().isEmpty());
  }

  @Test
  public void testIgnoredSelections() {
    Type type1 = new TypeForTest(1, "A");

    missingDataChecker.setIgnoredSelections(new HashSet<>(Arrays.asList("O112")));

    Mockito.when(siteServerAPI.getClassToSubTypeForClass(Mockito.anyString(), Mockito.any())) //
        .thenReturn(prepareOptional(type1));
    Mockito.when(siteServerAPI.getEventToOutcomeForType(Mockito.any(List.class), Mockito.any())) //
        .thenReturn(
            prepareOptional( //
                new EventForTest(
                    "11",
                    "E1",
                    type1.getId(), //
                    new MarketForTest(
                        "111",
                        "M11", //
                        new OutcomeForTest("1111", "O111"), //
                        new OutcomeForTest("1112", "O112") //
                        ) //
                    ) //
                ));

    Mockito.when(timeformMeetingService.getMeetingsByDate(Mockito.any()))
        .thenReturn( //
            Arrays.asList( //
                buildMeeting(
                    1, //
                    buildRace(
                        11, //
                        buildEntry(1111) //
                        ) //
                    ) //
                ) //
            );

    missingDataChecker.validate(new Date());
    ArgumentCaptor<MissingTimeFormData> captor = ArgumentCaptor.forClass(MissingTimeFormData.class);
    Mockito.verify(listener, Mockito.never()).accept(captor.capture());
  }

  @Test
  public void testIgnoredMarkets() {
    Type type1 = new TypeForTest(1, "A");

    missingDataChecker.setIgnoredMarkets(new HashSet<>(Arrays.asList("M11")));

    Mockito.when(siteServerAPI.getClassToSubTypeForClass(Mockito.anyString(), Mockito.any())) //
        .thenReturn(prepareOptional(type1));
    Mockito.when(siteServerAPI.getEventToOutcomeForType(Mockito.any(List.class), Mockito.any())) //
        .thenReturn(
            prepareOptional( //
                new EventForTest(
                    "11",
                    "E1",
                    type1.getId(), //
                    new MarketForTest(
                        "111",
                        "M11", //
                        new OutcomeForTest("1111", "O111"), //
                        new OutcomeForTest("1112", "O112") //
                        ) //
                    ) //
                ));

    Mockito.when(timeformMeetingService.getMeetingsByDate(Mockito.any()))
        .thenReturn( //
            Arrays.asList( //
                buildMeeting(
                    1, //
                    buildRace(
                        11, //
                        buildEntry(1111) //
                        ) //
                    ) //
                ) //
            );

    missingDataChecker.validate(new Date());
    ArgumentCaptor<MissingTimeFormData> captor = ArgumentCaptor.forClass(MissingTimeFormData.class);
    Mockito.verify(listener, Mockito.never()).accept(captor.capture());
  }

  @Test
  public void testLostData() {
    Type type1 = new TypeForTest(1, "A");
    Type type2 = new TypeForTest(2, "B");

    Mockito.when(siteServerAPI.getClassToSubTypeForClass(Mockito.anyString(), Mockito.any())) //
        .thenReturn(prepareOptional(type1, type2));
    Mockito.when(siteServerAPI.getEventToOutcomeForType(Mockito.any(List.class), Mockito.any())) //
        .thenReturn(
            prepareOptional( //
                new EventForTest(
                    "11",
                    "E1",
                    type1.getId(), //
                    new MarketForTest(
                        "111",
                        "M11", //
                        new OutcomeForTest("1111", "O111"), //
                        new OutcomeForTest("1112", "O112") //
                        ), //
                    new MarketForTest(
                        "112",
                        "M12", //
                        new OutcomeForTest("1121", "O121"), //
                        new OutcomeForTest("1122", "O122") //
                        ) //
                    ), //
                new EventForTest(
                    "12",
                    "E2",
                    type1.getId(), //
                    new MarketForTest(
                        "121",
                        "M21", //
                        new OutcomeForTest("1211", "O211"), //
                        new OutcomeForTest("1212", "O212") //
                        ), //
                    new MarketForTest(
                        "122",
                        "M22", //
                        new OutcomeForTest("1221", "O221"), //
                        new OutcomeForTest("1222", "O222") //
                        ) //
                    ), //
                new EventForTest(
                    "13",
                    "E3",
                    type2.getId(), //
                    new MarketForTest(
                        "131",
                        "M31", //
                        new OutcomeForTest("1311", "O311"), //
                        new OutcomeForTest("1312", "O312") //
                        ), //
                    new MarketForTest(
                        "132",
                        "M32", //
                        new OutcomeForTest("1321", "O321"), //
                        new OutcomeForTest("1322", "O322") //
                        ) //
                    ) //
                ));

    Mockito.when(timeformMeetingService.getMeetingsByDate(Mockito.any()))
        .thenReturn( //
            Arrays.asList( //
                buildMeeting(
                    1, //
                    buildRace(
                        11, //
                        buildEntry(1111), //
                        buildEntry(1112), //
                        buildEntry(1121), //
                        buildEntry(1122) //
                        ), //
                    buildRace(
                        12, //
                        buildEntry(1211), //
                        buildEntry(1222) //
                        ) //
                    ) //
                ) //
            );

    missingDataChecker.validate(new Date());
    ArgumentCaptor<MissingTimeFormData> captor = ArgumentCaptor.forClass(MissingTimeFormData.class);
    Mockito.verify(listener).accept(captor.capture());

    MissingTimeFormData missingData = captor.getValue();
    Assert.assertEquals(1, missingData.getLostTypes().size());
    Assert.assertEquals(1, missingData.getLostEvents().size());
    Assert.assertEquals(2, missingData.getLostOutcomes().size());

    Assert.assertEquals("B", missingData.getLostTypes().get(0).getName());
    Assert.assertEquals("B", missingData.getLostEvents().get(0).getType().getName());
    Assert.assertEquals("E3", missingData.getLostEvents().get(0).getEvent().getName());

    Assert.assertEquals("A", missingData.getLostOutcomes().get(0).getType().getName());
    Assert.assertEquals("E2", missingData.getLostOutcomes().get(0).getEvent().getName());
    Assert.assertEquals("M21", missingData.getLostOutcomes().get(0).getMarket().getName());
    Assert.assertEquals("O212", missingData.getLostOutcomes().get(0).getOutcome().getName());

    Assert.assertEquals("A", missingData.getLostOutcomes().get(1).getType().getName());
    Assert.assertEquals("E2", missingData.getLostOutcomes().get(1).getEvent().getName());
    Assert.assertEquals("M22", missingData.getLostOutcomes().get(1).getMarket().getName());
    Assert.assertEquals("O221", missingData.getLostOutcomes().get(1).getOutcome().getName());
  }

  private <T> Optional<List<T>> prepareOptional(T... elements) {
    return Optional.of(Arrays.asList(elements));
  }

  private Meeting buildMeeting(int id, Race... races) {
    Meeting meeting = new Meeting();
    meeting.setOpenBetIds(new HashSet<>(Arrays.asList(1)));
    meeting.setRaces(new HashSet<>(Arrays.asList(races)));
    return meeting;
  }

  private Race buildRace(int id, Entry... entries) {
    Race race = new Race();
    race.setRaceId(id * 13);
    race.setOpenBetIds(new HashSet<>(Arrays.asList(id)));
    race.setEntries(new HashSet<>(Arrays.asList(entries)));
    return race;
  }

  private Entry buildEntry(int id) {
    EntryForTest entry = new EntryForTest();
    entry.setEntryId(id * 13);
    entry.setOpenBetIds(new HashSet<>(Arrays.asList(id)));
    return entry;
  }

  @Test
  public void testIgnoredFlags() {
    Type type1 = new TypeForTest(1, "A");

    missingDataChecker.setIgnoredClassFlagCodes(new HashSet<>(Arrays.asList("E1")));

    Mockito.when(siteServerAPI.getClassToSubTypeForClass(Mockito.anyString(), Mockito.any())) //
        .thenReturn(prepareOptional(type1));
    Mockito.when(siteServerAPI.getEventToOutcomeForType(Mockito.any(List.class), Mockito.any())) //
        .thenReturn(
            prepareOptional( //
                new EventForTest(
                    "11",
                    "A1,E1",
                    type1.getId(), //
                    new MarketForTest(
                        "111",
                        "M11", //
                        new OutcomeForTest("1111", "O111"), //
                        new OutcomeForTest("1112", "O112") //
                        ) //
                    ) //
                ));

    Mockito.when(timeformMeetingService.getMeetingsByDate(Mockito.any()))
        .thenReturn( //
            Arrays.asList( //
                buildMeeting(
                    1, //
                    buildRace(
                        11, //
                        buildEntry(1111) //
                        ) //
                    ) //
                ) //
            );

    missingDataChecker.validate(new Date());
    ArgumentCaptor<MissingTimeFormData> captor = ArgumentCaptor.forClass(MissingTimeFormData.class);
    Mockito.verify(listener, Mockito.never()).accept(captor.capture());
  }

  @Test
  public void testStatusDescriptions() {
    Type type1 = new TypeForTest(1, "A");

    missingDataChecker.setIgnoredStatusDescriptions(new HashSet<>(Arrays.asList("status1")));

    Mockito.when(siteServerAPI.getClassToSubTypeForClass(Mockito.anyString(), Mockito.any())) //
        .thenReturn(prepareOptional(type1));
    Mockito.when(siteServerAPI.getEventToOutcomeForType(Mockito.any(List.class), Mockito.any())) //
        .thenReturn(
            prepareOptional( //
                new EventForTest(
                    "11",
                    "E1",
                    type1.getId(), //
                    new MarketForTest(
                        "111",
                        "M11", //
                        new OutcomeForTest("1111", "O111"), //
                        new OutcomeForTest("1112", "O112") //
                        ) //
                    ) //
                ));

    Mockito.when(timeformMeetingService.getMeetingsByDate(Mockito.any()))
        .thenReturn( //
            Arrays.asList( //
                buildMeeting(
                    1, //
                    buildRace(
                        11, //
                        buildEntry(1111),
                        buildEntry(1112) //
                        ) //
                    ) //
                ) //
            );

    missingDataChecker.validate(new Date());
    ArgumentCaptor<MissingTimeFormData> captor = ArgumentCaptor.forClass(MissingTimeFormData.class);
    Mockito.verify(listener, Mockito.never()).accept(captor.capture());
  }
}
