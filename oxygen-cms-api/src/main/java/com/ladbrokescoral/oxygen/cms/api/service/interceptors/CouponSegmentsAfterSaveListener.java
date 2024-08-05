package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.CouponSegmentDto;
import com.ladbrokescoral.oxygen.cms.api.entity.CouponSegment;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.CouponSegmentPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class CouponSegmentsAfterSaveListener extends BasicMongoEventListener<CouponSegment> {

  private final CouponSegmentPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "coupon-segments";

  public CouponSegmentsAfterSaveListener(
      final CouponSegmentPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<CouponSegment> event) {
    String brand = event.getSource().getBrand();
    List<CouponSegmentDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
