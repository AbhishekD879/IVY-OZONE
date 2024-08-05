package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.PromotionWithSectionContainerDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PromotionSection;
import com.ladbrokescoral.oxygen.cms.api.service.PromotionSectionService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.PromotionPublicService;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class PromotionSectionsAfterSaveListener extends BasicMongoEventListener<PromotionSection> {
  private final PromotionPublicService promotionService;
  private final PromotionSectionService promotionSectionService;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "grouped-promotions";

  public PromotionSectionsAfterSaveListener(
      final PromotionPublicService promotionService,
      final PromotionSectionService promotionSectionService,
      final DeliveryNetworkService context) {
    super(context);
    this.promotionService = promotionService;
    this.promotionSectionService = promotionSectionService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<PromotionSection> event) {
    String brand = event.getSource().getBrand();
    if (!event.getSource().getId().equals(brand)) {
      promotionSectionService.save(promotionSectionService.unassignedSection(brand));
    }
    PromotionWithSectionContainerDto content = promotionService.findByBrandGroupedBySections(brand);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, Optional.of(content));
  }
}
