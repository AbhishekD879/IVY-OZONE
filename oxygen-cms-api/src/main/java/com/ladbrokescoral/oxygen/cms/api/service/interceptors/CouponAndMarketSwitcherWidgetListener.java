package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.CouponAndMarketSwitcherCFDto;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CouponAndMarketSwitcher;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.CouponAndMarketSwitcherWidgetService;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class CouponAndMarketSwitcherWidgetListener
    extends BasicMongoEventListener<CouponAndMarketSwitcher> {
  private final CouponAndMarketSwitcherWidgetService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "couponAndMarketSwitcherWidget";

  public CouponAndMarketSwitcherWidgetListener(
      final CouponAndMarketSwitcherWidgetService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<CouponAndMarketSwitcher> event) {
    String brand = event.getSource().getBrand();
    Optional<CouponAndMarketSwitcherCFDto> content = service.convertToCFDto(event.getSource());
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
