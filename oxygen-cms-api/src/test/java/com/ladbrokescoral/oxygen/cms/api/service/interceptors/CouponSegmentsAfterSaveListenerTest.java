package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.CouponSegmentDto;
import com.ladbrokescoral.oxygen.cms.api.entity.CouponSegment;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.CouponSegmentPublicService;
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
public class CouponSegmentsAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<CouponSegment> {

  @Mock private CouponSegmentPublicService service;
  @Getter @InjectMocks private CouponSegmentsAfterSaveListener listener;

  @Getter @Mock private CouponSegment entity;
  @Getter private List<CouponSegmentDto> collection = Arrays.asList(new CouponSegmentDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "coupon-segments"},
          {"connect", "api/connect", "coupon-segments"}
        });
  }

  @Before
  public void init() {

    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
