package com.ladbrokescoral.oxygen.cms.api.service;

import static com.ladbrokescoral.oxygen.cms.util.Util.isOneOf;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportCategoryArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.SportCategoryArchive;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SportNameDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplaySport;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.IdImageTitlePair;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.HomeInplaySportRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig.ImagePath;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@Component
@Validated
public class SportCategoryService extends AbstractSegmentService<SportCategory> {

  private final SportCategoryRepository sportCategoryRepository;
  private final SportTabService sportTabService;
  private final SportModuleService sportModuleService;
  private final ImageEntityService<SportCategory> imageEntityService;
  private final IconEntityService<SportCategory> iconEntityService;
  private final SvgEntityService<SportCategory> svgEntityService;
  private final SiteServeService siteServeService;
  private final ScheduledTaskExecutor scheduledTaskExecutor;
  private final ImagePath sportCategoryIcon;
  private final ImagePath sportCategoryMenuImagePath;
  private final HomeInplaySportRepository homeInplaySportRepository;
  private ModelMapper modelMapper;

  @Autowired
  public SportCategoryService(
      SportCategoryRepository sportCategoryRepository,
      SportTabService sportTabService,
      SportModuleService sportModuleService,
      ImageEntityService<SportCategory> imageEntityService,
      IconEntityService<SportCategory> iconEntityService,
      SvgEntityService<SportCategory> svgEntityService,
      SiteServeService siteServeService,
      ScheduledTaskExecutor scheduledTaskExecutor,
      ImagePath sportCategoryIcon,
      ImagePath sportCategoryMenuImagePath,
      SportCategoryArchivalRepository sportCategoryArchivalRepository,
      SegmentService segmentService,
      ModelMapper modelMapper,
      HomeInplaySportRepository homeInplaySportRepository) {
    super(sportCategoryRepository, sportCategoryArchivalRepository, segmentService);
    this.sportCategoryRepository = sportCategoryRepository;
    this.sportTabService = sportTabService;
    this.sportModuleService = sportModuleService;
    this.imageEntityService = imageEntityService;
    this.iconEntityService = iconEntityService;
    this.svgEntityService = svgEntityService;
    this.siteServeService = siteServeService;
    this.scheduledTaskExecutor = scheduledTaskExecutor;
    this.sportCategoryIcon = sportCategoryIcon;
    this.sportCategoryMenuImagePath = sportCategoryMenuImagePath;
    this.modelMapper = modelMapper;
    this.homeInplaySportRepository = homeInplaySportRepository;
  }

  @CacheEvict(
      cacheNames = {"sport-categories"},
      key = "#newCategory.id")
  @Override
  public SportCategory save(SportCategory newCategory) {
    boolean isCreateTabsAndModules = Objects.isNull(newCategory.getId());
    SportCategory savedCategory = super.save(newCategory);
    updateHomeInPlaySportName(
        newCategory.getImageTitle(), newCategory.getCategoryId(), newCategory.getBrand());
    if (isCreateTabsAndModules && Objects.nonNull(savedCategory.getCategoryId())) {
      sportTabService.createTabs(savedCategory);
      sportModuleService.renewModules(savedCategory);
    }
    return savedCategory;
  }

  @Cacheable("sport-categories")
  public IdImageTitlePair findIdNamePairById(String id) {
    return sportCategoryRepository.findById(id, IdImageTitlePair.class);
  }

  @CacheEvict(
      cacheNames = {"sport-categories"},
      key = "#newCategory.id")
  @Override
  public SportCategory update(SportCategory existingCategory, SportCategory newCategory) {
    newCategory.setTier(existingCategory.getTier());
    prepareModelBeforeSave(newCategory);
    SportCategory updatedCategory = super.save(newCategory);
    updateHomeInPlaySportName(
        newCategory.getImageTitle(), newCategory.getCategoryId(), newCategory.getBrand());
    if (isCategoryIdChanged(existingCategory, updatedCategory)) {
      if (Objects.isNull(updatedCategory.getCategoryId())) {
        sportTabService.deleteTabs(existingCategory);
      } else if (Objects.isNull(existingCategory.getCategoryId())) {
        sportTabService.createTabs(updatedCategory);
      }
    }
    sportModuleService.renewModules(updatedCategory);
    return updatedCategory;
  }

