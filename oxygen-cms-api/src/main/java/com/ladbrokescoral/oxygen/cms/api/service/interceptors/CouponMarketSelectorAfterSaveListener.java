package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.CouponMarketSelectorDto;
import com.ladbrokescoral.oxygen.cms.api.entity.CouponMarketSelector;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.CouponMarketSelectorPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class CouponMarketSelectorAfterSaveListener
    extends BasicMongoEventListener<CouponMarketSelector> {

  private final CouponMarketSelectorPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "coupon-market-selector";

  public CouponMarketSelectorAfterSaveListener(
      final CouponMarketSelectorPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<CouponMarketSelector> event) {
    String brand = event.getSource().getBrand();
    List<CouponMarketSelectorDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
