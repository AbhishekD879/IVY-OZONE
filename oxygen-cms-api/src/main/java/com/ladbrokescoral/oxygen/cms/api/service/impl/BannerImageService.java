package com.ladbrokescoral.oxygen.cms.api.service.impl;

import com.ladbrokescoral.oxygen.cms.api.entity.Banner;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig.ImagePath;
import com.ladbrokescoral.oxygen.cms.util.ImageUtil;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.multipart.MultipartFile;

@Service
@Validated
@Slf4j
public class BannerImageService {

  private static final String RCOMB = "rcomb";
  private static final String FILE_REMOVAL_STATUS = "File {} removal status : {}";
  private final ImagePath imgDescriptor;

  private final ImageService imageService;

  public BannerImageService(ImageService imageService, ImagePath bannerImagePath) {
    this.imageService = imageService;
    this.imgDescriptor = bannerImagePath;
  }

  public Optional<Banner> updateMediumAndSmallImages(
      Banner banner, @ValidFileType({"jpeg", "png", "jpg"}) MultipartFile bannerImage) {
    boolean isRcomb = banner.getBrand().equalsIgnoreCase(RCOMB);
    Optional<Filename> smallSized =
        isRcomb
            ? Optional.empty()
            : imageService.upload(
                banner.getBrand(),
                bannerImage,
                imgDescriptor.getSmallPath(),
                imgDescriptor.getSmallSize());
    Optional<Filename> mediumSized =
        isRcomb
            ? Optional.empty()
            : imageService.upload(
                banner.getBrand(),
                bannerImage,
                imgDescriptor.getMediumPath(),
                imgDescriptor.getMediumSize());
    Optional<Filename> original =
        imageService.upload(
            banner.getBrand(), bannerImage, imgDescriptor.getImagesCorePath(), null);
    // if one of the uploads fails - stop further updates
    if ((!isRcomb && (!smallSized.isPresent() || !mediumSized.isPresent()))
        || !original.isPresent()) {
      log.error(
          "Issue with uploading image, uploading successful for : small - {}, medium - {}, original - {}",
          smallSized.isPresent(),
          mediumSized.isPresent(),
          original.isPresent());
      return Optional.empty();
    }

    original.ifPresent(banner::setFilename);

    if (!isRcomb) {
      smallSized.ifPresent(
          smallImage ->
              ImageUtil.populateSmallFields(
                  banner,
                  imgDescriptor.getSmallSize(),
                  PathUtil.normalizedPath(imgDescriptor.getSmallPath(), smallImage.getFilename())));
      mediumSized.ifPresent(
          mediumImage ->
              ImageUtil.populateMediumFields(
                  banner,
                  imgDescriptor.getMediumSize(),
                  PathUtil.normalizedPath(
                      imgDescriptor.getMediumPath(), mediumImage.getFilename())));
    }

    return Optional.of(banner);
  }

  public Optional<Banner> removeMediumAndSmallImages(Banner banner) {
    removeMediumImage(banner);
    removeSmallImage(banner);

    return Optional.of(banner);
  }

  private void removeSmallImage(Banner banner) {
    Optional.ofNullable(banner.getUriSmall())
        .ifPresent(
            uriSmall -> {
              Boolean isDeleted = imageService.removeImage(banner.getBrand(), uriSmall);
              log.info(FILE_REMOVAL_STATUS, uriSmall, isDeleted);
              ImageUtil.removeSmallFields(banner);
            });
  }

  private void removeMediumImage(Banner banner) {
    Optional.ofNullable(banner.getUriMedium())
        .ifPresent(
            uriMedium -> {
              Boolean isDeleted = imageService.removeImage(banner.getBrand(), uriMedium);
              log.info(FILE_REMOVAL_STATUS, uriMedium, isDeleted);
              ImageUtil.removeMediumFields(banner);
            });
  }

  public Optional<Banner> updateDesktopImage(
      Banner banner, @ValidFileType({"jpeg", "png", "jpg"}) MultipartFile image) {
    boolean isRcomb = banner.getBrand().equalsIgnoreCase(RCOMB);
    Optional<Filename> desktopSized =
        isRcomb
            ? Optional.empty()
            : imageService.upload(
                banner.getBrand(),
                image,
                imgDescriptor.getLargePath(),
                imgDescriptor.getLargeSize());
    Optional<Filename> desktopOriginal =
        imageService.upload(banner.getBrand(), image, imgDescriptor.getImagesCorePath(), null);

    if ((!isRcomb && !desktopSized.isPresent()) || !desktopOriginal.isPresent()) {
      log.error(
          "Issue with uploading desktop image, successful for : medium - {}, original -{}",
          desktopSized.isPresent(),
          desktopOriginal.isPresent());
      return Optional.empty();
    }

    if (!isRcomb) {
      desktopSized.ifPresent(
          desktopImage -> {
            banner.setDesktopHeightMedium(String.valueOf(imgDescriptor.getLargeSize().getHeight()));
            banner.setDesktopWidthMedium(String.valueOf(imgDescriptor.getLargeSize().getWidth()));
            banner.setDesktopUriMedium(
                PathUtil.normalizedPath(
                    imgDescriptor.getLargePath(), desktopSized.get().getFilename()));
          });
    }
    desktopOriginal.ifPresent(banner::setDesktopFilename);

    return Optional.of(banner);
  }

  public Optional<Banner> removeDesktopImage(Banner banner) {
    Optional.ofNullable(banner.getDesktopUriMedium())
        .ifPresent(
            desktopUriMedium -> {
              Boolean isDeleted = imageService.removeImage(banner.getBrand(), desktopUriMedium);
              log.info(FILE_REMOVAL_STATUS, desktopUriMedium, isDeleted);
              banner.setDesktopUriMedium(null);
              banner.setDesktopWidthMedium(null);
              banner.setDesktopHeightMedium(null);
            });
    return Optional.of(banner);
  }
}
