package com.ladbrokescoral.oxygen.cms.api.service;

import com.fortify.annotations.FortifyXSSValidate;
import com.ladbrokescoral.oxygen.cms.api.entity.Banner;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.IdImageTitlePair;
import com.ladbrokescoral.oxygen.cms.api.repository.BannerRepository;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.Collection;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class BannerService extends SortableService<Banner> {

  private final BannerRepository bannerRepository;
  private final SportCategoryService service;

  public BannerService(BannerRepository bannerRepository, SportCategoryService service) {
    super(bannerRepository);
    this.bannerRepository = bannerRepository;
    this.service = service;
  }

  @Override
  public Banner save(Banner entity) {
    Banner savedBanner = bannerRepository.save(entity);
    populateSportCategoryName(Optional.ofNullable(savedBanner));
    return savedBanner;
  }

  @Override
  public Banner update(Banner existingEntity, Banner updateEntity) {
    prepareModelBeforeSave(updateEntity);
    updateEntity.setUriMedium(existingEntity.getUriMedium());
    updateEntity.setUriSmall(existingEntity.getUriSmall());
    updateEntity.setDesktopUriMedium(existingEntity.getDesktopUriMedium());
    updateEntity.setDesktopUriSmall(existingEntity.getDesktopUriSmall());
    updateEntity.setDesktopFilename(existingEntity.getDesktopFilename());
    updateEntity.setDesktopHeightMedium(existingEntity.getDesktopHeightMedium());
    updateEntity.setDesktopHeightSmall(existingEntity.getDesktopHeightSmall());
    updateEntity.setDesktopWidthMedium(existingEntity.getDesktopWidthMedium());
    updateEntity.setDesktopWidthSmall(existingEntity.getDesktopWidthSmall());
    updateEntity.setFilename(existingEntity.getFilename());
    updateEntity.setHeightMedium(existingEntity.getHeightMedium());
    updateEntity.setHeightSmall(existingEntity.getHeightSmall());
    updateEntity.setWidthMedium(existingEntity.getWidthMedium());
    updateEntity.setWidthSmall(existingEntity.getWidthSmall());
    return save(updateEntity);
  }

  @FortifyXSSValidate("return")
  @Override
  public Optional<Banner> findOne(String id) {
    Optional<Banner> banner = bannerRepository.findById(id);
    populateSportCategoryName(banner);
    return banner;
  }

  @Override
  public List<Banner> findAll() {
    List<Banner> banners = bannerRepository.findAll();
    populateSportCategoryNames(banners);
    return banners;
  }

  private void populateSportCategoryName(Optional<Banner> banner) {
    banner
        .filter(b -> Objects.nonNull(b.getCategoryId()))
        .filter(b -> Util.isValidObjectIdString(b.getCategoryId().toString()))
        .ifPresent(
            b -> {
              IdImageTitlePair sportCategory =
                  service.findIdNamePairById(b.getCategoryId().toString());
              if (sportCategory != null) {
                b.setCategoryName(sportCategory.getImageTitle());
              }
            });
  }

  private void populateSportCategoryNames(Collection<Banner> banners) {
    banners.stream()
        .filter(b -> Objects.nonNull(b.getCategoryId()))
        .filter(b -> Util.isValidObjectIdString(b.getCategoryId().toString()))
        .forEach(
            b -> {
              IdImageTitlePair sportCategory =
                  service.findIdNamePairById(b.getCategoryId().toString());
              if (sportCategory != null) {
                b.setCategoryName(sportCategory.getImageTitle());
              }
            });
  }

  @Override
  public List<Banner> findByBrand(String brand) {
    List<Banner> byBrand =
        bannerRepository.findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC);
    populateSportCategoryNames(byBrand);
    return byBrand;
  }

  @Override
  public Banner prepareModelBeforeSave(Banner banner) {
    banner.setVipLevels(generateVipLevels(banner));
    banner.setImageTitleBrand(generateImageTitleBrand(banner));
    return banner;
  }

  private List<Integer> generateVipLevels(Banner banner) {
    if (!StringUtils.isBlank(banner.getVipLevelsInput())) {
      return Util.hyphenatedAndCommaSeparatedNumbersToList(banner.getVipLevelsInput());
    }
    return null;
  }

  private String generateImageTitleBrand(Banner banner) {
    return new StringBuilder(banner.getImageTitle())
        .append("-")
        .append(banner.getBrand())
        .toString()
        .toLowerCase()
        .replace(" ", "-");
  }
}
