package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BankingMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BankingMenu;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BankingMenuPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class BankingMenuAfterSaveListener extends BasicMongoEventListener<BankingMenu> {
  private final BankingMenuPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILENAME = "banking-menu";

  public BankingMenuAfterSaveListener(
      final BankingMenuPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<BankingMenu> event) {
    String brand = event.getSource().getBrand();
    List<BankingMenuDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILENAME, content);
  }
}
