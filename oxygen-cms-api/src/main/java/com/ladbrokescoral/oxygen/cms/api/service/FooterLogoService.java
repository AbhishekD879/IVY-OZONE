package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterLogo;
import com.ladbrokescoral.oxygen.cms.api.repository.FooterLogoRepository;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@Component
@Validated
public class FooterLogoService extends SortableService<FooterLogo> {

  private final FooterLogoRepository footerLogoRepository;
  private final ImageService imageService;
  private final SvgEntityService<FooterLogo> svgEntityService;

  private final String mediumMenusPath;
  private final String originalMenusPath;
  private final String svgMenuPath;

  @Autowired
  public FooterLogoService(
      FooterLogoRepository footerLogoRepository,
      ImageService imageService,
      SvgEntityService<FooterLogo> svgEntityService,
      @Value("${images.footerlogos.medium}") String mediumMenusPath,
      @Value("${images.footerlogos.original}") String originalMenusPath,
      @Value("${images.footerlogos.svg}") String svgMenuPath) {
    super(footerLogoRepository);
    this.footerLogoRepository = footerLogoRepository;
    this.imageService = imageService;
    this.svgEntityService = svgEntityService;

    this.mediumMenusPath = mediumMenusPath;
    this.originalMenusPath = originalMenusPath;
    this.svgMenuPath = svgMenuPath;
  }

  public List<FooterLogo> findAllByBrandAndDisabled(String brand) {
    return footerLogoRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE);
  }

  public Optional<FooterLogo> attachImage(
      FooterLogo menu, @ValidFileType("png") MultipartFile file) {
    Optional<Filename> mediumSized =
        imageService.upload(menu.getBrand(), file, mediumMenusPath, null);
    Optional<Filename> original =
        imageService.upload(menu.getBrand(), file, originalMenusPath, null);

    if (!mediumSized.isPresent() || !original.isPresent()) {
      log.error(
          "Issue with uploading image, uploading successful for : medium - {}, original - {}",
          mediumSized.isPresent(),
          original.isPresent());
      return Optional.empty();
    }

    mediumSized.ifPresent(
        mediumImage ->
            menu.setUriMedium(PathUtil.normalizedPath(mediumMenusPath, mediumImage.getFilename())));

    original.ifPresent(
        originalImage -> {
          menu.setUriOriginal(
              PathUtil.normalizedPath(originalMenusPath, originalImage.getFilename()));
          menu.setFilename(originalImage);
        });

    return Optional.of(menu);
  }

  public Optional<FooterLogo> removeImage(FooterLogo menu) {
    removeMediumImage(menu);
    removeOriginalImage(menu);

    return Optional.of(menu);
  }

  private void removeMediumImage(FooterLogo menu) {
    Optional.ofNullable(menu.getUriMedium())
        .ifPresent(
            uriMedium -> {
              Boolean isDeleted = imageService.removeImage(menu.getBrand(), uriMedium);
              log.info("File {} removal status : {}", uriMedium, isDeleted);
              menu.setUriMedium(null);
            });
  }

  private void removeOriginalImage(FooterLogo menu) {
    Optional.ofNullable(menu.getUriOriginal())
        .ifPresent(
            uriOriginal -> {
              Boolean isDeleted = imageService.removeImage(menu.getBrand(), uriOriginal);
              log.info("File {} removal status : {}", uriOriginal, isDeleted);
              menu.setUriOriginal(null);
              menu.setFilename(null);
            });
  }

  /**
   * @deprecated use SvgImages api to create new images and use update the menu endpoint to set the
   *     svg Id delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public Optional<FooterLogo> attachSvgImage(
      FooterLogo menu, @ValidFileType("svg") MultipartFile file) {
    return svgEntityService.attachSvgImage(menu, file, svgMenuPath);
  }

  /**
   * @deprecated use SvgImages api to delete images and use update the menu endpoint to set the
   *     svgId to null delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated
  public Optional<FooterLogo> removeSvgImage(FooterLogo menu) {
    return svgEntityService.removeSvgImage(menu);
  }
}
