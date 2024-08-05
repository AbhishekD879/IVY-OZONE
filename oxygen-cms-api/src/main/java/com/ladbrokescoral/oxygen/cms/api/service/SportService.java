package com.ladbrokescoral.oxygen.cms.api.service;

import static com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProviderImpl.DEFAULT_BRAND;

import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Type;
import com.fortify.annotations.FortifyXSSValidate;
import com.ladbrokescoral.oxygen.cms.api.entity.Sport;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.SportRepository;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.multipart.MultipartFile;

// Olympic sports
@Slf4j
@Component
@Validated
public class SportService extends SortableService<Sport> {
  private static final String DEFAULT_LANG = "en";

  private final SportRepository sportRepository;
  private final SiteServeApiProvider siteServeApiProvider;
  private final SportsImageUploadComponent sportsImageUploadComponent;

  public SportService(
      SportRepository sportRepository,
      SiteServeApiProvider siteServeApiProvider,
      SportsImageUploadComponent sportsImageUploadComponent) {
    super(sportRepository);
    this.sportRepository = sportRepository;
    this.siteServeApiProvider = siteServeApiProvider;
    this.sportsImageUploadComponent = sportsImageUploadComponent;
  }

  @Override
  public Sport save(Sport entity) {
    setDefaultValuesOnSportCreation(entity);
    validateCategoryAndTypeIds(entity);
    return sportRepository.save(entity);
  }

  private void setDefaultValuesOnSportCreation(Sport entity) {
    if (entity.getLang() == null) {
      entity.setLang(DEFAULT_LANG);
    }

    sportsImageUploadComponent.setDefaultImageSizes(entity);

    entity.clearAllImages();

    entity.setSpriteClass(
        entity.getBrand().equalsIgnoreCase(DEFAULT_BRAND)
            ? entity.getImageTitle()
            : entity.getBrand().concat("_").concat(entity.getImageTitle()));

    if (entity.getSortOrder() != null) {
      incrementSortOrder(entity);
    }
  }

  /** Checks if: - provided type ids are in specified category id - provided type ids exist */
  private void validateCategoryAndTypeIds(Sport entity) {
    Integer categoryId = entity.getCategoryId();
    String typeIds = entity.getTypeIds();

    List<String> inputTypeIds =
        Arrays.stream(typeIds.split(","))
            .filter(id -> !StringUtils.isBlank(id))
            .map(String::trim)
            .collect(Collectors.toList());

    List<Category> classes = getCategoriesFromSiteServe(entity, inputTypeIds);

    Set<String> types =
        classes.stream()
            .flatMap(category -> category.getTypes().stream())
            .map(Type::getId)
            .map(String::valueOf)
            .collect(Collectors.toSet());

    Set<String> categories =
        classes.stream().map(Category::getCategoryCode).collect(Collectors.toSet());

    if (categories.size() >= 2) {
      throw new ValidationException(
          String.format("Type ids: %s are from more than one category", inputTypeIds));
    } else if (categories.size() == 1) {
      Category ssClass = classes.get(0);
      if (!ssClass.getCategoryId().equals(categoryId)) {
        throw new ValidationException(
            String.format(
                "Type ids: %s are not from category with id=%s", inputTypeIds, categoryId));
      }

      List<String> notExistingIds =
          inputTypeIds.stream().filter(id -> !types.contains(id)).collect(Collectors.toList());

      if (!notExistingIds.isEmpty()) {
        throw new ValidationException(String.format("Type ids: %s do not exist", notExistingIds));
      }

      // if validation is passed, set category code
      entity.setSsCategoryCode(ssClass.getCategoryCode());
    } else {
      throw new ValidationException(String.format("Type ids: %s do not exist", inputTypeIds));
    }
  }

  private List<Category> getCategoriesFromSiteServe(Sport entity, List<String> inputTypeIds) {
    try {
      return siteServeApiProvider
          .api(entity.getBrand())
          .getClassToSubTypeForType(inputTypeIds, Collections::emptyList)
          .orElse(Collections.emptyList());
    } catch (Exception e) {
      log.error("Failed to find categories {} in SiteServer", inputTypeIds, e);
      return Collections.emptyList();
    }
  }

