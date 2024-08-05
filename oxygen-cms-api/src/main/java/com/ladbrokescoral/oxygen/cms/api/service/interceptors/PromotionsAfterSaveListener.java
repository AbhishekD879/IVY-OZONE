package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.PromotionContainerDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionV2Dto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionWithSectionContainerDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.service.PromotionSectionService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.PromotionPublicService;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class PromotionsAfterSaveListener extends BackgroundBasicMongoEventListener<Promotion> {
  private final PromotionPublicService promotionService;
  private final PromotionSectionService promotionSectionService;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String V_2_PATH_TEMPLATE = "api/v2/{0}";
  private static final String V_3_PATH_TEMPLATE = "api/v3/{0}";
  private static final String FILE_NAME = "promotions";
  private static final String PROMOTIONS_WITH_SECTIONS_FILE_NAME = "grouped-promotions";

  /**
   * To upload categories on akamai, we need to upload all possible variations of categoryId
   * positions, for example 1,2,3 or 1,4 or 2,4,6 and so on. For six categories there will be 55986
   * combinations (6+6^2+6^3+6^4+6^5+6^6 = 55986) Áfter a discussion with 'Native' team, they use
   * only either 1 or 2 or 3 category id. Only these 3 combinations are supported. updated 1000 as
   * for lads category id and updated 19998 as connect id in coral (BMA-65613)
   */
  private static final List<String> V2_NATIVE_CATEGORIES =
      Arrays.asList("1", "2", "3", "1000", "19998");

  public PromotionsAfterSaveListener(
      final PromotionPublicService promotionService,
      final PromotionSectionService promotionSectionService,
      final DeliveryNetworkService context) {
    super(context);
    this.promotionService = promotionService;
    this.promotionSectionService = promotionSectionService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<Promotion> event) {
    promotionSectionService.save(
        promotionSectionService.unassignedSection(event.getSource().getBrand()));
    super.onAfterSave(event);
  }

  @Override
  protected void onAfterSaveInBackground(AfterSaveEvent<Promotion> event) {
    String brand = event.getSource().getBrand();
    PromotionContainerDto<PromotionDto> content = promotionService.findByBrand(brand);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, Optional.of(content));
    PromotionWithSectionContainerDto content1 =
        promotionService.findByBrandGroupedBySections(brand);
    uploadOptional(brand, PATH_TEMPLATE, PROMOTIONS_WITH_SECTIONS_FILE_NAME, Optional.of(content1));

    V2_NATIVE_CATEGORIES.forEach(
        categoryId -> {
          PromotionContainerDto<PromotionV2Dto> v2Content =
              promotionService.findByBrandAndCategories(brand, categoryId);
          uploadOptional(
              brand, V_2_PATH_TEMPLATE + "/" + FILE_NAME, categoryId, Optional.of(v2Content));
          uploadOptional(
              brand, V_3_PATH_TEMPLATE, FILE_NAME + "_" + categoryId, Optional.of(v2Content));
        });
  }
}
