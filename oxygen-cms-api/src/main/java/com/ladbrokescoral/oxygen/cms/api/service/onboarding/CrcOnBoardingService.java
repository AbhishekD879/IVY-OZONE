package com.ladbrokescoral.oxygen.cms.api.service.onboarding;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.CrcOnBoardingDto;
import com.ladbrokescoral.oxygen.cms.api.dto.CrcOnBoardingCFDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CrcOnBoarding;
import com.ladbrokescoral.oxygen.cms.api.exception.CrcOnBoardingException;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.repository.CrcOnBoardingRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import java.util.Objects;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.multipart.MultipartFile;

@Service
@Validated
@Slf4j
public class CrcOnBoardingService extends OnboardingService<CrcOnBoarding> {
  private ModelMapper modelMapper;

  public CrcOnBoardingService(
      CrcOnBoardingRepository repository,
      ImageService imageService,
      @Value("${images.crc.medium}") String mediumPath,
      @Value("${images.crc.size}") String mediumImageSize,
      ModelMapper modelMapper) {
    super(repository, imageService, mediumPath, mediumImageSize);
    this.modelMapper = modelMapper;
  }

  @Override
  public CrcOnBoarding save(CrcOnBoarding crcOnboarding) {
    if (Objects.nonNull(crcOnboarding.getOnboardImageDetails())
        || isEntityValidToCreate(crcOnboarding)) return super.save(crcOnboarding);
    throw new CrcOnBoardingException("Save failed");
  }

  @Override
  public boolean isEntityValidToCreate(CrcOnBoarding entity) {

    return (!ObjectUtils.isEmpty(entity.getId()))
        || (!onBoardingRepository.existsByBrand(entity.getBrand()));
  }

  @Override
  public Optional<CrcOnBoarding> attachImage(CrcOnBoarding crconboarding, MultipartFile image) {
    try {
      return Optional.ofNullable(getMyStableUploadImageFunctionExcludeHW(crconboarding, image));
    } catch (FileUploadException exception) {
      log.info("File Upload Exception : " + exception.getMessage());
      throw new CrcOnBoardingException("File Upload failed");
    }
  }

  public CrcOnBoarding getMyStableUploadImageFunctionExcludeHW(
      CrcOnBoarding crconboarding, MultipartFile multipartFile) {

    Optional<Filename> uploaded =
        Optional.of(
            imageService
                .upload(crconboarding.getBrand(), multipartFile, mediumPath)
                .orElseThrow(
                    () ->
                        new FileUploadException(
                            "Image uploading error for image: "
                                + multipartFile.getOriginalFilename())));

    uploaded.ifPresent(crconboarding::setOnboardImageDetails);
    return crconboarding;
  }

  @Override
  public Optional<CrcOnBoarding> removeImage(CrcOnBoarding crconboarding) {

    return Optional.ofNullable(crconboarding.getOnboardImageDetails())
        .map(
            (Filename filename) -> {
              String path =
                  crconboarding
                      .getOnboardImageDetails()
                      .getPath()
                      .concat(crconboarding.getOnboardImageDetails().getFilename());
              if (!imageService.removeImage(crconboarding.getBrand(), path))
                throw new CrcOnBoardingException(
                    "Remove Image failed with id : " + crconboarding.getId());
              return Optional.of(crconboarding);
            })
        .orElseThrow(
            () ->
                new CrcOnBoardingException(
                    String.format(
                        "There's no Existing image details for the given entity with id  : %s and remove failed",
                        crconboarding.getId())));
  }

  public Optional<CrcOnBoardingCFDto> convertToCFDto(CrcOnBoarding entity) {
    return Optional.ofNullable(modelMapper.map(entity, CrcOnBoardingCFDto.class));
  }

  public CrcOnBoarding updateOnboardingImage(
      CrcOnBoarding existingEntity, CrcOnBoardingDto crcOnboardingDto) {
    CrcOnBoarding crcOnboarding = null;
    CrcOnBoarding validEntity = null;
    try {

      if (Objects.nonNull(crcOnboardingDto.getOnboardImg())) {
        crcOnboarding = modelMapper.map(crcOnboardingDto, CrcOnBoarding.class);
        validEntity = checkDeletedandRemoved(existingEntity, crcOnboardingDto, crcOnboarding);

        return validEntity;
      } else {
        throw new CrcOnBoardingException("Image should be uploaded!!");
      }
    } catch (Exception ae) {
      throw new CrcOnBoardingException(ae.getMessage());
    }
  }

  private CrcOnBoarding checkDeletedandRemoved(
      CrcOnBoarding existingEntity,
      CrcOnBoardingDto crcOnboardingDto,
      CrcOnBoarding crcOnboarding) {

    Optional<Filename> filenameOptional =
        Optional.ofNullable(crcOnboarding.getOnboardImageDetails());

    return filenameOptional
        .map(
            (Filename filenames) -> {
              try {
                String path =
                    existingEntity
                        .getOnboardImageDetails()
                        .getPath()
                        .concat(existingEntity.getOnboardImageDetails().getFilename());
                if (handleRemoveFile(existingEntity.getBrand(), path)) {
                  uploadImageToCF(crcOnboardingDto, crcOnboarding);
                }
              } catch (Exception e) {
                handleException(existingEntity);
                throw new CrcOnBoardingException("Exception :  " + e.getMessage());
              }
              return crcOnboarding;
            })
        .orElseGet(
            () -> {
              try {
                uploadImageToCF(crcOnboardingDto, crcOnboarding);
              } catch (Exception ae) {
                handleException(existingEntity);
                throw new CrcOnBoardingException("Exception :  " + ae.getMessage());
              }
              return crcOnboarding;
            });
  }

  private void uploadImageToCF(CrcOnBoardingDto crcOnboardingDto, CrcOnBoarding crcOnboarding) {
    Filename filename =
        handleOnboardingImageUpload(crcOnboarding.getBrand(), crcOnboardingDto.getOnboardImg());

    crcOnboarding.setOnboardImageDetails(filename);
  }

  private void handleException(CrcOnBoarding existingEntity) {
    existingEntity.setOnboardImageDetails(null);
    save(existingEntity);
  }

  private Filename handleOnboardingImageUpload(String brand, MultipartFile file) {
    return uploadImage(brand, file);
  }

  public Filename uploadImage(String brand, MultipartFile imageFile) {
    return imageService
        .upload(brand, imageFile, mediumPath)
        .orElseThrow(
            () ->
                new FileUploadException(
                    "Image uploading error for image: " + imageFile.getOriginalFilename()));
  }

  private boolean handleRemoveFile(String brand, String path) {
    return imageService.removeImage(brand, path);
  }
}
