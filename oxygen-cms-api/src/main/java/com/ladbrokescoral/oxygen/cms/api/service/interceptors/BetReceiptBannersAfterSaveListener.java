package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BetReceiptBannerDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetReceiptBanner;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetReceiptBannerPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class BetReceiptBannersAfterSaveListener extends BasicMongoEventListener<BetReceiptBanner> {

  private final BetReceiptBannerPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}/bet-receipt-banners";
  private static final String FILE_NAME = "mobile";

  public BetReceiptBannersAfterSaveListener(
      final BetReceiptBannerPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<BetReceiptBanner> event) {
    String brand = event.getSource().getBrand();
    List<BetReceiptBannerDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
