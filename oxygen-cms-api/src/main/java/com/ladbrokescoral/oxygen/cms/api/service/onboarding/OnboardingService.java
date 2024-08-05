package com.ladbrokescoral.oxygen.cms.api.service.onboarding;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.OnBoarding;
import com.ladbrokescoral.oxygen.cms.api.repository.IOnBoardingRepository;
import com.ladbrokescoral.oxygen.cms.api.service.AbstractService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.util.List;
import java.util.Optional;
import java.util.function.BiFunction;
import org.springframework.util.CollectionUtils;
import org.springframework.util.ObjectUtils;
import org.springframework.web.multipart.MultipartFile;

public abstract class OnboardingService<T extends OnBoarding> extends AbstractService<T> {
  IOnBoardingRepository<T> onBoardingRepository;
  protected final ImageService imageService;
  protected final String mediumPath;
  private final String mediumImageSize;

  protected OnboardingService(
      IOnBoardingRepository<T> repository,
      ImageService imageService,
      String mediumPath,
      String mediumImageSize) {
    super(repository);
    this.onBoardingRepository = repository;
    this.imageService = imageService;
    this.mediumPath = mediumPath;
    this.mediumImageSize = mediumImageSize;
  }

  public boolean isEntityValidToCreate(T entity) {

    return !ObjectUtils.isEmpty(entity.getId())
        || !onBoardingRepository.existsByBrand(entity.getBrand());
  }

  public Optional<T> readByBrand(String brand) {
    List<T> tutorials = onBoardingRepository.findByBrand(brand);
    if (CollectionUtils.isEmpty(tutorials)) return Optional.empty();
    return Optional.ofNullable(tutorials.get(0));
  }
  // Image upload with the Size (WxH)
  public BiFunction<T, MultipartFile, Optional<T>> getUploadImageFunction() {
    return (T onboarding, MultipartFile image) -> {
      ImageServiceImpl.Size size = new ImageServiceImpl.Size(mediumImageSize);
      Optional<Filename> uploaded = Optional.empty();
      if (image.getOriginalFilename().endsWith(".svg"))
        uploaded = imageService.upload(onboarding.getBrand(), image, mediumPath);
      else uploaded = imageService.upload(onboarding.getBrand(), image, mediumPath, size);
      return uploaded.map(
          (Filename uploadedImage) -> {
            onboarding.setHeightMedium(size.getHeight());
            onboarding.setWidthMedium(size.getWidth());
            onboarding.setImageUrl(
                PathUtil.normalizedPath(mediumPath, uploadedImage.getFilename()));
            return onboarding;
          });
    };
  }
  // Image upload without the Size (WxH)
  public BiFunction<T, MultipartFile, Optional<T>> getUploadImageFunctionExcludeHW() {
    return (T onboarding, MultipartFile image) -> {
      Optional<Filename> uploaded = Optional.empty();
      uploaded = imageService.upload(onboarding.getBrand(), image, mediumPath);
      return uploaded.map(
          (Filename uploadedImage) -> {
            onboarding.setImageUrl(
                PathUtil.normalizedPath(mediumPath, uploadedImage.getFilename()));
            return onboarding;
          });
    };
  }

  public Optional<T> attachImage(T onboarding, MultipartFile image) {
    onboarding.setFileName(image.getOriginalFilename());
    return getUploadImageFunction().apply(onboarding, image);
  }

  public Optional<T> removeImage(T onboarding) {
    return Optional.ofNullable(onboarding.getImageUrl())
        .map(
            (String uriMedium) -> {
              if (imageService.removeImage(onboarding.getBrand(), uriMedium)) {
                onboarding.setImageUrl(null);
                onboarding.setHeightMedium(null);
                onboarding.setWidthMedium(null);
                onboarding.setFileName(null);
                return onboarding;
              }
              return null;
            });
  }
}
