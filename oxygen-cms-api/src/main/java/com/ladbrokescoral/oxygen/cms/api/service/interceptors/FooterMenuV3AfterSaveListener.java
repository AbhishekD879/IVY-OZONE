package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.FooterMenuV2Dto;
import com.ladbrokescoral.oxygen.cms.api.dto.FooterMenuV3Dto;
import com.ladbrokescoral.oxygen.cms.api.entity.DeviceType;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FooterMenuPublicService;
import java.util.Arrays;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class FooterMenuV3AfterSaveListener extends BasicMongoEventListener<FooterMenu> {

  private final FooterMenuPublicService service;
  private static final String PATH_TEMPLATE_V_2 = "api/v2/{0}";
  private static final String PATH_TEMPLATE_V_3 = "api/v3/{0}";
  private static final String FILE_NAME = "footer-menu";
  private static final String COLLECTION_NAME = "footermenus";

  public FooterMenuV3AfterSaveListener(
      final FooterMenuPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<FooterMenu> event) {
    if (COLLECTION_NAME.equals(event.getCollectionName())) {
      String brand = event.getSource().getBrand();
      List<FooterMenuV3Dto> content = service.find(brand);
      uploadCollection(brand, PATH_TEMPLATE_V_3, FILE_NAME, content);

      Arrays.asList(DeviceType.values())
          .forEach(
              deviceType -> {
                String device = deviceType.getValue();
                List<FooterMenuV2Dto> v2Content = service.find(brand, device);
                uploadCollection(brand, PATH_TEMPLATE_V_2 + "/" + FILE_NAME, device, v2Content);
              });
    }
  }
}
