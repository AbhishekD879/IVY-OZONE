package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.BannerEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.BetReceiptBannerExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.CustomMongoRepository;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@Validated
public class BetReceiptService<T extends BannerEntity> extends ImageOperationsService<T> {

  private final BetReceiptBannerExtendedRepository<T> extendedRepository;
  private final ImageService imageService;
  private final String originalPath;
  private final String mediumPath;
  private final String mediumSize;

  BetReceiptService(
      CustomMongoRepository repository,
      BetReceiptBannerExtendedRepository extendedRepository,
      ImageService imageService,
      String originalPath,
      String mediumPath,
      String mediumSize) {
    super(repository);
    this.extendedRepository = extendedRepository;
    this.imageService = imageService;
    this.originalPath = originalPath;
    this.mediumPath = mediumPath;
    this.mediumSize = mediumSize;
  }

  public List<T> findAllByBrand(String brand) {
    return extendedRepository.findBetReceiptBanners(brand);
  }

  public Optional<T> uploadImage(
      T betReceipt, @ValidFileType({"jpeg", "png", "jpg"}) MultipartFile image) {

    imageService
        .upload(betReceipt.getBrand(), image, mediumPath, new ImageServiceImpl.Size(mediumSize))
        .ifPresent(
            uImage ->
                betReceipt.setUriMedium(PathUtil.normalizedPath(mediumPath, uImage.getFilename())));

    imageService
        .upload(betReceipt.getBrand(), image, originalPath)
        .ifPresent(
            uImage -> {
              betReceipt.setUriOriginal(
                  PathUtil.normalizedPath(originalPath, uImage.getFilename()));
              betReceipt.setFilename(uImage);
            });

    return Optional.of(betReceipt);
  }

  @Override
  public Optional<T> removeImages(T betReceipt) {
    String uriMedium = betReceipt.getUriMedium();
    Optional.ofNullable(uriMedium)
        .map(image -> imageService.removeImage(betReceipt.getBrand(), image))
        .ifPresent(
            deleted -> {
              log.info("File {} removal status : {}", uriMedium, deleted);
              betReceipt.setUriMedium(null);
            });

    String uriOriginal = betReceipt.getUriOriginal();
    Optional.ofNullable(uriOriginal)
        .map(image -> imageService.removeImage(betReceipt.getBrand(), image))
        .ifPresent(
            deleted -> {
              log.info("File {} removal status : {}", uriOriginal, deleted);
              betReceipt.setUriOriginal(null);
              betReceipt.setFilename(null);
            });
    return Optional.of(betReceipt);
  }
}
