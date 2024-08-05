package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSport;
import com.ladbrokescoral.oxygen.cms.api.dto.VirtualSportDto;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.interceptors.helpers.BasicInitialDataAfterSaveListener;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.VirtualSportPublicService;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class VirtualSportAfterSaveListener extends BasicInitialDataAfterSaveListener<VirtualSport> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "virtual-sports";

  private final VirtualSportPublicService virtualSportPublicService;

  public VirtualSportAfterSaveListener(
      InitialDataService initialDataService,
      DeliveryNetworkService deliveryNetworkService,
      VirtualSportPublicService service) {
    super(initialDataService, deliveryNetworkService);
    this.virtualSportPublicService = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<VirtualSport> event) {
    log.info("Updating VirtualSports in InitialData");

    String brand = event.getSource().getBrand();
    List<VirtualSportDto> content =
        virtualSportPublicService.findActiveSportsWithActiveTracksOnly(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);

    super.upload(event);
  }
}
