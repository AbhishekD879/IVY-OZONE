package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.CouponMarketMappingDto;
import com.ladbrokescoral.oxygen.cms.api.entity.CouponMarketMappingEntity;
import com.ladbrokescoral.oxygen.cms.api.service.CouponMarketMappingService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;

/** @author PBalarangakumar 21-02-2024 */
@RunWith(Parameterized.class)
public class CouponMarketMappingAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<CouponMarketMappingEntity> {

  @Mock private CouponMarketMappingService service;
  @Getter @InjectMocks private CouponMarketMappingAfterSaveListener listener;
  @Getter @Mock private CouponMarketMappingEntity entity;

  @Getter @Mock
  private List<CouponMarketMappingDto> collection = Arrays.asList(new CouponMarketMappingDto());

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "coupon-market-mapping"},
          {"connect", "api/connect", "coupon-market-mapping"}
        });
  }

  @Before
  public void init() {
    given(service.findByBrandDto(anyString())).willReturn(this.getCollection());
  }
}
