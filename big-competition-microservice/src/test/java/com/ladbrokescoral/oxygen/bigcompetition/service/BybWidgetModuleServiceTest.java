package com.ladbrokescoral.oxygen.bigcompetition.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.bigcompetition.TestUtil;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.BybWidgetModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.service.impl.module.BybWidgetModuleServiceImpl;
import com.ladbrokescoral.oxygen.cms.client.model.BybWidgetDataDto;
import com.ladbrokescoral.oxygen.cms.client.model.BybWidgetDto;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import java.time.Instant;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class BybWidgetModuleServiceTest {

  private BybWidgetModuleServiceImpl bybWidgetModuleService;

  @Mock CmsApiService cmsApiService;
  @Mock SiteServeApiService siteServeApiService;

  private static final String BRAND = "ladbrokes";

  @Before
  public void setUp() {
    bybWidgetModuleService =
        new BybWidgetModuleServiceImpl(siteServeApiService, cmsApiService, BRAND);
  }

  @Test
  public void testBybWidgetFromCms() {

    CompetitionModule competitionModule =
        TestUtil.deserializeWithJackson(
            "/competitionBybWidgetService/bybWidgetModule.json", CompetitionModule.class);
    List<Event> events =
        TestUtil.deserializeListWithJackson(
            "/competitionBybWidgetService/events_from_siteserver.json", Event.class);

    when(siteServeApiService.getEventToOutcomeForMarkets(any())).thenReturn(Optional.of(events));
    when(cmsApiService.getBybWidget(any())).thenReturn(Optional.of(getBybWidgetDto()));

    BybWidgetModuleDto moduleDto = this.bybWidgetModuleService.process(competitionModule);
    Assert.assertNotNull(moduleDto);
  }

  private BybWidgetDto getBybWidgetDto() {
    BybWidgetDto widgetDto = new BybWidgetDto();
    BybWidgetDataDto dataDto1 = getBybWidgetDataDto(Instant.now(), "236383275");
    BybWidgetDataDto dataDto2 = getBybWidgetDataDto(Instant.now(), "236383276");
    BybWidgetDataDto dataDto3 = getBybWidgetDataDto(Instant.now().plusSeconds(20), "236383275");
    BybWidgetDataDto dataDto4 = getBybWidgetDataDto(Instant.now(), "235135538");
    BybWidgetDataDto dataDto5 = getBybWidgetDataDto(Instant.now(), "235135539");
    widgetDto.setData(Arrays.asList(dataDto1, dataDto2, dataDto3, dataDto4, dataDto5));
    return widgetDto;
  }

  private BybWidgetDataDto getBybWidgetDataDto(Instant displayFrom, String marketId) {
    BybWidgetDataDto dataDto = new BybWidgetDataDto();
    dataDto.setDisplayFrom(displayFrom);
    dataDto.setMarketId(marketId);
    return dataDto;
  }
}
