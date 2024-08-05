package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.fortify.annotations.FortifyXSSValidate;
import com.ladbrokescoral.oxygen.cms.api.dto.BetPackOnboardingDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OnboardingImageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackOnboarding;
import com.ladbrokescoral.oxygen.cms.api.entity.OnboardingImage;
import com.ladbrokescoral.oxygen.cms.api.exception.BetPackMarketPlaceException;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceOnboardingService;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.owasp.encoder.Encode;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@Slf4j
public class BPMPOnBoardingController extends AbstractSortableController<BetPackOnboarding> {

  private BetPackMarketPlaceOnboardingService onBoardingService;
  private ModelMapper modelMapper;

  public BPMPOnBoardingController(
      BetPackMarketPlaceOnboardingService onBoardingService, ModelMapper modelMapper) {
    super(onBoardingService);
    this.onBoardingService = onBoardingService;
    this.modelMapper = modelMapper;
  }

  @FortifyXSSValidate("return")
  @PostMapping("bet-pack/onboarding")
  public ResponseEntity<BetPackOnboarding> createBpmpOnboarding(
      @ModelAttribute @Valid BetPackOnboardingDto betPackOnboardingDto) {

    String onboardingId = null;
    try {
      BetPackOnboarding betPackOnboarding =
          modelMapper.map(betPackOnboardingDto, BetPackOnboarding.class);

      BetPackOnboarding betPackOnBoardingSavedEntity = super.create(betPackOnboarding).getBody();
      onboardingId = onBoardingService.getBpmpOnboardingId(betPackOnBoardingSavedEntity);

      return ResponseEntity.status(HttpStatus.CREATED)
          .body(
              onBoardingService.uploadOnboardingImage(
                  betPackOnBoardingSavedEntity, betPackOnboardingDto.getImages()));

    } catch (FileUploadException ex) {
      log.info("File Upload Exception : {}", ex.getMessage());
      super.delete(onboardingId);
      throw new BetPackMarketPlaceException("File Upload Failed");
    } catch (Exception ex) {
      log.info("Exception : {}, due to {}", ex.getMessage(), ex);
      super.delete(onboardingId);
      throw new BetPackMarketPlaceException("Error occurred while creating bet pack on boarding");
    }
  }

