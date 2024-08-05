package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.CouponMarketMappingDto;
import com.ladbrokescoral.oxygen.cms.api.entity.CouponMarketMappingEntity;
import com.ladbrokescoral.oxygen.cms.api.service.CouponMarketMappingService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

/** @author PBalarangakumar 08-02-2024 */
@Component
public class CouponMarketMappingAfterSaveListener
    extends BasicMongoEventListener<CouponMarketMappingEntity> {

  private final CouponMarketMappingService service;

  private static final String PATH_TEMPLATE = "api/{0}";

  private static final String FILE_NAME = "coupon-market-mapping";

  public CouponMarketMappingAfterSaveListener(
      final DeliveryNetworkService context, final CouponMarketMappingService service) {

    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<CouponMarketMappingEntity> event) {
    final String brand = event.getSource().getBrand();
    final List<CouponMarketMappingDto> content = service.findByBrandDto(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
