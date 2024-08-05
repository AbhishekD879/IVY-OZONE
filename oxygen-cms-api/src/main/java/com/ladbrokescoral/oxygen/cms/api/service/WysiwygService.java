package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.WysiwygEntity;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@Service
public class WysiwygService {

  private final ImageService imageService;
  private final String wyswigCorePath;

  public WysiwygService(
      ImageService imageService, @Value("${images.wyswig.path}") String wyswigCorePath) {
    this.imageService = imageService;
    this.wyswigCorePath = wyswigCorePath;
  }

  public Optional<WysiwygEntity> attachWyswigImage(
      String brand,
      @ValidFileType({"png", "jpeg", "jpg"}) MultipartFile file,
      String collectionName,
      String entityId) {
    Optional<Filename> upload =
        imageService.upload(
            brand, file, PathUtil.concatPath(wyswigCorePath, collectionName, entityId), null);
    return upload.map(Filename::getFullPath).map(WysiwygEntity::new);
  }

  public boolean removeWyswigImage(
      String brand, String collectionName, String id, String imageName) {
    String path = PathUtil.concatPath(wyswigCorePath, collectionName, id, imageName);
    Boolean isDeleted = imageService.removeImage(brand, path);
    log.info("File {} removal status : {}", path, isDeleted);

    return isDeleted;
  }
}
