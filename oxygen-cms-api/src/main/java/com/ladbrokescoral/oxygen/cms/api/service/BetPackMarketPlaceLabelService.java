package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackLabel;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.exception.BetPackMarketPlaceException;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackEnablerLabelRepository;
import java.util.List;
import java.util.Objects;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
@Slf4j
public class BetPackMarketPlaceLabelService extends SortableService<BetPackLabel> {

  private final ImageService imageService;
  private final String path;

  public BetPackMarketPlaceLabelService(
      ImageService imageService,
      @Value("${images.betPackLabel.png}") String path,
      BetPackEnablerLabelRepository betPackEnablerLabelRepository) {
    super(betPackEnablerLabelRepository);
    this.imageService = imageService;
    this.path = path;
  }

  /**
   * UploadBannerImage - to save banner image and update the image name and path to the existing
   * Object.
   *
   * @param id saved ID in Mongo
   * @param backgroundImg the image file which will be save into S3
   * @return betPackBanner
   */
  public BetPackLabel uploadBackgroundImage(String id, MultipartFile backgroundImg) {
    BetPackLabel betPackLabelEntity = repository.findById(id).orElseThrow(NotFoundException::new);
    if (!backgroundImg.isEmpty()) {
      if (Objects.nonNull(betPackLabelEntity.getBackgroundImage())) {
        handleRemoveFile(
            betPackLabelEntity.getBrand(), betPackLabelEntity.getBackgroundImage().relativePath());
      }
      handleBackgroundUpload(betPackLabelEntity, backgroundImg);
    }
    save(betPackLabelEntity);
    return betPackLabelEntity;
  }

  private void handleBackgroundUpload(BetPackLabel betPackLabel, MultipartFile backgroundImage) {
    Filename backgroundImg = uploadImage(betPackLabel.getBrand(), backgroundImage);
    betPackLabel.setBackgroundImage(backgroundImg);
    betPackLabel.setBackgroundImageFileName(backgroundImg.getOriginalname());
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

  public BetPackLabel handleRemoveImage(BetPackLabel responseEntity) {
    boolean status =
        imageService.removeImage(
            responseEntity.getBrand(), responseEntity.getBackgroundImage().relativePath());
    if (status) {
      responseEntity.setBackgroundImage(null);
      responseEntity.setBackgroundImageFileName(null);
    }
    return responseEntity;
  }

  public List<BetPackLabel> getBetPackLabelByBrand(String brand) {
    return this.repository.findByBrand(brand);
  }
}
