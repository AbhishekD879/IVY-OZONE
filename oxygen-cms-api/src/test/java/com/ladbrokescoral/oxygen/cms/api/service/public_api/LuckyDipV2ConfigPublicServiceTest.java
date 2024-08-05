package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipV2ConfigurationPublicDto;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipV2ConfigService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.io.IOException;
import java.util.Optional;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.modelmapper.ModelMapper;

@ExtendWith(MockitoExtension.class)
class LuckyDipV2ConfigPublicServiceTest extends BDDMockito {

  @Mock private LuckyDipV2ConfigService luckyDipConfigService;
  @Mock private SiteServeApiProvider siteServeApiProvider;
  @Mock private SiteServerApi siteServerApi;
  @Mock private ModelMapper modelMapper;

  private Event event;
  private LuckyDipV2ConfigPublicService luckyDipConfigPublicService;

  @BeforeEach
  public void init() throws IOException {
    luckyDipConfigPublicService =
        new LuckyDipV2ConfigPublicService(luckyDipConfigService, siteServeApiProvider, modelMapper);
    event =
        TestUtil.deserializeWithJackson(
            "controller/private_api/validateSSIds/event_from_ss.json", Event.class);
  }

  @Test
  void getAllLuckyDipConfigByBrandAndEventAndEventNotPresentTest() {
    given(siteServeApiProvider.api(any())).willReturn(siteServerApi);
    given(siteServerApi.getEvent(any(), (Boolean) any())).willReturn(Optional.empty());

    Optional<LuckyDipV2ConfigurationPublicDto> ld =
        luckyDipConfigPublicService.getAllLuckyDipConfigByBrandAndEvent("BMA", "123");
    LuckyDipV2ConfigurationPublicDto dto = new LuckyDipV2ConfigurationPublicDto();
    dto.setStatus(null);
    Assertions.assertEquals(ld, Optional.of(dto));
  }

  @Test
  void getAllLuckyDipConfigByBrandAndEventWithExceptionTest() {
    given(siteServeApiProvider.api(any())).willReturn(siteServerApi);
    given(siteServerApi.getEvent(any(), (Boolean) any())).willReturn(Optional.of(event));
    given(luckyDipConfigService.getLDByBrandAndLDConfigLevelId(any(), any()))
        .willReturn(Optional.empty());
    Optional<LuckyDipV2ConfigurationPublicDto> ld =
        luckyDipConfigPublicService.getAllLuckyDipConfigByBrandAndEvent("BMA", "123");
    LuckyDipV2ConfigurationPublicDto dto = new LuckyDipV2ConfigurationPublicDto();
    dto.setStatus(null);
    Assertions.assertEquals(ld, Optional.of(dto));
  }
}
