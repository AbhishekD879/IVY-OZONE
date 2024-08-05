package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static java.util.stream.Collectors.toList;

import com.ladbrokescoral.oxygen.cms.api.dto.PromotionContainerDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionV2Dto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionWithSectionContainerDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PublicPromotionSectionDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.entity.PromotionSection;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.mapping.PromotionMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.api.service.PromotionSectionService;
import com.ladbrokescoral.oxygen.cms.api.service.PromotionService;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import com.ladbrokescoral.oxygen.cms.api.service.StructureService;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;
import org.apache.commons.lang3.StringUtils;
import org.bson.types.ObjectId;
import org.springframework.stereotype.Service;

@Service
public class PromotionPublicService {

  private final PromotionService promotionService;
  private final PromotionSectionService sectionService;
  private final StructureService structureService;
  private final SportCategoryRepository sportCategoryRepository;

  private static final String DEFAULT_EXPANDED_AMOUNT = "2";

  public PromotionPublicService(
      PromotionService promotionService,
      StructureService structureService,
      PromotionSectionService sectionService,
      SportCategoryRepository sportCategoryRepository) {
    this.promotionService = promotionService;
    this.structureService = structureService;
    this.sectionService = sectionService;
    this.sportCategoryRepository = sportCategoryRepository;
  }

  public PromotionContainerDto<PromotionDto> findByBrand(String brand) {

    brand = Util.updateBrand(brand);
    PromotionContainerDto<PromotionDto> result = createPromotionContainerDto(brand);

    List<Promotion> promotionCollection = promotionService.findAllByBrandSorted(brand);
    List<PromotionDto> list =
        promotionCollection.stream()
            .map(PromotionMapper.INSTANCE::toDto)
            .collect(Collectors.toList());
    fillWithCategoryId(list, brand);
    result.setPromotions(list);

    return result;
  }

  public PromotionWithSectionContainerDto findByBrandGroupedBySections(String brand) {

    final String updatedBrand = Util.updateBrand(brand);
    PromotionWithSectionContainerDto result = new PromotionWithSectionContainerDto();

    result.setExpandedAmount(getExpandedAmount(brand));

    final List<PromotionSection> sections =
        sectionService.findByBrandWithDefaultSectionSorted(updatedBrand);
    result.setPromotionsBySection(convertToPublicPromotionSections(sections));

    return result;
  }

  private List<PublicPromotionSectionDto> convertToPublicPromotionSections(
      List<PromotionSection> sections) {
    return sections.stream()
        .filter(
            section ->
                (section.getPromotionIds() != null && !section.getPromotionIds().isEmpty())
                    || section.getUnassignedPromotionIds() != null)
        .map(
            s ->
                PublicPromotionSectionDto.builder()
                    .brand(s.getBrand())
                    .name(s.getName())
                    .sortOrder(s.getSortOrder())
                    .promotions(fillWithCategoryId(getPromotionsBySection(s), s.getBrand()))
                    .build())
        .collect(toList());
  }

  public List<PromotionDto> getPromotionsBySection(PromotionSection section) {
    if (section.getUnassignedPromotionIds() != null) {
      return promotionService.findByIds(section.getBrand(), section.getUnassignedPromotionIds())
          .stream()
          .map(PromotionMapper.INSTANCE::toDto)
          .collect(toList());
    } else {
      return promotionService
          .findByPromotionIdsSorted(
              section.getBrand(), Arrays.asList(section.getPromotionIds().split(",")))
          .stream()
          .map(PromotionMapper.INSTANCE::toDto)
          .collect(toList());
    }
  }

  public PromotionContainerDto<PromotionV2Dto> findByBrandAndCategories(
      String brand, String categories) {

    brand = Util.updateBrand(brand);
    PromotionContainerDto<PromotionV2Dto> result = createPromotionContainerDto(brand);

    Collection<Promotion> promotionCollection =
        promotionService.findAllByBrandSortedAndCategoryIds(brand, getSportCategoryIds(categories));
    List<PromotionV2Dto> list =
        promotionCollection.stream().map(PromotionMapper.INSTANCE::toDtoV2).collect(toList());
    result.setPromotions(list);

    return result;
  }

  public PromotionContainerDto<PromotionV2Dto> findByBrandAndCompetitions(
      String brand, String competitionId) {
    brand = Util.updateBrand(brand);
    PromotionContainerDto<PromotionV2Dto> result = createPromotionContainerDto(brand);
    Collection<Promotion> promotionCollection =
        promotionService.findAllByBrandSortedAndCompetitionId(brand, competitionId);
    List<PromotionV2Dto> list =
        promotionCollection.stream().map(PromotionMapper.INSTANCE::toDtoV2).collect(toList());
    result.setPromotions(list);
    return result;
  }

  private <T> PromotionContainerDto<T> createPromotionContainerDto(String brand) {
    PromotionContainerDto<T> result = new PromotionContainerDto<>();

    result.setExpandedAmount(getExpandedAmount(brand));
    return result;
  }

  private String getExpandedAmount(String brand) {
    return structureService
        .findByBrandAndConfigName(brand, "Promotions")
        .flatMap(promotionsMap -> Optional.ofNullable(promotionsMap.get("expandedAmount")))
        .map(Object::toString)
        .orElse(DEFAULT_EXPANDED_AMOUNT);
  }

  private List<ObjectId> getSportCategoryIds(String categories) {
    List<Integer> ids =
        Arrays.stream(categories.split("\\s*,\\s*")).map(Integer::valueOf).collect(toList());
    return sportCategoryRepository.findAllByMatchingCategoryIds(ids).stream()
        .map(sC -> new ObjectId(sC.getId()))
        .collect(toList());
  }

  private List<PromotionDto> fillWithCategoryId(List<PromotionDto> promotions, String brand) {
    Map<String, String> categories =
        sportCategoryRepository.findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC).stream()
            .collect(
                Collectors.toMap(
                    SportCategory::getId, entity -> String.valueOf(entity.getCategoryId())));
    promotions.forEach(
        (PromotionDto promotion) -> {
          List<String> ids =
              promotion.getCategoryId().stream()
                  .map(categories::get)
                  .filter(StringUtils::isNotBlank)
                  .collect(toList());
          promotion.setCategoryId(ids);
        });
    return promotions;
  }
}
