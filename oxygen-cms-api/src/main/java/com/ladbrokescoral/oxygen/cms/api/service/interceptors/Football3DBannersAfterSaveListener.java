package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.FootballBanner3dDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Football3DBanner;
import com.ladbrokescoral.oxygen.cms.api.mapping.Football3DBannerMapper;
import com.ladbrokescoral.oxygen.cms.api.service.Football3DBannerService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class Football3DBannersAfterSaveListener extends BasicMongoEventListener<Football3DBanner> {

  private final Football3DBannerService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "3d-football-banners";

  public Football3DBannersAfterSaveListener(
      final Football3DBannerService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<Football3DBanner> event) {
    String brand = event.getSource().getBrand();
    Collection<Football3DBanner> football3DBannerCollection =
        service.findAllByBrandAndDisabled(brand);
    List<FootballBanner3dDto> content =
        football3DBannerCollection.stream()
            .map(Football3DBannerMapper.INSTANCE::toDto)
            .collect(Collectors.toList());
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
