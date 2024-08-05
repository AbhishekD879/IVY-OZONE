package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.FreeRidePublicSplashPageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideSplashPage;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FreeRideSplashPagePublicService;
import java.util.List;
import java.util.Objects;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class FreeRideSplashPageAfterSaveListener
    extends BasicMongoEventListener<FreeRideSplashPage> {
  private final FreeRideSplashPagePublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILENAME = "freeride-splashpage";

  public FreeRideSplashPageAfterSaveListener(
      final FreeRideSplashPagePublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<FreeRideSplashPage> event) {
    String brand = event.getSource().getBrand();
    List<FreeRidePublicSplashPageDto> splashPages = service.getFreeRideSplashPageByBrand(brand);
    FreeRidePublicSplashPageDto splashPagesDto = !splashPages.isEmpty() ? splashPages.get(0) : null;
    if (Objects.nonNull(splashPagesDto)
        && Objects.nonNull(splashPagesDto.getBannerImageUrl())
        && Objects.nonNull(splashPagesDto.getSplashImageUrl())
        && Objects.nonNull(splashPagesDto.getFreeRideLogoUrl())) {
      uploadCollection(brand, PATH_TEMPLATE, FILENAME, splashPages);
    }
  }
}
