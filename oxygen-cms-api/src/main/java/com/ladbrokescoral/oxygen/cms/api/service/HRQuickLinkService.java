package com.ladbrokescoral.oxygen.cms.api.service;

import static com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl.Size;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.HRQuickLink;
import com.ladbrokescoral.oxygen.cms.api.repository.HRQuickLinkRepository;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import com.ladbrokescoral.oxygen.cms.util.ImageUtil;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
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
public class HRQuickLinkService extends SortableService<HRQuickLink> {

  private final ImageService imageService;

  private final String originalMenusPath;
  private final String mediumMenusPath;
  private final String mediumMenuSize;
  private final Size medium;

  @Autowired
  public HRQuickLinkService(
      HRQuickLinkRepository repository,
      ImageService imageService,
      @Value("${images.hrquicklinks.original.path}") String originalMenusPath,
      @Value("${images.hrquicklinks.medium.path}") String mediumMenusPath,
      @Value("${images.hrquicklinks.medium.size}") String mediumMenuSize) {
    super(repository);
    this.imageService = imageService;

    this.originalMenusPath = originalMenusPath;
    this.mediumMenusPath = mediumMenusPath;
    this.mediumMenuSize = mediumMenuSize;
    medium = new Size(mediumMenuSize);
  }

  public Optional<HRQuickLink> attachImage(
      HRQuickLink menu, @ValidFileType({"jpeg", "png", "jpg"}) MultipartFile file) {
    Optional<Filename> original =
        imageService.upload(menu.getBrand(), file, originalMenusPath, null);
    Optional<Filename> mediumSized =
        imageService.upload(menu.getBrand(), file, mediumMenusPath, medium);

    if (!mediumSized.isPresent() || !original.isPresent()) {
      log.error(
          "Issue with uploading image, uploading successful for : medium - {}, original - {}",
          mediumSized.isPresent(),
          original.isPresent());
      return Optional.empty();
    }

    original.ifPresent(menu::setFilename);

    mediumSized.ifPresent(
        mediumImage ->
            ImageUtil.populateMediumFields(
                menu, medium, PathUtil.normalizedPath(mediumMenusPath, mediumImage.getFilename())));

    return Optional.of(menu);
  }

  public Optional<HRQuickLink> removeImage(HRQuickLink menu) {
    removeMediumImage(menu);
    removeOriginalImage(menu);

    return Optional.of(menu);
  }

  private void removeMediumImage(HRQuickLink menu) {
    Optional.ofNullable(menu.getUriMedium())
        .ifPresent(
            uriMedium -> {
              Boolean isDeleted = imageService.removeImage(menu.getBrand(), uriMedium);
              log.info("File {} removal status : {}", uriMedium, isDeleted);
              ImageUtil.removeMediumFields(menu);
            });
  }

  private void removeOriginalImage(HRQuickLink menu) {
    Optional.ofNullable(menu.getFilename())
        .ifPresent(
            filename -> {
              String pathToOriginal =
                  PathUtil.normalizedPath(filename.getPath(), filename.getFilename());
              Boolean isDeleted = imageService.removeImage(menu.getBrand(), pathToOriginal);
              log.info("File {} removal status : {}", pathToOriginal, isDeleted);
              menu.setFilename(null);
            });
  }
}
