package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.CouponMarketSelectorDto;
import com.ladbrokescoral.oxygen.cms.api.entity.CouponMarketSelector;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.CouponMarketSelectorPublicService;
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
public class CouponMarketSelectorAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<CouponMarketSelector> {

  @Mock private CouponMarketSelectorPublicService service;
  @Getter @InjectMocks private CouponMarketSelectorAfterSaveListener listener;

  @Getter @Mock private CouponMarketSelector entity;

  @Getter
  private List<CouponMarketSelectorDto> collection = Arrays.asList(new CouponMarketSelectorDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "coupon-market-selector"},
          {"connect", "api/connect", "coupon-market-selector"}
        });
  }

  @Before
  public void init() {

    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
