package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.RacingEdpMarketDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RacingEdpMarket;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.RacingEdpMarketPublicService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class RacingEdpMarketsAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<RacingEdpMarket> {

  @Mock private RacingEdpMarketPublicService service;
  @Getter @InjectMocks private RacingEdpMarketsAfterSaveListener listener;

  @Getter @Mock private RacingEdpMarket entity;
  @Getter private List<RacingEdpMarketDto> collection = Arrays.asList(new RacingEdpMarketDto());

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "racing-edp-markets"},
          {"connect", "api/connect", "racing-edp-markets"}
        });
  }

  @Before
  public void init() {

    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
