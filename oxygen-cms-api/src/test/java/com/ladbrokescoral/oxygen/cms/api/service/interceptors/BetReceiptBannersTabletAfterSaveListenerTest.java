package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BetReceiptBannerTabletDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetReceiptBannerTablet;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetReceiptBannerTabletPublicService;
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
public class BetReceiptBannersTabletAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<BetReceiptBannerTablet> {

  @Mock private BetReceiptBannerTabletPublicService service;
  @Getter @InjectMocks private BetReceiptBannersTabletAfterSaveListener listener;

  @Getter @Mock private BetReceiptBannerTablet entity;

  @Getter
  private List<BetReceiptBannerTabletDto> collection =
      Arrays.asList(new BetReceiptBannerTabletDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma/bet-receipt-banners", "tablet"},
          {"connect", "api/connect/bet-receipt-banners", "tablet"}
        });
  }

  @Before
  public void init() {

    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
