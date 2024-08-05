package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.IconAbstractMenu;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig.ImagePath;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.util.Objects;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

/**
 * this service provides methods for uploading & removing sets of icons - e.g. small, medium & large
 * altogether
 *
 * @param <T>
 */
@Slf4j
@Service
public class IconEntityService<T extends IconAbstractMenu> {

  private static final String FILE_REMOVAL_STATUS = "File {} removal status : {}";
  private final ImageService imageService;
  private final String corePath;

  public IconEntityService(ImageService imageService, @Value("${images.core}") String corePath) {
    this.imageService = imageService;
    this.corePath = corePath;
  }

  public Optional<T> attachAllSizesIcon(
      T menu, String fileName, MultipartFile file, ImagePath iconDescriptor) {

    boolean fileNameExists = Objects.nonNull(fileName);

    Optional<Filename> original = imageService.upload(menu.getBrand(), file, corePath);
    Optional<Filename> smallSized =
        fileNameExists
            ? imageService.upload(
                menu.getBrand(),
                file,
                iconDescriptor.getSmallPath(),
                fileName,
                iconDescriptor.getSmallSize())
            : imageService.upload(
                menu.getBrand(),
                file,
                iconDescriptor.getSmallPath(),
                iconDescriptor.getSmallSize());

    Optional<Filename> mediumSized =
        fileNameExists
            ? imageService.upload(
                menu.getBrand(),
                file,
                iconDescriptor.getMediumPath(),
                fileName,
                iconDescriptor.getMediumSize())
            : imageService.upload(
                menu.getBrand(),
                file,
                iconDescriptor.getMediumPath(),
                iconDescriptor.getMediumSize());

    Optional<Filename> largeSized =
        fileNameExists
            ? imageService.upload(
                menu.getBrand(),
                file,
                iconDescriptor.getLargePath(),
                fileName,
                iconDescriptor.getLargeSize())
            : imageService.upload(
                menu.getBrand(),
                file,
                iconDescriptor.getLargePath(),
                iconDescriptor.getLargeSize());

    if (!smallSized.isPresent() || !mediumSized.isPresent() || !largeSized.isPresent()) {
      log.error(
          "Issue with uploading resized icon, uploading successful for : small - {}, medium - {}, large - {}",
          smallSized.isPresent(),
          mediumSized.isPresent(),
          largeSized.isPresent());
      return Optional.empty();
    }

    original.ifPresent(menu::setIcon);

    smallSized.ifPresent(
        smallImage -> {
          menu.setHeightSmallIcon(iconDescriptor.getSmallSize().getHeight());
          menu.setWidthSmallIcon(iconDescriptor.getSmallSize().getWidth());
          menu.setUriSmallIcon(
              PathUtil.normalizedPath(iconDescriptor.getSmallPath(), smallImage.getFilename()));
        });

    mediumSized.ifPresent(
        mediumImage -> {
          menu.setHeightMediumIcon(iconDescriptor.getMediumSize().getHeight());
          menu.setWidthMediumIcon(iconDescriptor.getMediumSize().getWidth());
          menu.setUriMediumIcon(
              PathUtil.normalizedPath(iconDescriptor.getMediumPath(), mediumImage.getFilename()));
        });

    largeSized.ifPresent(
        largeImage -> {
          menu.setHeightLargeIcon(iconDescriptor.getLargeSize().getHeight());
          menu.setWidthLargeIcon(iconDescriptor.getLargeSize().getWidth());
          menu.setUriLargeIcon(
              PathUtil.normalizedPath(iconDescriptor.getLargePath(), largeImage.getFilename()));
        });

    return Optional.of(menu);
  }

  public Optional<T> attachAllSizesIcon(T menu, MultipartFile file, ImagePath iconDescriptor) {

    return attachAllSizesIcon(menu, null, file, iconDescriptor);
  }

  public Optional<T> removeAllSizesIcon(T menu) {
    removeSmallIcon(menu);
    removeMediumIcon(menu);
    removeLargeIcon(menu);

    removeOriginal(menu);

    return Optional.of(menu);
  }

  private void removeSmallIcon(T menu) {
    Optional.ofNullable(menu.getUriSmallIcon())
        .ifPresent(
            uriSmall -> {
              Boolean isDeleted = imageService.removeImage(menu.getBrand(), uriSmall);
              log.info(FILE_REMOVAL_STATUS, uriSmall, isDeleted);
              menu.setHeightSmallIcon(null);
              menu.setWidthSmallIcon(null);
              menu.setUriSmallIcon(null);
            });
  }

  private void removeMediumIcon(T menu) {
    Optional.ofNullable(menu.getUriMediumIcon())
        .ifPresent(
            uriMedium -> {
              Boolean isDeleted = imageService.removeImage(menu.getBrand(), uriMedium);
              log.info(FILE_REMOVAL_STATUS, uriMedium, isDeleted);
              menu.setHeightMediumIcon(null);
              menu.setWidthMediumIcon(null);
              menu.setUriMediumIcon(null);
            });
  }

  private void removeLargeIcon(T menu) {
    Optional.ofNullable(menu.getUriLargeIcon())
        .ifPresent(
            uriLarge -> {
              Boolean isDeleted = imageService.removeImage(menu.getBrand(), uriLarge);
              log.info(FILE_REMOVAL_STATUS, uriLarge, isDeleted);
              menu.setHeightLargeIcon(null);
              menu.setWidthLargeIcon(null);
              menu.setUriLargeIcon(null);
            });
  }

  private void removeOriginal(T menu) {
    Optional.ofNullable(menu.getIcon())
        .ifPresent(
            filename -> {
              String pathToOriginal =
                  PathUtil.normalizedPath(filename.getPath(), filename.getFilename());
              Boolean isDeleted = imageService.removeImage(menu.getBrand(), pathToOriginal);
              log.info(FILE_REMOVAL_STATUS, pathToOriginal, isDeleted);
              menu.setIcon(null);
            });
  }
}
