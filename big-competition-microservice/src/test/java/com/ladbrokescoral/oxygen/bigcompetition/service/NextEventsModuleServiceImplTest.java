package com.ladbrokescoral.oxygen.bigcompetition.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.model.Aggregation;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.bigcompetition.TestUtil;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.NextEventsModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.service.impl.module.NextEventsModuleServiceImpl;
import com.ladbrokescoral.oxygen.cms.client.model.Competition;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class NextEventsModuleServiceImplTest {

  @Mock CmsApiService cmsApiService;
  @Mock SiteServeApiService siteServeApiService;
  NextEventsModuleServiceImpl nextEventsModuleService;

  @Before
  public void setUp() throws Exception {
    nextEventsModuleService =
        new NextEventsModuleServiceImpl(siteServeApiService, cmsApiService, "bma");
  }

  @Test
  public void testSurfaceBetsFromCms() {

    CompetitionModule competitionModuleDto =
        TestUtil.deserializeWithJackson("/nextEventsService/module.json", CompetitionModule.class);
    List<Event> events =
        TestUtil.deserializeListWithJackson(
            "/nextEventsService/events_from_siteserver.json", Event.class);
    List<Aggregation> aggregations =
        TestUtil.deserializeListWithJackson(
            "/nextEventsService/aggregation_from_siteserver.json", Aggregation.class);
    Competition competition =
        TestUtil.deserializeWithJackson(
            "/nextEventsService/configuration_from_cms.json", Competition.class);

    when(siteServeApiService.getNextEventForType(anyInt())).thenReturn(events);
    when(siteServeApiService.getMarketsCountForEvents(any())).thenReturn(Optional.of(aggregations));
    when(cmsApiService.findCompetitionByBrandAndUri("bma", "premier-league"))
        .thenReturn(Optional.of(competition));
    NextEventsModuleDto process = nextEventsModuleService.process(competitionModuleDto);

    Assert.assertNotNull(process);
  }
}
