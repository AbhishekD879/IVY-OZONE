package com.ladbrokescoral.oxygen.cms.api.service.onboarding;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.MyStableOnboardingDto;
import com.ladbrokescoral.oxygen.cms.api.dto.MyStableOnboardingCFDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.MyStableOnboarding;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.MyStableOnboardingException;
import com.ladbrokescoral.oxygen.cms.api.repository.MyStableOnboardingRepository;
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
public class MyStableOnboardingService extends OnboardingService<MyStableOnboarding> {
  private ModelMapper modelMapper;

  public MyStableOnboardingService(
      MyStableOnboardingRepository repository,
      ImageService imageService,
      @Value("${images.mystable.medium}") String mediumPath,
      @Value("${images.mystable.size}") String mediumImageSize,
      ModelMapper modelMapper) {
    super(repository, imageService, mediumPath, mediumImageSize);
    this.modelMapper = modelMapper;
  }

  @Override
  public MyStableOnboarding save(MyStableOnboarding myStableOnboarding) {
    if (Objects.nonNull(myStableOnboarding.getOnboardImageDetails())
        || isEntityValidToCreate(myStableOnboarding)) return super.save(myStableOnboarding);
    throw new MyStableOnboardingException("Save failed");
  }

  @Override
  public boolean isEntityValidToCreate(MyStableOnboarding entity) {

    return (!ObjectUtils.isEmpty(entity.getId()))
        || (!onBoardingRepository.existsByBrand(entity.getBrand()));
  }

  @Override
  public Optional<MyStableOnboarding> attachImage(
      MyStableOnboarding onboarding, MultipartFile image) {
    try {
      return Optional.ofNullable(getMyStableUploadImageFunctionExcludeHW(onboarding, image));
    } catch (FileUploadException exception) {
      log.error("File Upload Exception : {}", exception.getMessage());
      throw new MyStableOnboardingException("File Upload failed");
    }
  }

  public MyStableOnboarding getMyStableUploadImageFunctionExcludeHW(
      MyStableOnboarding onboarding, MultipartFile multipartFile) {

    Optional<Filename> uploaded =
        Optional.of(
            imageService
                .upload(onboarding.getBrand(), multipartFile, mediumPath)
                .orElseThrow(
                    () ->
                        new FileUploadException(
                            "Image uploading error for image: "
                                + multipartFile.getOriginalFilename())));

    uploaded.ifPresent(onboarding::setOnboardImageDetails);
    return onboarding;
  }

  @Override
  public Optional<MyStableOnboarding> removeImage(MyStableOnboarding onboarding) {

    return Optional.ofNullable(onboarding.getOnboardImageDetails())
        .map(
            (Filename filename) -> {
              String path =
                  onboarding
                      .getOnboardImageDetails()
                      .getPath()
                      .concat(onboarding.getOnboardImageDetails().getFilename());
              if (!imageService.removeImage(onboarding.getBrand(), path))
                throw new MyStableOnboardingException(
                    "Remove Image failed with id : " + onboarding.getId());
              return Optional.of(onboarding);
            })
        .orElseThrow(
            () ->
                new MyStableOnboardingException(
                    String.format(
                        "There's no Existing image details for the given entity with id  : %s and remove failed",
                        onboarding.getId())));
  }

  public Optional<MyStableOnboardingCFDto> convertToCFDto(MyStableOnboarding entity) {
    return Optional.ofNullable(modelMapper.map(entity, MyStableOnboardingCFDto.class));
  }

  public MyStableOnboarding updateOnboardingImage(
      MyStableOnboarding existingEntity, MyStableOnboardingDto myStableOnboardingDto) {
    MyStableOnboarding myStableOnboarding = null;
    MyStableOnboarding validEntity = null;
    try {

      if (Objects.nonNull(myStableOnboardingDto.getOnboardImg())) {
        myStableOnboarding = modelMapper.map(myStableOnboardingDto, MyStableOnboarding.class);
        validEntity =
            checkDeletedandRemoved(existingEntity, myStableOnboardingDto, myStableOnboarding);

        return validEntity;
      } else {
        throw new MyStableOnboardingException("Image should be uploaded!!");
      }
    } catch (Exception ae) {
      throw new MyStableOnboardingException(ae.getMessage());
    }
  }

  private MyStableOnboarding checkDeletedandRemoved(
      MyStableOnboarding existingEntity,
      MyStableOnboardingDto myStableOnboardingDto,
      MyStableOnboarding myStableOnboarding) {

    Optional<Filename> filenameOptional =
        Optional.ofNullable(myStableOnboarding.getOnboardImageDetails());

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
                  uploadImageToCF(myStableOnboardingDto, myStableOnboarding);
                }
              } catch (Exception e) {
                handleException(existingEntity);
                throw new MyStableOnboardingException("Exception :  " + e.getMessage());
              }
              return myStableOnboarding;
            })
        .orElseGet(
            () -> {
              try {
                uploadImageToCF(myStableOnboardingDto, myStableOnboarding);
              } catch (Exception ae) {
                handleException(existingEntity);
                throw new MyStableOnboardingException("Exception :  " + ae.getMessage());
              }
              return myStableOnboarding;
            });
  }

  private void uploadImageToCF(
      MyStableOnboardingDto myStableOnboardingDto, MyStableOnboarding myStableOnboarding) {
    Filename filename =
        handleOnboardingImageUpload(
            myStableOnboarding.getBrand(), myStableOnboardingDto.getOnboardImg());

    myStableOnboarding.setOnboardImageDetails(filename);
  }

  private void handleException(MyStableOnboarding existingEntity) {
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
