package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackBanner;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.exception.BetPackMarketPlaceException;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackEnablerBannerRepository;
import java.util.List;
import java.util.Objects;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class BetPackMarketPlaceBannerService extends SortableService<BetPackBanner> {

  private final BetPackEnablerBannerRepository betPackEnablerBannerRepository;
  private final ImageService imageService;
  private final String path;

  public BetPackMarketPlaceBannerService(
      BetPackEnablerBannerRepository betPackEnablerBannerRepository,
      ImageService imageService,
      @Value("${images.betPackBanner.png}") String path) {
    super(betPackEnablerBannerRepository);
    this.betPackEnablerBannerRepository = betPackEnablerBannerRepository;
    this.imageService = imageService;
    this.path = path;
  }

  /**
   * UploadBannerImage - to save banner image and update the image name and path to the existing
   * Object.
   *
   * @param id saved ID in Mongo
   * @param img
   * @param bannerImgInMarketPlacePage
   * @param bannerImg the image file which will be save into S3
   * @return betPackBanner
   */
  public BetPackBanner uploadBannerImage(
      MultipartFile bannerImg, BetPackBanner betPackBannerEntity) {
    if (null != bannerImg) {
      if (Objects.nonNull(betPackBannerEntity.getBannerImage())) {
        handleRemoveFile(
            betPackBannerEntity.getBrand(), betPackBannerEntity.getBannerImage().relativePath());
      }
      handleBannerUpload(betPackBannerEntity, bannerImg);
    }

    save(betPackBannerEntity);
    return betPackBannerEntity;
  }

  private void handleBannerUpload(
      BetPackBanner betPackBanner, MultipartFile bannerImgInMarketPlacePage) {
    Filename banner = uploadImage(betPackBanner.getBrand(), bannerImgInMarketPlacePage);
    betPackBanner.setBannerImage(banner);
    betPackBanner.setBannerImageFileName(banner.getOriginalname());
  }

  private void handleRemoveFile(String brand, String path) {
    if (!(imageService.removeImage(brand, path))) {
      throw new BetPackMarketPlaceException("Error occurred while Removing file");
    }
  }

  /**
   * UploadBannerImage - to save banner image and update the image name and path to the existing
   * Object.
   *
   * @param brand The image will be saved for different brand. let's say Coral/ Ladbrokes
   * @param imageFile the image file which will be save into S3
   * @return Filename
   */
  public Filename uploadImage(String brand, MultipartFile imageFile) {
    return imageService
        .upload(brand, imageFile, path)
        .orElseThrow(
            () ->
                new FileUploadException(
                    "Image uploading error for image: " + imageFile.getOriginalFilename()));
  }

  public List<BetPackBanner> getBetPackBannerByBrand(String brand) {
    return this.betPackEnablerBannerRepository.findByBrand(brand);
  }
}
