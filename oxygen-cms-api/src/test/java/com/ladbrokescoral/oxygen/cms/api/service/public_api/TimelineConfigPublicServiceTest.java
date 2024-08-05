package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;
import static org.mockito.Matchers.anyString;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.dto.TimelineGeneralConfigDto;
import com.ladbrokescoral.oxygen.cms.api.dto.TimelineSplashConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Campaign;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Config;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelineSplashConfig;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineCampaignService;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineConfigService;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineSplashConfigService;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class TimelineConfigPublicServiceTest {
  public static final String BRAND = "ladbrokes";
  public static final String CAMPAIGN_ID = "3443543";
  private TimelineConfigPublicService service;

  @Mock private TimelineConfigService generalConfigService;
  @Mock private TimelineSplashConfigService splashConfigService;
  @Mock private TimelineCampaignService timelineCampaignService;

  @Before
  public void init() {
    Config config = new Config();
    when(generalConfigService.findOptionalByBrand(anyString())).thenReturn(Optional.of(config));
    Campaign campaign = new Campaign();
    campaign.setId(CAMPAIGN_ID);
    when(timelineCampaignService.findCurrentLiveCampaignByBrand(anyString()))
        .thenReturn(Optional.of(campaign));
    TimelineSplashConfig splashPageConfig = new TimelineSplashConfig();
    when(splashConfigService.findOptionalByBrand(BRAND)).thenReturn(Optional.of(splashPageConfig));

    service =
        new TimelineConfigPublicService(
            generalConfigService, splashConfigService, timelineCampaignService);
  }

  @Test
  public void testFindGeneralConfigByBrand() {
    Optional<TimelineGeneralConfigDto> config = service.findGeneralConfigByBrand(BRAND);

    verify(generalConfigService).findOptionalByBrand(BRAND);
    verify(timelineCampaignService).findCurrentLiveCampaignByBrand(BRAND);
    assertEquals(CAMPAIGN_ID, config.get().getLiveCampaignId());
  }

  @Test
  public void testFindSplashPageConfigByBrand() {
    Optional<TimelineSplashConfigDto> config = service.findSplashConfigByBrand(BRAND);

    verify(splashConfigService).findOptionalByBrand(BRAND);
    assertNotEquals(Optional.empty(), config);
  }

  @Test
  public void testFindSplashPageConfigByBrandReturnsEmpty() {
    when(splashConfigService.findOptionalByBrand(BRAND)).thenReturn(Optional.empty());

    Optional<TimelineSplashConfigDto> config = service.findSplashConfigByBrand(BRAND);

    verify(splashConfigService).findOptionalByBrand(BRAND);
    assertEquals(Optional.empty(), config);
  }
}
