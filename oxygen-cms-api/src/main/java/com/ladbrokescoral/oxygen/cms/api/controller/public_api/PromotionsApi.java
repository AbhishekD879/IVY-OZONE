package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.PromotionContainerDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionV2Dto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionWithSectionContainerDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Patterns;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.PromotionPublicService;
import javax.validation.constraints.Pattern;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@Validated
@RestController
public class PromotionsApi implements Public {

  private final PromotionPublicService promotionService;

  @Autowired
  public PromotionsApi(PromotionPublicService promotionService) {
    this.promotionService = promotionService;
  }

  @GetMapping(value = "{brand}/promotions")
  public PromotionContainerDto<PromotionDto> findByBrand(@PathVariable("brand") String brand) {
    return promotionService.findByBrand(brand);
  }

  @GetMapping(value = "{brand}/grouped-promotions")
  public PromotionWithSectionContainerDto findByBrandAndGroupedBySection(
      @PathVariable("brand") String brand) {
    return promotionService.findByBrandGroupedBySections(brand);
  }

  @GetMapping(value = "v2/{brand}/promotions/{categories}")
  public PromotionContainerDto<PromotionV2Dto> findByBrandAndCategories(
      @PathVariable("brand") String brand,
      @Pattern(
              regexp = Patterns.COMMA_SEPARTED_NUMBERS,
              message = "must be valid comma separated ids")
          @PathVariable("categories")
          String categories) {
    return promotionService.findByBrandAndCategories(brand, categories);
  }

  @GetMapping(value = "{brand}/promotions/{competition}")
  public PromotionContainerDto<PromotionV2Dto> findByBrandAndCompetitions(
      @PathVariable("brand") String brand, @PathVariable("competition") String competition) {
    return promotionService.findByBrandAndCompetitions(brand, competition);
  }
}
