package com.ladbrokescoral.oxygen.bigcompetition.service;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.*;

import com.egalacoral.spark.siteserver.api.ExistsFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.bigcompetition.TestUtil;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.SpecialsModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.EventDto;
import com.ladbrokescoral.oxygen.bigcompetition.service.impl.SiteServeApiServiceImpl;
import com.ladbrokescoral.oxygen.bigcompetition.service.impl.module.SpecialModuleServiceImpl;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModuleType;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionSpecialModuleData;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CompetitionSpecialServiceTest {

  @Mock private SiteServerApi siteServerApiMock;
  private SpecialModuleService competitionSpecialService;

  @Before
  public void setUp() throws Exception {
    competitionSpecialService =
        new SpecialModuleServiceImpl(new SiteServeApiServiceImpl(siteServerApiMock));
  }

  @Test
  public void testPopulateSpecialModuleWithEventsByEventId() {
    List<Event> events =
        TestUtil.deserializeListWithJackson(
            "/competitionSpecialService/event_from_ss_by_eventId.json", Event.class);
    when(siteServerApiMock.getEventToOutcomeForEvent(
            eq(Collections.singletonList("8130591")),
            any(SimpleFilter.class),
            any(ExistsFilter.class),
            eq(Arrays.asList("event", "market")),
            eq(false)))
        .thenReturn(Optional.ofNullable(events));

    CompetitionModule competitionModule = new CompetitionModule();
    competitionModule.setId("12345678");
    competitionModule.setType(CompetitionModuleType.SPECIALS);
    CompetitionSpecialModuleData moduleData = new CompetitionSpecialModuleData();
    moduleData.setEventIds(Collections.singletonList(8130591));
    competitionModule.setSpecialModuleData(moduleData);
    SpecialsModuleDto moduleDto =
        (SpecialsModuleDto) competitionSpecialService.process(competitionModule);

    List<EventDto> expected =
        TestUtil.deserializeListWithJackson(
            "/competitionSpecialService/eventsDto.json", EventDto.class);

    assertEquals(new HashSet<>(expected), moduleDto.getEvents());
  }

  @Test
  public void testPopulateSpecialModuleWithEventsByTypeId() {
    List<Event> events =
        TestUtil.deserializeListWithJackson(
            "/competitionSpecialService/event_from_ss_by_eventId.json", Event.class);
    when(siteServerApiMock.getEventToOutcomeForType(
            eq(Collections.singletonList("442")),
            any(SimpleFilter.class),
            any(ExistsFilter.class),
            eq(Arrays.asList("event", "market")),
            eq(false)))
        .thenReturn(Optional.ofNullable(events));

    CompetitionModule competitionModule = new CompetitionModule();
    competitionModule.setId("12345678");
    competitionModule.setType(CompetitionModuleType.SPECIALS_OVERVIEW);
    CompetitionSpecialModuleData moduleData = new CompetitionSpecialModuleData();
    moduleData.setTypeIds(Collections.singletonList(442));
    competitionModule.setSpecialModuleData(moduleData);
    SpecialsModuleDto moduleDto =
        (SpecialsModuleDto) competitionSpecialService.process(competitionModule);

    List<EventDto> expected =
        TestUtil.deserializeListWithJackson(
            "/competitionSpecialService/eventsDto.json", EventDto.class);

    assertEquals(new HashSet<>(expected), moduleDto.getEvents());
  }
}
