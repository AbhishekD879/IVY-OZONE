package com.ladbrokescoral.oxygen.cms.api.controller.private_api.onboarding;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.CrcOnBoardingDto;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.AbstractCrudController;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CrcOnBoarding;
import com.ladbrokescoral.oxygen.cms.api.exception.CrcOnBoardingException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.CrcOnBoardingService;
import java.util.Optional;
import javax.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
@Validated
@Slf4j
public class CrcOnBoardingController extends AbstractCrudController<CrcOnBoarding> {
  private final CrcOnBoardingService service;
  private final ModelMapper mapper;

  private static final String ERROR_MESSAGE = "Image upload failed!";

  CrcOnBoardingController(CrcOnBoardingService crconboardingService, ModelMapper mapper) {
    super(crconboardingService);
    this.mapper = mapper;
    this.service = crconboardingService;
  }

  @PostMapping("/crc-onboarding/image")
  public ResponseEntity<CrcOnBoardingDto> createWithImage(
      @ModelAttribute @Valid CrcOnBoardingDto crcOnboardingDto) {
    Optional<CrcOnBoardingDto> mappedDto = Optional.empty();
    try {
      CrcOnBoarding crcOnboarding = mapper.map(crcOnboardingDto, CrcOnBoarding.class);

      mappedDto =
          Optional.of(service.attachImage(crcOnboarding, crcOnboardingDto.getOnboardImg()))
              .map(
                  (Optional<CrcOnBoarding> crconboarding) -> {
                    CrcOnBoarding savedEntity = super.create(crcOnboarding).getBody();
                    return mapper.map(savedEntity, CrcOnBoardingDto.class);
                  });
    } catch (CrcOnBoardingException ex) {
      log.info("Exception : {}, due to {}", ex.getMessage(), ex);
      throw new CrcOnBoardingException("Error occurred while creating MyStable onboarding");
    }
    return ResponseEntity.status(HttpStatus.CREATED).body(mappedDto.get());
  }

  @PostMapping("crc-onboarding/{id}")
  public ResponseEntity<CrcOnBoardingDto> saveWithId(
      @PathVariable String id, @RequestBody CrcOnBoardingDto crcOnboardingDto) {

    Optional<CrcOnBoarding> crcOnboarding = service.findOne(id);
    CrcOnBoardingDto mappedDtoObject = null;
    mappedDtoObject =
        crcOnboarding
            .map(
                (CrcOnBoarding crconboarding) -> {
                  CrcOnBoarding mappedObject = mapper.map(crcOnboardingDto, CrcOnBoarding.class);
                  mappedObject = service.save(mappedObject);
                  return mapper.map(mappedObject, CrcOnBoardingDto.class);
                })
            .orElseThrow(() -> new NotFoundException("Entity with id " + id + " doesn't exist"));
    return new ResponseEntity<>(mappedDtoObject, HttpStatus.CREATED);
  }

  @PutMapping("/crc-onboarding/{id}")
  public CrcOnBoardingDto update(
      @PathVariable String id, @RequestBody CrcOnBoardingDto crcOnboardingDto) {
    CrcOnBoarding crcOnboarding = mapper.map(crcOnboardingDto, CrcOnBoarding.class);
    CrcOnBoarding updatedEntity = super.update(id, crcOnboarding);
    return mapper.map(updatedEntity, CrcOnBoardingDto.class);
  }

  @GetMapping("/crc-onboarding/brand/{brand}")
  public ResponseEntity<CrcOnBoardingDto> findAllByBrand(@PathVariable String brand) {
    CrcOnBoarding crcOnboarding = service.readByBrand(brand).orElse(null);

    if (crcOnboarding != null) {
      CrcOnBoardingDto dto = mapper.map(crcOnboarding, CrcOnBoardingDto.class);
      return new ResponseEntity<>(dto, HttpStatus.OK);
    } else {
      return new ResponseEntity<>(new CrcOnBoardingDto(), HttpStatus.NO_CONTENT);
    }
  }

  @GetMapping("/crc-onboarding/{id}")
  public CrcOnBoardingDto findById(@PathVariable String id) {
    CrcOnBoarding crcOnboarding = super.read(id);

    return mapper.map(crcOnboarding, CrcOnBoardingDto.class);
  }

  @DeleteMapping("/crc-onboarding/{id}")
  public void deleteById(@PathVariable String id) {
    super.delete(id);
  }

  @DeleteMapping("/crc-onboarding/{id}/images")
  public ResponseEntity<CrcOnBoardingDto> removeImageById(@PathVariable("id") String id) {
    try {
      CrcOnBoardingDto crcOnboardingDto =
          service
              .findOne(id)
              .map(
                  (CrcOnBoarding crconboarding) -> {
                    service
                        .removeImage(crconboarding)
                        .ifPresent(onboardingVal -> crconboarding.setOnboardImageDetails(null));
                    return mapper.map(service.save(crconboarding), CrcOnBoardingDto.class);
                  })
              .orElseThrow(() -> new NotFoundException("Entity with " + id + " does not exist"));
      return new ResponseEntity<>(crcOnboardingDto, HttpStatus.OK);
    } catch (Exception e) {
      log.info("Exception occured while deleting : " + e.getMessage());
      throw new CrcOnBoardingException(ERROR_MESSAGE);
    }
  }

  @PutMapping("/crc-onboarding/{id}/image")
  public ResponseEntity<CrcOnBoardingDto> updateImageById(
      @PathVariable("id") String id, @ModelAttribute CrcOnBoardingDto crconboardingDto) {
    CrcOnBoardingDto mappedDtoObject = null;

    try {
      Optional<CrcOnBoarding> existingEntity = service.findOne(id); // check
      mappedDtoObject =
          existingEntity
              .map(
                  (CrcOnBoarding crconboarding) -> {
                    CrcOnBoarding returnedEntity =
                        service.updateOnboardingImage(existingEntity.get(), crconboardingDto);
                    returnedEntity = service.save(returnedEntity);
                    return mapper.map(returnedEntity, CrcOnBoardingDto.class);
                  })
              .orElseThrow(() -> new CrcOnBoardingException("Entity with id " + id + " not found"));

    } catch (CrcOnBoardingException e) {
      log.info("Exception encountered " + e.getMessage());
      throw new CrcOnBoardingException("Image upload failed");
    }
    return new ResponseEntity<>(mappedDtoObject, HttpStatus.OK);
  }
}
