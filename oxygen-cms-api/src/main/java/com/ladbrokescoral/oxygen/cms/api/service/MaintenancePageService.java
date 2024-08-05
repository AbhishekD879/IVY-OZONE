package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.MaintenancePage;
import com.ladbrokescoral.oxygen.cms.api.repository.MaintenancePageRepository;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
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
public class MaintenancePageService extends ImageOperationsService<MaintenancePage> {

  private final MaintenanceNotificationSchedulerService maintenanceNotificationService;
  private final ImageService imageService;
  private final String originalPath;
  private final String mediumPath;
  private final String mediumSize;

  @Autowired
  public MaintenancePageService(
      MaintenancePageRepository repository,
      ImageService imageService,
      MaintenanceNotificationSchedulerService maintenanceNotificationService,
      @Value("${images.maintenancePage.original}") String originalPath,
      @Value("${images.maintenancePage.medium}") String mediumPath,
      @Value("${images.maintenancePage.mediumSize}") String mediumSize) {
    super(repository);
    this.imageService = imageService;
    this.maintenanceNotificationService = maintenanceNotificationService;
    this.originalPath = originalPath;
    this.mediumPath = mediumPath;
    this.mediumSize = mediumSize;
  }

  @Override
  public <S extends MaintenancePage> S save(S entity) {
    S saved = super.save(entity);
    maintenanceNotificationService.updateNotifications(saved);
    return saved;
  }

  @Override
  public void delete(String id) {
    Optional<MaintenancePage> oldMaintenancePage = findOne(id);
    super.delete(id);
    oldMaintenancePage.ifPresent(maintenanceNotificationService::updateNotifications);
  }

  public Optional<MaintenancePage> uploadImage(
      MaintenancePage maintenancePage, @ValidFileType({"jpeg", "png", "jpg"}) MultipartFile image) {
    Optional<Filename> uploadedMedium =
        imageService.upload(
            maintenancePage.getBrand(), image, mediumPath, new ImageServiceImpl.Size(mediumSize));
    Optional<Filename> uploadedOriginal =
        imageService.upload(maintenancePage.getBrand(), image, originalPath);

    uploadedMedium.ifPresent(
        uImage ->
            maintenancePage.setUriMedium(
                PathUtil.normalizedPath(mediumPath, uImage.getFilename())));

    uploadedOriginal.ifPresent(
        uImage -> {
          maintenancePage.setUriOriginal(
              PathUtil.normalizedPath(originalPath, uImage.getFilename()));
          maintenancePage.setFilename(uImage);
        });

    return Optional.of(maintenancePage);
  }

  @Override
  public Optional<MaintenancePage> removeImages(MaintenancePage maintenancePage) {
    removeMediumImage(maintenancePage);
    removeOriginalImage(maintenancePage);

    return Optional.of(maintenancePage);
  }

  private void removeMediumImage(MaintenancePage maintenancePage) {
    Optional.ofNullable(maintenancePage.getUriMedium())
        .ifPresent(
            uri -> {
              Boolean isDeleted = imageService.removeImage(maintenancePage.getBrand(), uri);
              log.info("File {} removal status : {}", uri, isDeleted);
              maintenancePage.setUriMedium(null);
            });
  }

  private void removeOriginalImage(MaintenancePage maintenancePage) {
    Optional.ofNullable(maintenancePage.getUriOriginal())
        .ifPresent(
            uri -> {
              Boolean isDeleted = imageService.removeImage(maintenancePage.getBrand(), uri);
              log.info("File {} removal status : {}", uri, isDeleted);
              maintenancePage.setUriOriginal(null);
              maintenancePage.setFilename(null);
            });
  }
}
