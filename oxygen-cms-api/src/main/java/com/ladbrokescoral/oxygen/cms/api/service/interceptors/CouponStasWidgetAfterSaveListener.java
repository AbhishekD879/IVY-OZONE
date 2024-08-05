package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.CouponStatsWidgetCFDto;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CouponStatsWidget;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.CouponStatsWidgetService;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class CouponStasWidgetAfterSaveListener extends BasicMongoEventListener<CouponStatsWidget> {

  private final CouponStatsWidgetService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "coupon-stats-widget";

  public CouponStasWidgetAfterSaveListener(
      final CouponStatsWidgetService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<CouponStatsWidget> event) {
    String brand = event.getSource().getBrand();
    Optional<CouponStatsWidgetCFDto> content = service.convertToCFDto(event.getSource());
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
