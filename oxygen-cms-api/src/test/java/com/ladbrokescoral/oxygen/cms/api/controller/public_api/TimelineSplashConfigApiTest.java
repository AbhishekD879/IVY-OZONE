package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.dto.TimelineSplashConfigDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.TimelineConfigPublicService;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class TimelineSplashConfigApiTest {
  public static final String BRAND = "ladbrokes";
  @Mock private TimelineConfigPublicService service;

  private TimelineSplashConfigApi api;

  private TimelineSplashConfigDto splashConfig;

  @Before
  public void init() {
    splashConfig = new TimelineSplashConfigDto();
    api = new TimelineSplashConfigApi(service);

    when(service.findSplashConfigByBrand(BRAND)).thenReturn(Optional.of(splashConfig));
  }

  @Test
  public void testFindTimelineSplashConfigByBrand() {
    api.findTimelineSplashConfigByBrand(BRAND);

    verify(service).findSplashConfigByBrand(BRAND);
  }
}
