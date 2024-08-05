package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.FirstBetPlaceCFDto;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.FirstBetPlaceTutorial;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.FirstBetPlaceTutorialService;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class FirstBetPlaceAfterSaveListener extends BasicMongoEventListener<FirstBetPlaceTutorial> {

  private final FirstBetPlaceTutorialService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "first-bet-place";

  public FirstBetPlaceAfterSaveListener(
      final FirstBetPlaceTutorialService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<FirstBetPlaceTutorial> event) {
    String brand = event.getSource().getBrand();
    Optional<FirstBetPlaceCFDto> content = service.convertToCFDto(event.getSource());
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
