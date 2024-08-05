package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.*;
import com.ladbrokescoral.oxygen.cms.api.entity.InplayStatsConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.mapping.InplayStatsDisplayMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.InplayStatsSortingMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.SportCategoryMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportTabRepository;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabNames;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class SportCategoryPublicService implements ApiService<SportCategoryDto> {

  private static final Comparator<SportTabConfigDto> SORT_ORDER_COMPARATOR =
      Comparator.comparing(SportTabConfigDto::isHidden)
          .reversed() // hidden first
          .thenComparing(
              SportTabConfigDto::getSortOrder, Comparator.nullsFirst(Comparator.naturalOrder()));

  private final SportCategoryRepository categoryRepository;
  private final SportTabRepository tabRepository;
  private final SegmentService segmentService;

  private final InplayStatsDisplayService statsDisplayService;

  private final InplayStatsSortingService statsSortingService;

  public SportCategoryPublicService(
      SportCategoryRepository categoryRepository,
      SportTabRepository tabRepository,
      SegmentService segmentService,
      InplayStatsDisplayService statsDisplayService,
      InplayStatsSortingService statsSortingService) {
    this.categoryRepository = categoryRepository;
    this.tabRepository = tabRepository;
    this.segmentService = segmentService;
    this.statsDisplayService = statsDisplayService;
    this.statsSortingService = statsSortingService;
  }

  public List<SportCategoryDto> findByBrand(String brand) {
    return findAndMap(brand, SportCategoryMapper.INSTANCE::toDto);
  }

  public List<SportCategoryNativeDto> findNative(String brand) {
    return findAndMap(brand, SportCategoryMapper.INSTANCE::toDtoNative);
  }

  private <T> List<T> findAndMap(String brand, Function<SportCategory, T> dtoMapper) {

    List<SportCategory> sportCategories =
        categoryRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE);
    sportCategories = SportCategorySortHelper.sortUniversalRecords(sportCategories);
    return sportCategories.stream().map(dtoMapper).collect(Collectors.toList());
  }

  public SportTabConfigListDto getSportTabs(String brand, Integer categoryId) {
    SportCategory sport =
        categoryRepository.findByBrandAndCategoryId(brand, categoryId).stream()
            .findFirst()
            .orElseThrow(NotFoundException::new);

    SportTabConfigListDto.Builder tabConfigsBuilder =
        SportTabConfigListDto.builder(sport.getTargetUri());
    tabRepository.findAllByBrandAndSportId(brand, categoryId).forEach(tabConfigsBuilder::addTab);
    SportTabConfigListDto sportTabs = tabConfigsBuilder.build();
    sportTabs.getTabs().sort(SORT_ORDER_COMPARATOR);
    return sportTabs;
  }

  public SportPageConfigDto getSportConfig(String brand, Integer categoryId) {
    SportCategory sport =
        categoryRepository.findByBrandAndCategoryId(brand, categoryId).stream()
            .findFirst()
            .orElseThrow(NotFoundException::new);

    SportPageConfigDto.TabBuilder configBuilder = SportPageConfigDto.builder().config(sport);
    tabRepository
        .findAllByBrandAndSportId(brand, categoryId)
        .forEach(
            tab -> {
              configBuilder.addTab(tab);
              if (SportTabNames.MATCHES.nameLowerCase().equals(tab.getName())) {
                configBuilder.addSubTab("today").addSubTab("tomorrow").addSubTab("future");
              }
            });
    SportPageConfigDto configDto = configBuilder.build();
    configDto.getTabs().sort(SORT_ORDER_COMPARATOR);
    return configDto;
  }

  public List<SportPageConfigDto> getSportsConfigs(String brand, List<Integer> categoryIds) {
    return categoryIds
        .parallelStream()
        .map(
            categoryId -> {
              try {
                return this.getSportConfig(brand, categoryId);
              } catch (NotFoundException e) {
                return null;
              }
            })
        .filter(Objects::nonNull)
        .collect(Collectors.toList());
  }

  public List<InitialDataSportCategoryDto> findInitialData(String brand) {
    return findAndMap(brand, SportCategoryMapper.INSTANCE::toInitialDto);
  }

  public List<InitialDataSportCategorySegmentedDto> findAllActiveByBrand(String brand) {

    List<SportCategory> sportCategories =
        categoryRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE);
    List<String> segments = segmentService.getSegmentsForSegmentedViews(brand);
    sportCategories = SportCategorySortHelper.sortUniversalRecords(sportCategories);
    return sportCategories.stream()
        .map(
            (SportCategory sportCategory) -> {
              InitialDataSportCategorySegmentedDto dto =
                  SportCategoryMapper.INSTANCE.toDto(sportCategory, segments);
              dto.setInplayStatsConfigDto(mapInplaySportConfig(sportCategory, brand));
              return dto;
            })
        .collect(Collectors.toList());
  }

  public List<InitialDataSportCategoryDto> findSportCategoriesInitialData(
      String brand, String segmentName) {

    List<InitialDataSportCategoryDto> initialDataSportCategoryDtos =
        findByBrandAndSegmentName(brand, segmentName).stream()
            .filter(sportCategory -> !sportCategory.isDisabled())
            .map(
                (SportCategory sportCategory) -> {
                  InitialDataSportCategoryDto dto =
                      SportCategoryMapper.INSTANCE.toInitialDto(sportCategory);
                  dto.setInplayStatsConfigDto(mapInplaySportConfig(sportCategory, brand));
                  return dto;
                })
            .collect(Collectors.toList());

    List<String> categoryIds =
        initialDataSportCategoryDtos.stream()
            .parallel()
            .map(InitialDataSportCategoryDto::getId)
            .collect(Collectors.toList());
    List<InitialDataSportCategoryDto> initialDataSportCategoryDtosHomeDisablefalse =
        categoryRepository.findByDisableFalseAndIdNotIn(categoryIds, brand).stream()
            .map(
                (SportCategory sportCategory) -> {
                  InitialDataSportCategoryDto dto =
                      SportCategoryMapper.INSTANCE.toInitialDto(sportCategory);
                  dto.setInplayStatsConfigDto(mapInplaySportConfig(sportCategory, brand));
                  return dto;
                })
            .map(this::setHomePageFalse)
            .collect(Collectors.toList());
    initialDataSportCategoryDtos.addAll(initialDataSportCategoryDtosHomeDisablefalse);
    return initialDataSportCategoryDtos;
  }

  private InplayStatsConfigDto mapInplaySportConfig(SportCategory sportCategory, String brand) {
    InplayStatsConfig config = sportCategory.getInplayStatsConfig();
    if (config != null) {
      List<InplayStatsDisplayDto> statsDisplayDtos =
          this.statsDisplayService.findByBrandAndCategoryId(brand, sportCategory.getCategoryId())
              .stream()
              .map(InplayStatsDisplayMapper.MAPPER::toDto)
              .collect(Collectors.toList());
      List<InplayStatsSortingDto> statsSortingDtos =
          this.statsSortingService.findByBrandAndCategoryId(brand, sportCategory.getCategoryId())
              .stream()
              .map(InplayStatsSortingMapper.MAPPER::toDto)
              .collect(Collectors.toList());
      StatsWidgetDto statsWidgetDto = new StatsWidgetDto();
      statsWidgetDto.setShowStatsWidget(config.isShowStatsWidget());
      statsWidgetDto.setNote(config.getNote());
      StatsDisplayDto statsDisplayDto = new StatsDisplayDto();
      statsDisplayDto.setShowStatsDisplay(config.isShowStatsDisplay());
      statsDisplayDto.setStatsDisplayDtoList(statsDisplayDtos);
      StatsSortingDto statsSortingDto = new StatsSortingDto();
      statsSortingDto.setShowStatsSorting(config.isShowStatsSorting());
      statsSortingDto.setReorderDisplayIn(config.getReorderDisplayIn());
      statsSortingDto.setStatsSortingDtoList(statsSortingDtos);
      return InplayStatsConfigDto.builder()
          .statsWidgetDto(statsWidgetDto)
          .statsDisplayDto(statsDisplayDto)
          .statsSortingDto(statsSortingDto)
          .build();
    }
    return null;
  }

  private InitialDataSportCategoryDto setHomePageFalse(
      InitialDataSportCategoryDto initialDataSportCategoryDto) {

    initialDataSportCategoryDto.setShowInHome(false);
    return initialDataSportCategoryDto;
  }

  private List<SportCategory> findByBrandAndSegmentName(String brand, String segmentName) {

    return SegmentConstants.UNIVERSAL.equalsIgnoreCase(segmentName)
        ? getUniversalRecords(brand)
        : getSegmentAndUniversal(brand, segmentName);
  }

  private List<SportCategory> getUniversalRecords(String brand) {
    List<SportCategory> universalList =
        categoryRepository.findUniversalRecordsByBrand(
            brand, SortableService.SORT_BY_SORT_ORDER_ASC);

    return SportCategorySortHelper.sortUniversalRecords(universalList);
  }

  private List<SportCategory> getSegmentAndUniversal(String brand, String segmentName) {

    List<SportCategory> recordsWithSegmentReference =
        SportCategorySortHelper.sortByOrder(
            segmentName,
            categoryRepository.findAllByBrandAndSegmentName(brand, Arrays.asList(segmentName)));

    List<String> idsFromSegmentReferences =
        recordsWithSegmentReference.stream().map(SportCategory::getId).collect(Collectors.toList());

    List<SportCategory> universalList =
        categoryRepository
            .findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
                brand,
                Arrays.asList(segmentName),
                idsFromSegmentReferences,
                SortableService.SORT_BY_SORT_ORDER_ASC);

    universalList = SportCategorySortHelper.sortUniversalRecords(universalList);

    recordsWithSegmentReference.addAll(universalList);
    return recordsWithSegmentReference;
  }
}