  @GetMapping("bet-pack/onboarding/brand/{brand}")
  public ResponseEntity<BetPackOnboarding> getBpmpOnboardingByBrand(@PathVariable String brand) {
    List<BetPackOnboarding> betPackOnboardings = onBoardingService.getBpmpOnboarding(brand);
    if (!betPackOnboardings.isEmpty()) {
      return new ResponseEntity<>(betPackOnboardings.get(0), HttpStatus.OK);
    } else {
      return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
  }

  @PutMapping("bet-pack/onboarding/{id}")
  public ResponseEntity<BetPackOnboardingDto> updateBpmpOnboarding(
      @PathVariable("id") String id,
      @Valid @ModelAttribute BetPackOnboardingDto betPackOnboardingDto) {
    String idValue = Encode.forJava(id);
    Optional<BetPackOnboarding> maybeEntity = Optional.empty();
    try {
      maybeEntity = onBoardingService.checkIfBpmpOnboardingExists(idValue);
      if (!maybeEntity.isPresent()) throw new NotFoundException("Data not found");
      BetPackOnboarding betPackOnboarding =
          modelMapper.map(betPackOnboardingDto, BetPackOnboarding.class);
      BetPackOnboarding betPackOnBoardingUpdatedEntity = super.update(idValue, betPackOnboarding);
      BetPackOnboardingDto dtoUpdated =
          modelMapper.map(
              onBoardingService.uploadOnboardingImage(
                  betPackOnBoardingUpdatedEntity, betPackOnboardingDto.getImages()),
              BetPackOnboardingDto.class);
      return new ResponseEntity<>(dtoUpdated, HttpStatus.OK);
    } catch (FileUploadException ex) {
      log.info("File Upload Exception : {}", ex.getMessage());
      maybeEntity.ifPresent(
          betPackOnboarding -> super.update(betPackOnboarding.getId(), betPackOnboarding));
      throw new BetPackMarketPlaceException("File Upload Failed");
    } catch (NotFoundException ex) {
      log.info("Entity with id {} doesn't exist, error occurred {} ", idValue, ex.getMessage());
      throw ex;
    } catch (Exception ex) {
      log.info("Exception : {}, due to {}", ex.getMessage(), ex);
      throw new BetPackMarketPlaceException("Error occurred while updating bet pack on boarding");
    }
  }

  @PutMapping("bet-pack/onboarding/{onboarding_id}/images/{image_id}")
  public ResponseEntity<OnboardingImage> updateImageInfo(
      @PathVariable("onboarding_id") String onboardingId,
      @PathVariable("image_id") String imageId,
      @ModelAttribute @Valid OnboardingImageDto onboardingImageDto) {

    onboardingImageDto.setId(imageId);

    Optional<BetPackOnboarding> betPackOnboardingOptioal =
        onBoardingService.checkIfBpmpOnboardingExists(onboardingId);

    if (!betPackOnboardingOptioal.isPresent())
      throw new BetPackMarketPlaceException(
          "BetpackOnboarding with id " + onboardingId + " doesn't exist");

    BetPackOnboarding betPackOnboarding = betPackOnboardingOptioal.get();

    Optional<OnboardingImage> maybeEntity =
        betPackOnboarding.getImages().stream()
            .filter(i -> i.getId().toString().equals(imageId))
            .findFirst();

    if (maybeEntity.isPresent()) {
      return ResponseEntity.status(HttpStatus.OK)
          .body(
              onBoardingService.updateOnboardingImage(
                  betPackOnboarding, onboardingImageDto, maybeEntity.get()));
    } else throw new BetPackMarketPlaceException("Image with id " + imageId + " doesn't exist");
  }

  @DeleteMapping("bet-pack/onboarding/{onboarding_id}/images/{image_id}")
  public ResponseEntity<OnboardingImage> deleteOnboardingImage(
      @PathVariable("onboarding_id") String onboardingId,
      @PathVariable("image_id") String imageId) {

    try {
      BetPackOnboarding betPackOnboarding = onBoardingService.getBpmpOnboardingById(onboardingId);
      return new ResponseEntity<>(
          onBoardingService.deleteOnboardImageInfoById(betPackOnboarding, imageId), HttpStatus.OK);
    } catch (Exception ex) {
      log.info("Error deleting image with id : {} due to the error {}", ex);
      throw ex;
    }
  }

  @DeleteMapping("bet-pack/onboarding/{id}")
  public ResponseEntity<String> deleteById(@PathVariable String id) {

    try {
      onBoardingService.deleteBpmpOnboardingById(id);
      return new ResponseEntity<>(HttpStatus.OK);
    } catch (Exception ex) {
      log.info("Error occurred while deleting, caused by {}", ex.getMessage());
      return new ResponseEntity<>(
          "Error occurred while deleting, caused by " + ex.getMessage(),
          HttpStatus.INTERNAL_SERVER_ERROR);
    }
  }

  @GetMapping("bet-pack/onboarding/{onboardingId}/images/{imageId}")
  public ResponseEntity<OnboardingImage> getBpmpOnboardingById(
      @PathVariable("onboardingId") String onboardingId, @PathVariable("imageId") String imageId) {
    BetPackOnboarding betPackOnboarding = onBoardingService.getBpmpOnboardingById(onboardingId);
    List<OnboardingImage> onboardingImages = betPackOnboarding.getImages();
    Optional<OnboardingImage> onboardingImage =
        onboardingImages.stream().filter(i -> i.getId().toString().equals(imageId)).findFirst();
    if (onboardingImage.isPresent())
      return ResponseEntity.status(HttpStatus.OK).body(onboardingImage.get());
    else throw new BetPackMarketPlaceException("No Data Found for the given Image id: " + imageId);
  }
}
