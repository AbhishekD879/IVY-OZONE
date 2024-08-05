package com.ladbrokescoral.oxygen.cms.api.service;

import com.fortify.annotations.FortifyXSSValidate;
import com.ladbrokescoral.oxygen.cms.api.dto.OnboardingImageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackOnboarding;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.OnboardingImage;
import com.ladbrokescoral.oxygen.cms.api.exception.BetPackMarketPlaceException;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackMarketplaceOnboardingRepository;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;
import org.bson.types.ObjectId;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class BetPackMarketPlaceOnboardingService extends SortableService<BetPackOnboarding> {

  private final BetPackMarketplaceOnboardingRepository onboardingRepository;
  private final ImageService imageService;
  private final String path;
  private final ModelMapper modelMapper;

  public BetPackMarketPlaceOnboardingService(
      BetPackMarketplaceOnboardingRepository onboardingRepository,
      ImageService imageService,
      ModelMapper modelMapper,
      @Value("${images.betPackOnboarding.png}") String path) {
    super(onboardingRepository);
    this.onboardingRepository = onboardingRepository;
    this.imageService = imageService;
    this.path = path;
    this.modelMapper = modelMapper;
  }

  @FortifyXSSValidate("return")
  public BetPackOnboarding uploadOnboardingImage(
      BetPackOnboarding betPackOnboarding, List<OnboardingImageDto> images) {
    List<OnboardingImage> imageList =
        images.stream()
            .map(
                (OnboardingImageDto img) ->
                    uploadOnboardingImage(
                        betPackOnboarding,
                        modelMapper.map(img, OnboardingImage.class),
                        img.getOnboardImageDetails(),
                        img.getOnboardImg()))
            .collect(Collectors.toList());

    betPackOnboarding.setImages(imageList);

    return save(betPackOnboarding);
  }

  public OnboardingImage updateOnboardingImage(
      BetPackOnboarding betPackOnboarding, OnboardingImageDto img, OnboardingImage previousEntity) {
    OnboardingImage onboardingImage =
        uploadOnboardingImage(
            betPackOnboarding,
            modelMapper.map(img, OnboardingImage.class),
            img.getOnboardImageDetails(),
            img.getOnboardImg());

    onboardingImage.setId(new ObjectId(img.getId()));
    List<OnboardingImage> onboardingImageList = betPackOnboarding.getImages();
    int index = onboardingImageList.indexOf(previousEntity);
    onboardingImageList.remove(index);
    onboardingImageList.add(index, onboardingImage);

    save(betPackOnboarding);

    return onboardingImage;
  }

  private OnboardingImage uploadOnboardingImage(
      BetPackOnboarding betPackOnboarding,
      OnboardingImage onboardingImage,
      Filename imgDetails,
      MultipartFile file) {

    if (file != null) {
      if (Objects.nonNull(imgDetails)) {
        handleRemoveFile(betPackOnboarding.getBrand(), imgDetails.relativePath());
      }
      onboardingImage.setOnboardImageDetails(handleOnboardingImageUpload(betPackOnboarding, file));
    }
    return onboardingImage;
  }

  private Filename handleOnboardingImageUpload(
      BetPackOnboarding betPackOnboarding, MultipartFile file) {
    return uploadImage(betPackOnboarding.getBrand(), file);
  }

  public Filename uploadImage(String brand, MultipartFile imageFile) {
    return imageService
        .upload(brand, imageFile, path)
        .orElseThrow(
            () ->
                new FileUploadException(
                    "Image uploading error for image: " + imageFile.getOriginalFilename()));
  }

  public String getBpmpOnboardingId(BetPackOnboarding responseEntity) {
    try {
      return responseEntity.getId();
    } catch (NullPointerException ex) {
      throw new BetPackMarketPlaceException("Id should not be null");
    }
  }

  private void handleRemoveFile(String brand, String path) {
    if (!(imageService.removeImage(brand, path))) {
      throw new BetPackMarketPlaceException("Error occurred while Removing file");
    }
  }

  public OnboardingImage deleteOnboardImageInfoById(
      BetPackOnboarding betPackOnboarding, String imageId) {

    Optional<OnboardingImage> maybeEntity =
        betPackOnboarding.getImages().stream()
            .filter(obj -> obj.getId().toString().equals(imageId))
            .findFirst();

    if (maybeEntity.isPresent()) {
      handleRemoveFile(
          betPackOnboarding.getBrand(), maybeEntity.get().getOnboardImageDetails().relativePath());
      betPackOnboarding.getImages().remove(maybeEntity.get());
      save(betPackOnboarding);
      return maybeEntity.get();
    } else throw new BetPackMarketPlaceException("Image Id : " + imageId + " doesn't exist");
  }

  @FortifyXSSValidate("return")
  public List<BetPackOnboarding> getBpmpOnboarding(String brand) {

    return repository.findByBrand(brand);
  }

  @FortifyXSSValidate("return")
  public BetPackOnboarding getBpmpOnboardingById(String onboardingId) {
    return repository.findById(onboardingId).orElseThrow(NotFoundException::new);
  }

  public void deleteBpmpOnboardingById(String id) {

    onboardingRepository.deleteById(id);
  }

  public Optional<BetPackOnboarding> checkIfBpmpOnboardingExists(String id) {

    return onboardingRepository.findById(id);
  }
}
