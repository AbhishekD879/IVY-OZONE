package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Feature;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.repository.FeatureExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.FeatureRepository;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import com.ladbrokescoral.oxygen.cms.util.ImageUtil;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@Component
public class FeatureService extends ImageOperationsService<Feature> {

  private final FeatureExtendedRepository extendedRepository;
  private final ImageService imageService;

  private final String mediumFeaturesPath;
  private final String corePath;

  private final ImageServiceImpl.Size medium;

  @Autowired
  public FeatureService(
      FeatureRepository repository,
      FeatureExtendedRepository extendedRepository,
      ImageService imageService,
      @Value("${images.features.medium.path}") String mediumFeaturesPath,
      @Value("${images.core}") String corePath,
      @Value("${images.features.medium.size}") String mediumFeaturesSize) {
    super(repository);
    this.extendedRepository = extendedRepository;
    this.imageService = imageService;

    this.corePath = corePath;
    this.mediumFeaturesPath = mediumFeaturesPath;

    this.medium = new ImageServiceImpl.Size(mediumFeaturesSize);
  }

  public List<Feature> findAllByBrand(String brand) {
    return extendedRepository.findFeatures(brand);
  }

  public Optional<Feature> attachImage(
      Feature feature, @ValidFileType({"png", "jpeg", "jpg"}) MultipartFile file) {
    Optional<Filename> mediumSized =
        imageService.upload(feature.getBrand(), file, mediumFeaturesPath, medium);
    Optional<Filename> original = imageService.upload(feature.getBrand(), file, corePath);

    if (!mediumSized.isPresent()) {
      log.error("Issue with uploading image, uploading successful for : medium - {}", false);
      return Optional.empty();
    }

    mediumSized.ifPresent(
        mediumImage ->
            ImageUtil.populateMediumFields(
                feature,
                medium,
                PathUtil.normalizedPath(mediumFeaturesPath, mediumImage.getFilename())));

    original.ifPresent(feature::setFilename);
    return Optional.of(feature);
  }

  public Optional<Feature> removeImages(Feature feature) {
    removeMediumImage(feature);
    removeOriginal(feature);

    return Optional.of(feature);
  }

  private void removeMediumImage(Feature feature) {
    Optional.ofNullable(feature.getUriMedium())
        .ifPresent(
            uriMedium -> {
              Boolean isDeleted = imageService.removeImage(feature.getBrand(), uriMedium);
              log.info("File {} removal status : {}", uriMedium, isDeleted);
              ImageUtil.removeMediumFields(feature);
            });
  }

  private void removeOriginal(Feature feature) {
    Optional.ofNullable(feature.getFilename())
        .ifPresent(
            filename -> {
              String pathToOriginal =
                  PathUtil.normalizedPath(filename.getPath(), filename.getFilename());
              Boolean isDeleted = imageService.removeImage(feature.getBrand(), pathToOriginal);
              log.info("File {} removal status : {}", pathToOriginal, isDeleted);
              feature.setFilename(null);
            });
  }
}
