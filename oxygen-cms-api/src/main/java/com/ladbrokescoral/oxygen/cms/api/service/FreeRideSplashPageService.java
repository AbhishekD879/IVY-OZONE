package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideSplashPage;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.FreeRideSplashPageFailureException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.FreeRideSplashPageRepository;
import java.util.List;
import java.util.Objects;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class FreeRideSplashPageService extends AbstractService<FreeRideSplashPage> {

  private final ImageService imageService;
  private FreeRideSplashPageRepository freeRideSplashPageRepository;
  private final String path;

  public FreeRideSplashPageService(
      ImageService imageService,
      FreeRideSplashPageRepository freeRideSplashPageRepository,
      @Value("${images.freeride.png}") String path) {
    super(freeRideSplashPageRepository);
    this.imageService = imageService;
    this.path = path;
    this.freeRideSplashPageRepository = freeRideSplashPageRepository;
  }

  public FreeRideSplashPage handleFileUploading(
      String splashpageId,
      MultipartFile splashFile,
      MultipartFile bannerFile,
      MultipartFile freeRideFile) {
    FreeRideSplashPage freeRideSplashPage =
        findOne(splashpageId).orElseThrow(NotFoundException::new);
    if (null != splashFile) {
      if (Objects.nonNull(freeRideSplashPage.getSplashImage())) {
        handleRemoveFile(
            freeRideSplashPage.getBrand(), freeRideSplashPage.getSplashImage().relativePath());
      }
      handleSplashFile(splashFile, freeRideSplashPage);
    }
    if (null != bannerFile) {
      if (Objects.nonNull(freeRideSplashPage.getBannerImage())) {
        handleRemoveFile(
            freeRideSplashPage.getBrand(), freeRideSplashPage.getBannerImage().relativePath());
      }
      handleBannerFile(bannerFile, freeRideSplashPage);
    }
    if (null != freeRideFile) {
      if (Objects.nonNull(freeRideSplashPage.getFreeRideLogo())) {
        handleRemoveFile(
            freeRideSplashPage.getBrand(), freeRideSplashPage.getFreeRideLogo().relativePath());
      }
      handleFreeRideFile(freeRideFile, freeRideSplashPage);
    }
    save(freeRideSplashPage);
    return freeRideSplashPage;
  }

  private void handleRemoveFile(String brand, String path) {
    if (!(imageService.removeImage(brand, path))) {
      throw new FreeRideSplashPageFailureException("Error occurred while Removing file");
    }
  }

  private void handleSplashFile(MultipartFile splashFile, FreeRideSplashPage freeRideSplashPage) {

    Filename splash = getUploadedImage(freeRideSplashPage.getBrand(), splashFile);
    freeRideSplashPage.setSplashImage(splash);
    freeRideSplashPage.setSplashImageName(splash.getOriginalname());
  }

  private void handleBannerFile(MultipartFile bannerFile, FreeRideSplashPage freeRideSplashPage) {

    Filename banner = getUploadedImage(freeRideSplashPage.getBrand(), bannerFile);
    freeRideSplashPage.setBannerImage(banner);
    freeRideSplashPage.setBannerImageFileName(banner.getOriginalname());
  }

  private void handleFreeRideFile(
      MultipartFile freeRideFile, FreeRideSplashPage freeRideSplashPage) {

    Filename freeRide = getUploadedImage(freeRideSplashPage.getBrand(), freeRideFile);
    freeRideSplashPage.setFreeRideLogo(freeRide);
    freeRideSplashPage.setFreeRideLogoFileName(freeRide.getOriginalname());
  }

  private Filename getUploadedImage(String brand, MultipartFile imageFile) {
    return imageService
        .upload(brand, imageFile, path)
        .orElseThrow(
            () ->
                new FileUploadException(
                    "Image uploading error for image: " + imageFile.getOriginalFilename()));
  }

  public String getSplashPageId(FreeRideSplashPage responseEntity) {
    try {
      return responseEntity.getId();
    } catch (NullPointerException ex) {
      throw new FreeRideSplashPageFailureException("Id should not be null");
    }
  }

  public List<FreeRideSplashPage> getFreeRideSplashPageByBrand(String brand) {
    return this.freeRideSplashPageRepository.findAllByBrand(brand);
  }
}
