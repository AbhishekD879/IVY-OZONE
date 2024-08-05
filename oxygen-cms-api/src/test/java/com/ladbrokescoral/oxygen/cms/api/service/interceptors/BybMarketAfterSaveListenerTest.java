package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BybMarketDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybMarket;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BybMarketPublicService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class BybMarketAfterSaveListenerTest extends AbstractAfterSaveListenerTest<BybMarket> {

  @Mock private BybMarketPublicService service;
  @Getter @InjectMocks private BybMarketAfterSaveListener listener;

  @Getter @Mock private BybMarket entity;
  @Getter private List<BybMarketDto> collection = Arrays.asList(new BybMarketDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "byb-markets"},
          {"connect", "api/connect", "byb-markets"}
        });
  }

  @Before
  public void init() {

    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
