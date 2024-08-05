package com.ladbrokescoral.oxygen.cms.api.service;

import com.fasterxml.jackson.dataformat.csv.CsvSchema;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.QualificationRule;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.QualificationRuleRepository;
import com.ladbrokescoral.oxygen.cms.api.service.fileencryption.CsvEncryptingService;
import java.util.Optional;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class QualificationRuleService extends AbstractService<QualificationRule> {
  private final QualificationRuleRepository qualificationRuleRepository;
  private final ImageService imageService;
  private final String blacklistPath;
  private final String blacklistUUID;

  public QualificationRuleService(
      QualificationRuleRepository qualificationRuleRepository,
      ImageService imageService,
      @Value("${images.game.blacklist.path}") String blacklistPath,
      @Value("${images.game.blacklist.uuid}") String blacklistUUID) {
    super(qualificationRuleRepository);
    this.qualificationRuleRepository = qualificationRuleRepository;
    this.imageService = imageService;
    this.blacklistPath = blacklistPath;
    this.blacklistUUID = blacklistUUID;
  }

  @Override
  public QualificationRule save(QualificationRule entity) {
    if (qualificationRuleRepository.existsByBrand(entity.getBrand())) {
      throw new IllegalArgumentException(
          String.format(
              "Only one QualificationRule could exist per brand: '%s'", entity.getBrand()));
    }
    return super.save(entity);
  }

  @Override
  public QualificationRule update(
      QualificationRule existingEntity, QualificationRule updateEntity) {
    if (!existingEntity.getBrand().equals(updateEntity.getBrand())) {
      throw new IllegalArgumentException(
          "Brand cannot be cannot be changed once QualificationRule is created");
    }
    return qualificationRuleRepository.save(updateEntity);
  }

  public QualificationRule findOneByBrand(String brand) {
    return qualificationRuleRepository.findOneByBrand(brand).orElseThrow(NotFoundException::new);
  }

  public QualificationRule uploadEncryptedBlacklistedUsers(String brand, MultipartFile file) {
    MultipartFile encryptedCsv = getEncryptedMultipartFile(file);

    Optional<Filename> optionalFilename =
        imageService.upload(
            brand, encryptedCsv, path(brand, blacklistPath), getFilename(file), null);
    if (optionalFilename.isPresent()) {
      return saveUploadedCsvToGames(optionalFilename.get(), brand);
    } else {
      throw new FileUploadException("Something went wrong during file uploading");
    }
  }

  private QualificationRule saveUploadedCsvToGames(Filename filename, String brand) {
    QualificationRule existingQR = findOneByBrand(brand);
    existingQR.setBlacklistedUsersPath(buildPath(filename));
    return update(existingQR, existingQR);
  }

  private String buildPath(Filename filename) {
    return filename != null && filename.getPath() != null
        ? filename.getPath().concat("/").concat(filename.getFilename())
        : "";
  }

  private MultipartFile getEncryptedMultipartFile(MultipartFile file) {
    CsvEncryptingService csvEncryptingService =
        new CsvEncryptingService(file, blacklistUUID, getCsvSchema());

    return csvEncryptingService.getEncryptedContent();
  }

  private CsvSchema getCsvSchema() {
    return CsvSchema.builder().build().withoutHeader();
  }

  private String getFilename(MultipartFile image) {
    return Optional.ofNullable(image.getOriginalFilename())
        .filter(img -> img.contains("."))
        .map(img -> StringUtils.substringBefore(img, "."))
        .orElseGet(image::getName);
  }

  private String path(String brand, String path) {
    return StringUtils.endsWith(path, "/") ? (path + brand) : String.format("%s/%s", path, brand);
  }
}