  @Override
  public Sport update(Sport existingEntity, Sport updatedEntity) {
    boolean categoryOrTypeIdsChanged =
        !existingEntity.getCategoryId().equals(updatedEntity.getCategoryId())
            || !existingEntity.getTypeIds().equals(updatedEntity.getTypeIds());

    if (categoryOrTypeIdsChanged) {
      validateCategoryAndTypeIds(updatedEntity);
    }

    // don't update fields that are populated during images update
    updatedEntity.setFilename(existingEntity.getFilename());
    updatedEntity.setSvgFilename(existingEntity.getSvgFilename());
    updatedEntity.setSvg(existingEntity.getSvg());
    updatedEntity.setUriLargeIcon(existingEntity.getUriLargeIcon());
    updatedEntity.setUriLarge(existingEntity.getUriLarge());
    updatedEntity.setUriMediumIcon(existingEntity.getUriMediumIcon());
    updatedEntity.setUriMedium(existingEntity.getUriMedium());
    updatedEntity.setUriSmallIcon(existingEntity.getUriSmallIcon());
    updatedEntity.setUriSmall(existingEntity.getUriSmall());

    return sportRepository.save(updatedEntity);
  }

  @Override
  public List<Sport> findAll() {
    return sportRepository.findAll(SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  @Override
  public List<Sport> findByBrand(String brand) {
    return sportRepository.findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  @Override
  public void delete(String id) {
    this.deleteUploadedFiles(id, SportsImageUploadComponent.SportsImage.validValues());
    sportRepository.deleteById(id);
  }

  @Override
  protected boolean isNewElementCreatedFirstInTheList() {
    return false;
  }

  public List<Sport> findAllByBrandSorted(String brand) {
    return sportRepository.findAllByBrandOrderBySortOrderAsc(brand);
  }

  @FortifyXSSValidate("return")
  public List<Sport> findAllBySportNameAndBrand(String sportName, String brand) {
    boolean sportNameIsProvided = !StringUtils.isBlank(sportName);
    boolean brandIsProvided = !StringUtils.isBlank(brand);

    if (sportNameIsProvided && brandIsProvided) {
      return sportRepository
          .findByImageTitleContainingIgnoreCaseAndBrandIgnoreCaseOrderBySortOrderAsc(
              sportName, brand);
    } else if (sportNameIsProvided) {
      return sportRepository.findByImageTitleContainingIgnoreCaseOrderBySortOrderAsc(sportName);
    } else if (brandIsProvided) {
      return findByBrand(brand);
    } else {
      return findAll();
    }
  }

  public Optional<Sport> handleUploadedFiles(
      String sportId,
      @ValidFileType("png") MultipartFile imageFile,
      @ValidFileType("png") MultipartFile icon,
      @ValidFileType("svg") MultipartFile svgIcon) {
    return this.findOne(sportId)
        .map(
            sport ->
                sportRepository.save(
                    sportsImageUploadComponent.attachImages(sport, imageFile, icon, svgIcon)));
  }

  public Optional<Sport> deleteUploadedFiles(String id, String[] fileTypes) {
    SportsImageUploadComponent.SportsImage[] sportsImages =
        new SportsImageUploadComponent.SportsImage[fileTypes.length];
    for (int i = 0; i < fileTypes.length; i++) {
      String fileType = fileTypes[i];
      SportsImageUploadComponent.SportsImage sportsImage =
          SportsImageUploadComponent.SportsImage.fromString(fileType);
      if (sportsImage == SportsImageUploadComponent.SportsImage.UNKNOWN) {
        throw new ValidationException("Unknown fileType: " + fileType);
      }

      sportsImages[i] = sportsImage;
    }
    return deleteUploadedFiles(id, sportsImages);
  }

  private Optional<Sport> deleteUploadedFiles(
      String id, SportsImageUploadComponent.SportsImage[] fileTypes) {
    return findOne(id)
        .map(
            sport -> {
              sportsImageUploadComponent.deleteImages(fileTypes, sport);
              return sportRepository.save(sport);
            });
  }
}