  private boolean isCategoryIdChanged(SportCategory existingCategory, SportCategory newCategory) {
    return !Objects.equals(existingCategory.getCategoryId(), newCategory.getCategoryId());
  }

  @CacheEvict(
      cacheNames = {"sport-categories"},
      key = "#id")
  @Override
  public void delete(String id) {
    findOne(id)
        .ifPresent(
            (SportCategory category) -> {
              sportCategoryRepository.deleteById(id);
              if (Objects.nonNull(category.getCategoryId())
                  && !existsCategory(category.getBrand(), category.getCategoryId())) {
                sportTabService.deleteTabs(category);
                sportModuleService.deleteBySportId(category.getBrand(), category.getCategoryId());
              }

              SportCategoryArchive sportCategoryArchive = prepareArchivalEntity(category);
              sportCategoryArchive.setDeleted(true);
              super.saveArchivalEntity(sportCategoryArchive);
            });
  }

  private boolean existsCategory(String brand, Integer categoryId) {
    return sportCategoryRepository.existsByBrandAndCategoryId(brand, categoryId);
  }

  @Override
  public SportCategory prepareModelBeforeSave(SportCategory category) {
    validateSportCategory(category);
    if (Objects.nonNull(category.getCategoryId())) {
      boolean hasEvents =
          sportTabService.areThereEventsInCategoryBasedOnSportTabs(category)
              || siteServeService.isCategoryNotValidOrHasEvents(
                  category.getBrand(), category.getCategoryId());
      category.setHasEvents(hasEvents);
    } else if (Objects.isNull(category.getTier())) {
      category.setTier(SportTier.UNTIED);
    }
    return category;
  }

  public List<SportCategory> findAll(String brand, Collection<Integer> categoryIds) {
    return sportCategoryRepository.findAllByMatchingCategoryIds(brand, categoryIds);
  }

  public Optional<SportCategory> findOneByCategoryId(String brand, Integer categoryId) {
    List<SportCategory> sports =
        sportCategoryRepository.findByBrandAndCategoryId(brand, categoryId);
    return sports.isEmpty() ? Optional.empty() : Optional.of(sports.get(0));
  }

  public Optional<SportCategory> attachImage(
      SportCategory menu, @ValidFileType("png") MultipartFile file) {
    return imageEntityService.attachAllSizesImage(
        menu, menu.getImageTitle(), file, sportCategoryMenuImagePath);
  }

  public Optional<SportCategory> attachIcon(
      SportCategory menu, @ValidFileType("png") MultipartFile file) {
    return iconEntityService.attachAllSizesIcon(
        menu, menu.getImageTitle(), file, sportCategoryIcon);
  }

  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public Optional<SportCategory> attachSvgImage(
      SportCategory menu, @ValidFileType("svg") MultipartFile file) {
    return svgEntityService.attachSvgImage(menu, file, sportCategoryMenuImagePath.getSvgMenuPath());
  }

  public Optional<SportCategory> removeImage(SportCategory menu) {
    return imageEntityService.removeAllSizesImage(menu);
  }

  public Optional<SportCategory> removeIcon(SportCategory menu) {
    return iconEntityService.removeAllSizesIcon(menu);
  }

