package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BetReceiptBannerTabletDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetReceiptBannerTablet;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetReceiptBannerTabletPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class BetReceiptBannersTabletAfterSaveListener
    extends BasicMongoEventListener<BetReceiptBannerTablet> {

  private final BetReceiptBannerTabletPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}/bet-receipt-banners";
  private static final String FILE_NAME = "tablet";

  public BetReceiptBannersTabletAfterSaveListener(
      final BetReceiptBannerTabletPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<BetReceiptBannerTablet> event) {
    String brand = event.getSource().getBrand();
    List<BetReceiptBannerTabletDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
