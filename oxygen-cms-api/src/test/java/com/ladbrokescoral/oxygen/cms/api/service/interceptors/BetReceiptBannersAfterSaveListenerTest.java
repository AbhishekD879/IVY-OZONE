package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BetReceiptBannerDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetReceiptBanner;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetReceiptBannerPublicService;
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
public class BetReceiptBannersAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<BetReceiptBanner> {

  @Mock private BetReceiptBannerPublicService service;
  @Getter @InjectMocks private BetReceiptBannersAfterSaveListener listener;

  @Getter @Mock private BetReceiptBanner entity;

  @Getter private List<BetReceiptBannerDto> collection = Arrays.asList(new BetReceiptBannerDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma/bet-receipt-banners", "mobile"},
          {"connect", "api/connect/bet-receipt-banners", "mobile"}
        });
  }

  @Before
  public void init() {

    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
