package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.ImageAbstractMenu;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig.ImagePath;
import com.ladbrokescoral.oxygen.cms.util.ImageUtil;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.util.Objects;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

/**
 * this service provides methods for uploading & removing sets of images - e.g. small, medium &
 * large altogether
 *
 * @param <T>
 */
@Slf4j
@Service
public class ImageEntityService<T extends ImageAbstractMenu> {

  private static final String FILE_REMOVAL_STATUS = "File {} removal status : {}";
  private final ImageService imageService;
  // core path is typically "images/uploads", and original size files were(?) stored there
  private final String corePath;

  public ImageEntityService(ImageService imageService, @Value("${images.core}") String corePath) {
    this.imageService = imageService;
    this.corePath = corePath;
  }

  public Optional<T> attachAllSizesImage(
      T menu, String fileName, MultipartFile file, ImagePath imgDescriptor) {

    boolean fileNameExists = Objects.nonNull(fileName);

    Optional<Filename> original = imageService.upload(menu.getBrand(), file, corePath);
    Optional<Filename> smallSized =
        fileNameExists
            ? imageService.upload(
                menu.getBrand(),
                file,
                imgDescriptor.getSmallPath(),
                fileName,
                imgDescriptor.getSmallSize())
            : imageService.upload(
                menu.getBrand(), file, imgDescriptor.getSmallPath(), imgDescriptor.getSmallSize());

    Optional<Filename> mediumSized =
        fileNameExists
            ? imageService.upload(
                menu.getBrand(),
                file,
                imgDescriptor.getMediumPath(),
                fileName,
                imgDescriptor.getMediumSize())
            : imageService.upload(
                menu.getBrand(),
                file,
                imgDescriptor.getMediumPath(),
                imgDescriptor.getMediumSize());

    Optional<Filename> largeSized =
        fileNameExists
            ? imageService.upload(
                menu.getBrand(),
                file,
                imgDescriptor.getLargePath(),
                fileName,
                imgDescriptor.getLargeSize())
            : imageService.upload(
                menu.getBrand(), file, imgDescriptor.getLargePath(), imgDescriptor.getLargeSize());

    if (!smallSized.isPresent() || !mediumSized.isPresent() || !largeSized.isPresent()) {
      log.error(
          "Issue with uploading resized image, uploading successful for : small - {}, medium - {}, large - {}",
          smallSized.isPresent(),
          mediumSized.isPresent(),
          largeSized.isPresent());
      return Optional.empty();
    }

    original.ifPresent(menu::setFilename);

    smallSized.ifPresent(
        smallImage ->
            ImageUtil.populateSmallFields(
                menu,
                imgDescriptor.getSmallSize(),
                PathUtil.normalizedPath(imgDescriptor.getSmallPath(), smallImage.getFilename())));

    mediumSized.ifPresent(
        mediumImage ->
            ImageUtil.populateMediumFields(
                menu,
                imgDescriptor.getMediumSize(),
                PathUtil.normalizedPath(imgDescriptor.getMediumPath(), mediumImage.getFilename())));

    largeSized.ifPresent(
        largeImage ->
            ImageUtil.populateLargeFields(
                menu,
                imgDescriptor.getLargeSize(),
                PathUtil.normalizedPath(imgDescriptor.getLargePath(), largeImage.getFilename())));

    return Optional.of(menu);
  }

  public Optional<T> removeAllSizesImage(T menu) {
    removeSmallImage(menu);
    removeMediumImage(menu);
    removeLargeImage(menu);

    removeOriginal(menu);

    return Optional.of(menu);
  }

  private void removeSmallImage(T menu) {
    Optional.ofNullable(menu.getUriSmall())
        .ifPresent(
            uriSmall -> {
              Boolean isDeleted = imageService.removeImage(menu.getBrand(), uriSmall);
              log.info(FILE_REMOVAL_STATUS, uriSmall, isDeleted);
              ImageUtil.removeSmallFields(menu);
            });
  }

  private void removeMediumImage(T menu) {
    Optional.ofNullable(menu.getUriMedium())
        .ifPresent(
            uriMedium -> {
              Boolean isDeleted = imageService.removeImage(menu.getBrand(), uriMedium);
              log.info(FILE_REMOVAL_STATUS, uriMedium, isDeleted);
              ImageUtil.removeMediumFields(menu);
            });
  }

  private void removeLargeImage(T menu) {
    Optional.ofNullable(menu.getUriLarge())
        .ifPresent(
            uriLarge -> {
              Boolean isDeleted = imageService.removeImage(menu.getBrand(), uriLarge);
              log.info(FILE_REMOVAL_STATUS, uriLarge, isDeleted);
              ImageUtil.removeLargeFields(menu);
            });
  }

  private void removeOriginal(T menu) {
    Optional.ofNullable(menu.getFilename())
        .ifPresent(
            filename -> {
              String pathToOriginal =
                  PathUtil.normalizedPath(filename.getPath(), filename.getFilename());
              Boolean isDeleted = imageService.removeImage(menu.getBrand(), pathToOriginal);
              log.info(FILE_REMOVAL_STATUS, pathToOriginal, isDeleted);
              menu.setFilename(null);
            });
  }

  public Optional<T> attachAllSizesImage(T menu, MultipartFile file, ImagePath imgDescriptor) {
    return attachAllSizesImage(menu, null, file, imgDescriptor);
  }
}
