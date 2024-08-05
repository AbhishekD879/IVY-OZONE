package com.ladbrokescoral.oxygen.cms.api.controller.private_api.onboarding;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.MyStableOnboardingDto;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.AbstractCrudController;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.MyStableOnboarding;
import com.ladbrokescoral.oxygen.cms.api.exception.MyStableOnboardingException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.MyStableOnboardingService;
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
public class MyStableOnboardingController extends AbstractCrudController<MyStableOnboarding> {
  private final MyStableOnboardingService service;
  private final ModelMapper mapper;

  private static final String ERROR_MESSAGE = "Image upload failed!";

  MyStableOnboardingController(MyStableOnboardingService onboardingService, ModelMapper mapper) {
    super(onboardingService);
    this.mapper = mapper;
    this.service = onboardingService;
  }

  @PostMapping("/my-stable/image")
  public ResponseEntity<MyStableOnboardingDto> createWithImage(
      @ModelAttribute @Valid MyStableOnboardingDto myStableOnboardingDto) {
    Optional<MyStableOnboardingDto> mappedDto = Optional.empty();
    try {
      MyStableOnboarding myStableOnboarding =
          mapper.map(myStableOnboardingDto, MyStableOnboarding.class);

      mappedDto =
          Optional.of(
                  service.attachImage(myStableOnboarding, myStableOnboardingDto.getOnboardImg()))
              .map(
                  (Optional<MyStableOnboarding> onboarding) -> {
                    MyStableOnboarding savedEntity = super.create(myStableOnboarding).getBody();
                    return mapper.map(savedEntity, MyStableOnboardingDto.class);
                  });
    } catch (MyStableOnboardingException ex) {
      log.error("Exception : {}, due to {}", ex.getMessage(), ex);
      throw new MyStableOnboardingException("Error occurred while creating MyStable onboarding");
    }
    return ResponseEntity.status(HttpStatus.CREATED).body(mappedDto.get());
  }

  @PostMapping("my-stable/{id}")
  public ResponseEntity<MyStableOnboardingDto> saveWithId(
      @PathVariable String id, @RequestBody MyStableOnboardingDto myStableOnboardingDto) {

    Optional<MyStableOnboarding> myStableOnboarding = service.findOne(id);
    MyStableOnboardingDto mappedDtoObject = null;
    mappedDtoObject =
        myStableOnboarding
            .map(
                (MyStableOnboarding onboarding) -> {
                  MyStableOnboarding mappedObject =
                      mapper.map(myStableOnboardingDto, MyStableOnboarding.class);
                  mappedObject = service.save(mappedObject);
                  return mapper.map(mappedObject, MyStableOnboardingDto.class);
                })
            .orElseThrow(() -> new NotFoundException("Entity with id " + id + " doesn't exist"));
    return new ResponseEntity<>(mappedDtoObject, HttpStatus.CREATED);
  }

  @PutMapping("/my-stable/{id}")
  public MyStableOnboardingDto update(
      @PathVariable String id, @RequestBody MyStableOnboardingDto myStableOnboardingDto) {
    MyStableOnboarding myStableOnboarding =
        mapper.map(myStableOnboardingDto, MyStableOnboarding.class);
    MyStableOnboarding updatedEntity = super.update(id, myStableOnboarding);
    return mapper.map(updatedEntity, MyStableOnboardingDto.class);
  }

  @GetMapping("/my-stable/brand/{brand}")
  public ResponseEntity<MyStableOnboarding> findAllByBrand(@PathVariable String brand) {
    Optional<MyStableOnboarding> myStableOnboarding = service.readByBrand(brand);
    if (myStableOnboarding.isPresent()) {

      return new ResponseEntity<>(myStableOnboarding.get(), HttpStatus.OK);
    } else {
      return new ResponseEntity<>(new MyStableOnboarding(), HttpStatus.NO_CONTENT);
    }
  }

  @GetMapping("/my-stable/{id}")
  public MyStableOnboardingDto findById(@PathVariable String id) {
    MyStableOnboarding myStableOnboarding = super.read(id);

    return mapper.map(myStableOnboarding, MyStableOnboardingDto.class);
  }

  @DeleteMapping("/my-stable/{id}")
  public void deleteById(@PathVariable String id) {
    super.delete(id);
  }

  @DeleteMapping("/my-stable/{id}/images")
  public ResponseEntity<MyStableOnboardingDto> removeImageById(@PathVariable("id") String id) {
    try {
      MyStableOnboardingDto myStableOnboardingDto =
          service
              .findOne(id)
              .map(
                  (MyStableOnboarding onboarding) -> {
                    service
                        .removeImage(onboarding)
                        .ifPresent(onboardingVal -> onboarding.setOnboardImageDetails(null));
                    return mapper.map(service.save(onboarding), MyStableOnboardingDto.class);
                  })
              .orElseThrow(() -> new NotFoundException("Entity with " + id + " does not exist"));
      return new ResponseEntity<>(myStableOnboardingDto, HttpStatus.OK);
    } catch (Exception e) {
      log.error("Exception occured while deleting : {}", e.getMessage());
      throw new MyStableOnboardingException(ERROR_MESSAGE);
    }
  }

  @PutMapping("/my-stable/{id}/image")
  public ResponseEntity<MyStableOnboardingDto> updateImageById(
      @PathVariable("id") String id, @Valid @ModelAttribute MyStableOnboardingDto onboardingDto) {
    MyStableOnboardingDto mappedDtoObject = null;

    try {
      Optional<MyStableOnboarding> existingEntity = service.findOne(id);
      mappedDtoObject =
          existingEntity
              .map(
                  (MyStableOnboarding onboarding) -> {
                    MyStableOnboarding returnedEntity =
                        service.updateOnboardingImage(existingEntity.get(), onboardingDto);
                    returnedEntity = service.save(returnedEntity);
                    return mapper.map(returnedEntity, MyStableOnboardingDto.class);
                  })
              .orElseThrow(
                  () -> new MyStableOnboardingException("Entity with id " + id + " not found"));

    } catch (MyStableOnboardingException e) {
      log.error("Exception encountered {}", e.getMessage());
      throw new MyStableOnboardingException("Image upload failed");
    }
    return new ResponseEntity<>(mappedDtoObject, HttpStatus.OK);
  }
}
