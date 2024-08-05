package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.coral.oxygen.df.model.RaceEvent;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.entity.NextRacesResult;
import com.ladbrokescoral.oxygen.cms.api.entity.TypeFlagCodes;
import com.ladbrokescoral.oxygen.cms.api.service.df.DFService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.NextEventsParameters;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.NextEventsParameters.NextEventsParametersBuilder;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(MockitoJUnitRunner.class)
public class NextRacesPublicServiceTest {

  @Mock private SiteServeService siteServerService;

  @Mock private DFService dfService;

  @InjectMocks private NextRacesPublicService nextRacesPublicService;

  @Before
  public void init() throws IOException {

    Mockito.when(
            dfService.getNextRaces(Mockito.anyString(), Mockito.anyInt(), Mockito.anyCollection()))
        .thenReturn(Optional.empty());

    Mockito.when(
            dfService.getNextRaces(Mockito.anyString(), Mockito.anyInt(), Mockito.anyCollection()))
        .thenReturn(Optional.of(new HashMap()));

    ReflectionTestUtils.setField(nextRacesPublicService, "timePeriodMinutes", 15);
    ReflectionTestUtils.setField(nextRacesPublicService, "maxNextRaces", 3);
    ReflectionTestUtils.setField(nextRacesPublicService, "categoryId", 21);
  }

  @Test
  public void findEmpty() throws IOException {
    NextRacesResult result = nextRacesPublicService.find("bma");
    Assert.assertNotNull(result);
  }

  @Test
  public void findUkAndIreNoDF() throws IOException {
    mockSiteServer("UK,IE");
    NextRacesResult result = nextRacesPublicService.find("bma");
    Assert.assertEquals(3, result.getRaces().size());
    Assert.assertTrue(result.getUkAndIre());
  }

  private void mockSiteServer(String s) {
    NextEventsParametersBuilder paramsBuilder = NextEventsParameters.builder();
    paramsBuilder
        .brand("bma")
        .typeFlagCodes(TypeFlagCodes.of("UK,IRE,INT"))
        .comparator(NextRacesPublicService.START_TIME_COMPARATOR)
        .categoryId(21)
        .timePeriodMinutes(15);
    ArrayList<Event> value = new ArrayList<>();
    value.add(buildEvent("1", s));
    value.add(buildEvent("2", s));
    value.add(buildEvent("3", s));
    value.add(buildEvent("4", s));
    Mockito.when(siteServerService.getNextEvents(paramsBuilder.build())).thenReturn(value);
  }

  // FIXME: remove this dupplication of #mockSiteServer(String s) and inccorect stubing usage
  private void mockSiteServerForTodayRaces(String s) {
    NextEventsParametersBuilder paramsBuilder = NextEventsParameters.builder();
    paramsBuilder
        .brand("bma")
        .typeFlagCodes(TypeFlagCodes.of("UK,IRE,INT"))
        .comparator(NextRacesPublicService.START_TIME_COMPARATOR)
        .categoryId(21)
        .timePeriodMinutes(Mockito.anyInt());
    ArrayList<Event> value = new ArrayList<>();
    value.add(buildEvent("1", s));
    value.add(buildEvent("2", s));
    value.add(buildEvent("3", s));
    value.add(buildEvent("4", s));
    Mockito.when(siteServerService.getNextEvents(paramsBuilder.build()))
        .thenReturn(Mockito.anyList(), value);
  }

  @Test
  public void findIntNoDF() throws IOException {
    mockSiteServer("INT");
    NextRacesResult result = nextRacesPublicService.find("bma");
    Assert.assertEquals(3, result.getRaces().size());
    Assert.assertFalse(result.getUkAndIre());
  }

  @Ignore("FIXME: test is not testing subject")
  @Test
  public void findIntNoDFForToday() throws IOException {
    mockSiteServerForTodayRaces("INT");
    NextRacesResult result = nextRacesPublicService.find("bma");
    Assert.assertEquals(3, result.getRaces().size());
    Assert.assertTrue(result.getUkAndIre());
  }

  @Test
  public void findUkAndIre() throws IOException {
    mockDataFabric();
    mockSiteServer("UK,IE");
    NextRacesResult result = nextRacesPublicService.find("bma");
    Assert.assertEquals(3, result.getRaces().size());
    Assert.assertTrue(result.getUkAndIre());
    Assert.assertEquals("123", result.getRaces().get(0).getDistance());
  }

  @Test
  public void findUkAndIreForDfEmpty() throws IOException {
    mockDataFabric();
    mockSiteServer("UK,IE");
    Mockito.when(
            dfService.getNextRaces(Mockito.anyString(), Mockito.anyInt(), Mockito.anyCollection()))
        .thenReturn(Optional.empty());
    NextRacesResult result = nextRacesPublicService.find("bma");
    Assert.assertEquals(3, result.getRaces().size());
    Assert.assertTrue(result.getUkAndIre());
  }

  @Test
  public void findInt() throws IOException {
    mockDataFabric();
    mockSiteServer("INT");
    NextRacesResult result = nextRacesPublicService.find("bma");
    Assert.assertEquals(3, result.getRaces().size());
    Assert.assertFalse(result.getUkAndIre());
    Assert.assertEquals("123", result.getRaces().get(0).getDistance());
  }

  private void mockDataFabric() throws IOException {
    HashMap<Long, RaceEvent> races = new HashMap();
    races.put(1L, buildRaceEvent());
    races.put(3L, buildRaceEvent());
    Mockito.when(
            dfService.getNextRaces(Mockito.anyString(), Mockito.anyInt(), Mockito.anyCollection()))
        .thenReturn(Optional.of(races));
  }

  private RaceEvent buildRaceEvent() {
    RaceEvent raceEvent = new RaceEvent();
    raceEvent.setDistance("123");
    return raceEvent;
  }

  private Event buildEvent(String id, String typeFlagCodes) {
    Event event = new Event();
    event.setId(id);
    event.setName("name" + id);
    event.setTypeFlagCodes(typeFlagCodes);
    return event;
  }
}
