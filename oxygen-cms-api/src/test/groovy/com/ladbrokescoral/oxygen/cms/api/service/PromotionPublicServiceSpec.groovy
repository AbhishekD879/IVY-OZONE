package com.ladbrokescoral.oxygen.cms.api.service

import com.ladbrokescoral.oxygen.cms.api.dto.PromotionContainerDto
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionDto
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository
import com.ladbrokescoral.oxygen.cms.api.service.public_api.PromotionPublicService
import org.bson.types.ObjectId
import org.springframework.data.domain.Sort
import spock.lang.Specification

class PromotionPublicServiceSpec extends Specification {
  PromotionPublicService promotionPublicService
  PromotionService promotionService;
  StructureService structureService;
  SportCategoryRepository sportCategoryRepository;
  PromotionSectionService promotionSectionService;

  def setup() {
    promotionService = Mock(PromotionService)
    structureService = Mock(StructureService)
    promotionSectionService = Mock(PromotionSectionService)
    sportCategoryRepository = Mock(SportCategoryRepository)
    promotionPublicService = new PromotionPublicService(promotionService, structureService,
        promotionSectionService, sportCategoryRepository)
  }

  def "test fill promotions with categoryId array"() {
    given:
    structureService.findByBrandAndConfigName("bma", "Promotions") >> Optional.of(new HashMap<String, Object>())

    Promotion promotion = new Promotion()
    promotion.setCategoryId(Collections.singletonList(new ObjectId("599d4892cc01f90006c0f3f5")))
    promotionService.findAllByBrandSorted("bma") >> Collections.singletonList(promotion)

    SportCategory sportCategory = new SportCategory()
    sportCategory.setCategoryId(12)
    sportCategory.setId("599d4892cc01f90006c0f3f5")
    sportCategoryRepository.findByBrand("bma", Sort.by("sortOrder")) >> Collections.singletonList(sportCategory)

    when:
    PromotionContainerDto result = promotionPublicService.findByBrand("bma")

    then:
    result.getPromotions().size() == 1
    List<PromotionDto> promotions = result.getPromotions()
    PromotionDto promo = (PromotionDto) promotions.get(0)
    promo.getCategoryId().get(0) == "12"
  }
}