  /**
   * @deprecated use SvgImages api to remove images and use update the menu endpoint to set the
   *     svgId to null delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public Optional<SportCategory> removeSvgImage(SportCategory menu) {
    return svgEntityService.removeSvgImage(menu);
  }

  @Scheduled(cron = "${sportCategory.updateHasEventsField.cron}")
  public void updateHasEventsField() {
    scheduledTaskExecutor.execute(
        () ->
            sportCategoryRepository.findAllByDisabledFalse().forEach(this::updateCategorySilently));
  }

  private void updateCategorySilently(SportCategory category) {
    try {
      boolean value =
          sportTabService.areThereEventsInCategoryBasedOnSportTabs(category)
              || siteServeService.isCategoryNotValidOrHasEvents(
                  category.getBrand(), category.getCategoryId());
      if (category.isHasEvents() != value) {
        category.setHasEvents(value);
        sportCategoryRepository.save(category);
      }
    } catch (Exception e) {
      log.error(
          "Failed to check category {} for brand {}",
          category.getCategoryId(),
          category.getBrand(),
          e);
    }
  }

  private void validateSportCategory(SportCategory category) {
    if (Objects.nonNull(category.getTargetUri())
        && category.getTargetUri().contains("politics/outright")
        && Objects.nonNull(category.getSsCategoryCode())
        && category.getSsCategoryCode().contains("POLITICS")) {
      throw new ValidationException(
          "Category POLITICS could not contain target URI politics/outright");
    }

    if (Objects.isNull(category.getCategoryId())
        && !isOneOf(category.getTier(), SportTier.TIER_1, SportTier.TIER_2)) {
      // it should be possible to create Untied sport with categoryId=null
      return;
    }

    List<SportCategory> withSameCategoryId =
        sportCategoryRepository.findByBrandAndCategoryId(
            category.getBrand(), category.getCategoryId());
    if (withSameCategoryId.size() > 1
        || (withSameCategoryId.size() == 1
            && !withSameCategoryId.get(0).getId().equalsIgnoreCase(category.getId()))) {
      throw new ValidationException(
          "Another Sport Category with the categoryId already created. Please remove invalid one");
    }
  }

  @Override
  public <S extends SportCategory> S prepareArchivalEntity(SportCategory entity) {
    return (S) modelMapper.map(entity, SportCategoryArchive.class);
  }

  @Override
  public List<SportCategory> findByBrandAndSegmentName(String brand, String segmentName) {

    List<SportCategory> records = new ArrayList<>();

    if (SegmentConstants.UNIVERSAL.equalsIgnoreCase(segmentName)) {

      records.addAll(getUniversalRecords(brand));
    } else {
      records.addAll(getSegmentAndUniversal(brand, segmentName));
    }

    return records.stream().map(this::enhanceEntity).collect(Collectors.toList());
  }

  private List<SportCategory> getUniversalRecords(String brand) {
    List<SportCategory> universalList =
        sportCategoryRepository.findUniversalRecordsByBrand(
            brand, SortableService.SORT_BY_SORT_ORDER_ASC);

    return sortUniversalRecords(universalList);
  }

  private List<SportCategory> getSegmentAndUniversal(String brand, String segmentName) {

    List<SportCategory> recordsWithSegmentReference =
        super.sortByOrder(
            segmentName,
            sportCategoryRepository.findAllByBrandAndSegmentName(
                brand, Arrays.asList(segmentName)));

    isUniversalSegmentChanged(recordsWithSegmentReference, segmentName);
    // recordsWithSegmentReference
    // find universal.. ones...
    //
    List<String> idsFromSegmentReferences =
        recordsWithSegmentReference.stream().map(SportCategory::getId).collect(Collectors.toList());

    List<SportCategory> universalList =
        sportCategoryRepository
            .findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
                brand,
                Arrays.asList(segmentName),
                idsFromSegmentReferences,
                SortableService.SORT_BY_SORT_ORDER_ASC);

    universalList = sortUniversalRecords(universalList);

    recordsWithSegmentReference.addAll(universalList);
    return recordsWithSegmentReference;
  }

  private List<SportCategory> sortUniversalRecords(List<SportCategory> universalList) {

    List<SportCategory> segmentReferencesSortOrderRecords =
        universalList
            .parallelStream()
            .filter(
                x ->
                    (!CollectionUtils.isEmpty(x.getSegmentReferences()))
                        && isUniversalSortOrderExsists(x))
            .collect(Collectors.toList());

    List<String> segmentRefIds =
        segmentReferencesSortOrderRecords
            .parallelStream()
            .map(SportCategory::getId)
            .collect(Collectors.toList());

    List<SportCategory> segmentReferencesNOSortOrderRecords =
        universalList
            .parallelStream()
            .filter(segmentRef -> !segmentRefIds.contains(segmentRef.getId()))
            .collect(Collectors.toList());

    segmentReferencesSortOrderRecords =
        sortByOrder(SegmentConstants.UNIVERSAL, segmentReferencesSortOrderRecords);

    segmentReferencesNOSortOrderRecords =
        segmentReferencesNOSortOrderRecords.stream()
            .sorted(SegmentConstants.SPORT_CAT_UNIV_DEFAULT_SORT_ORDER)
            .collect(Collectors.toList());

    segmentReferencesSortOrderRecords.addAll(segmentReferencesNOSortOrderRecords);
    return segmentReferencesSortOrderRecords;
  }

  private static boolean isUniversalSortOrderExsists(SportCategory x) {
    return x.getSegmentReferences().stream()
        .anyMatch(
            ref ->
                SegmentConstants.UNIVERSAL.equalsIgnoreCase(ref.getSegmentName())
                    && ref.getSortOrder() >= 0);
  }

  @Override
  public void dragAndDropOrder(OrderDto newOrder) {
    if (!StringUtils.hasText(newOrder.getSegmentName())) {
      super.dragAndDropOrder(newOrder);
    } else {
      segmentedDragAndDropOrder(newOrder);
    }
  }

  public List<SportNameDto> readSportNameByBrand(String brand) {
    List<SportCategory> categories =
        sportCategoryRepository.findByBrandAndCategoryIdNotNullAndIsActiveAndInTier(brand);
    List<String> sportcategories =
        homeInplaySportRepository.findByBrand(brand).stream()
            .parallel()
            .filter(
                inplay ->
                    inplay.isUniversalSegment()
                        || !CollectionUtils.isEmpty(inplay.getInclusionList()))
            .map(HomeInplaySport::getCategoryId)
            .collect(Collectors.toList());
    return categories.stream()
        .filter(
            category ->
                category.getCategoryId() != null
                    && !sportcategories.contains(String.valueOf(category.getCategoryId())))
        .map(
            category ->
                SportNameDto.builder()
                    .categoryId(category.getCategoryId())
                    .sportName(category.getImageTitle())
                    .sportTier(category.getTier().toString())
                    .build())
        .sorted(Comparator.comparing(SportNameDto::getSportName))
        .collect(Collectors.toList());
  }

  private void updateHomeInPlaySportName(String sportName, Integer categoryId, String brand) {
    String catId = Objects.isNull(categoryId) ? null : String.valueOf(categoryId);

    List<HomeInplaySport> inplaysSports =
        homeInplaySportRepository.findByCategoryIdAndBrand(String.valueOf(catId), brand);
    inplaysSports =
        inplaysSports.stream()
            .filter(inplaySport -> !inplaySport.getSportName().equals(sportName))
            .map(inplay -> updateSportName(sportName, inplay))
            .collect(Collectors.toList());
    homeInplaySportRepository.saveAll(inplaysSports);
  }

  private HomeInplaySport updateSportName(String sportName, HomeInplaySport sport) {
    sport.setSportName(sportName);
    return sport;
  }

  public List<SportCategory> findSportCategoryByBrandAndImageTitle(
      String brand, String imageTitle) {
    return sportCategoryRepository.findByBrandAndImageTitle(brand, imageTitle);
  }
}
