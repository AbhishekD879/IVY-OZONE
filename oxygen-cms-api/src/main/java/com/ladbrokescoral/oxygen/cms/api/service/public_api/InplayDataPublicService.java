package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.toList;

import com.ladbrokescoral.oxygen.cms.api.dto.InplayDataDto;
import com.ladbrokescoral.oxygen.cms.api.dto.InplaySportCategoryDto;
import com.ladbrokescoral.oxygen.cms.api.dto.VirtualSportDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import com.ladbrokescoral.oxygen.cms.api.mapping.InplaySportCategoryMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportRepository;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class InplayDataPublicService {

  private final SportCategoryRepository sportCategoryRepository;
  private final SportRepository sportRepository;
  private static final Integer HR_CATEGORY_ID = 21;
  private final VirtualSportPublicService virtualSportPublicService;

  // get only tier 1 & tier 2 & HR categories, & also, as an exception - All Sports (categoryId "0")
  private static Predicate<SportCategory> CATEGORY_FILTER =
      sportCategory ->
          (Objects.nonNull(sportCategory.getTier())
                  && Objects.nonNull(sportCategory.getCategoryId())
                  && (sportCategory.getTier().equals(SportTier.TIER_1)
                      || sportCategory.getTier().equals(SportTier.TIER_2)
                      || sportCategory.getSsCategoryCode().equalsIgnoreCase("ALL_SPORTS")))
              || (HR_CATEGORY_ID.equals(sportCategory.getCategoryId()));

  /**
   * sports don`t have tier info (& it`s legacy structure used only for Olympic Sports), only
   * sportcategories We should work only with TIER 1 & TIER 2 sports/sportcategories given that we
   * have to have to: provide only tier 1/2 & non disabled & showInPlay sportCategories
   *
   * @param brand
   * @return
   */
  public InplayDataDto getInplayData(String brand) {
    List<InplaySportCategoryDto> categoryDtos =
        sportCategoryRepository.findAllByBrandOrderBySortOrderAsc(brand).stream()
            .filter(CATEGORY_FILTER)
            .map(InplaySportCategoryMapper.INSTANCE::categoryToInplay)
            .collect(toList());

    List<InplaySportCategoryDto> sportDtos =
        sportRepository.findAllByBrandOrderBySortOrderAsc(brand).stream()
            .map(InplaySportCategoryMapper.INSTANCE::sportToInplay)
            .collect(toList());

    Map<Boolean, List<InplaySportCategoryDto>> isSportCategoryEnabledMap =
        categoryDtos.stream()
            .collect(groupingBy(category -> !category.isDisabled() && category.isShowInPlay()));

    List<InplaySportCategoryDto> enabledSportCategories =
        isSportCategoryEnabledMap.getOrDefault(Boolean.TRUE, Collections.emptyList());
    List<VirtualSportDto> virtualSportDtoList =
        virtualSportPublicService.findActiveSportsWithActiveTracksOnly(brand);
    InplayDataDto dataListDto = new InplayDataDto();
    dataListDto.setActiveSportCategories(enabledSportCategories);
    dataListDto.setSportMap(getMergeMap(categoryDtos, sportDtos));
    dataListDto.setVirtualSports(virtualSportDtoList);
    return dataListDto;
  }

  // prepare grouped map of both sports & sportCategories
  private Map<Integer, InplaySportCategoryDto> getMergeMap(
      List<InplaySportCategoryDto> categoryDtos, List<InplaySportCategoryDto> sportDtos) {
    Map<Integer, InplaySportCategoryDto> sportCategoriesMap =
        categoryDtos.stream()
            .collect(
                Collectors.toMap(
                    InplaySportCategoryDto::getCategoryId, Function.identity(), (a, b) -> a));
    // map catId -> sport
    Map<Integer, InplaySportCategoryDto> sportsMap =
        sportDtos.stream()
            .collect(
                Collectors.toMap(
                    InplaySportCategoryDto::getCategoryId, Function.identity(), (a, b) -> a));

    Map<Integer, InplaySportCategoryDto> mergedMap = new HashMap<>();
    mergedMap.putAll(sportsMap);
    // olympic sports are less prioritized
    mergedMap.putAll(sportCategoriesMap);

    mergedMap
        .entrySet()
        .forEach(
            entry -> {
              InplaySportCategoryDto sport = sportsMap.get(entry.getKey());
              if (Objects.nonNull(sport)) {
                if (Objects.nonNull(sport.getImageTitle())) {
                  String categoryPath = sport.getImageTitle().toLowerCase().replace(" ", "");
                  entry.getValue().setCategoryPath(categoryPath);
                }
              }
            });
    return mergedMap;
  }
}
