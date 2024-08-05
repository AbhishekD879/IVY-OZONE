package com.ladbrokescoral.oxygen.cms.api.controller.private_api.onboarding;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.FirstBetPlaceTutorialDto;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.AbstractCrudController;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.FirstBetPlaceTutorial;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.FirstBetPlaceTutorialService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import javax.validation.Valid;
import org.modelmapper.ModelMapper;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
@Validated
public class FirstBetPlaceTutorials extends AbstractCrudController<FirstBetPlaceTutorial> {

  private final FirstBetPlaceTutorialService firstBetPlaceTutorialService;
  private final ModelMapper mapper;

  protected FirstBetPlaceTutorials(
      FirstBetPlaceTutorialService firstBetPlaceTutorialService, ModelMapper mapper) {
    super(firstBetPlaceTutorialService);
    this.mapper = mapper;
    this.firstBetPlaceTutorialService = firstBetPlaceTutorialService;
  }

  @PostMapping("/first-bet-place-tutorial")
  public ResponseEntity<FirstBetPlaceTutorial> create(
      @Valid @RequestBody FirstBetPlaceTutorialDto firstBetPlaceTutorialDto) {
    FirstBetPlaceTutorial firstBetPlaceTutorial =
        mapper.map(firstBetPlaceTutorialDto, FirstBetPlaceTutorial.class);
    return super.create(firstBetPlaceTutorial);
  }

  @PutMapping("/first-bet-place-tutorial/{id}")
  public FirstBetPlaceTutorial update(
      @PathVariable String id,
      @Valid @RequestBody FirstBetPlaceTutorialDto firstBetPlaceTutorialDto) {

    FirstBetPlaceTutorial firstBetPlaceTutorial =
        mapper.map(firstBetPlaceTutorialDto, FirstBetPlaceTutorial.class);
    return super.update(id, firstBetPlaceTutorial);
  }

  @GetMapping("/first-bet-place-tutorial/brand/{brand}")
  public FirstBetPlaceTutorial findAllByBrand(@PathVariable @Brand String brand) {
    return firstBetPlaceTutorialService.readByBrand(brand).orElseThrow(NotFoundException::new);
  }

  @GetMapping("/first-bet-place-tutorial/{id}")
  public FirstBetPlaceTutorial findById(@PathVariable String id) {
    return super.read(id);
  }

  @DeleteMapping("/first-bet-place-tutorial/{id}")
  public void deleteById(@PathVariable String id) {
    super.delete(id);
  }

  @PostMapping("/first-bet-place-tutorial/{id}/image")
  public ResponseEntity<FirstBetPlaceTutorial> addCSWImg(
      @PathVariable("id") String id,
      @ValidFileType({"png", "jpg", "jpeg", "svg"}) @RequestParam("file") MultipartFile file) {
    FirstBetPlaceTutorial firstBetPlaceTutorial =
        firstBetPlaceTutorialService.findOne(id).orElseThrow(NotFoundException::new);
    return firstBetPlaceTutorialService
        .attachImage(firstBetPlaceTutorial, file)
        .map(
            (FirstBetPlaceTutorial csw) -> {
              FirstBetPlaceTutorial saved = firstBetPlaceTutorialService.save(csw);
              return new ResponseEntity<>(saved, HttpStatus.OK);
            })
        .orElseGet(failedToUpdateImage());
  }

  @DeleteMapping("/first-bet-place-tutorial/{id}/image")
  public ResponseEntity<FirstBetPlaceTutorial> removeImage(@PathVariable("id") String id) {
    FirstBetPlaceTutorial firstBetPlaceTutorial =
        firstBetPlaceTutorialService.findOne(id).orElseThrow(NotFoundException::new);

    return firstBetPlaceTutorialService
        .removeImage(firstBetPlaceTutorial)
        .map(
            (FirstBetPlaceTutorial csw) -> {
              FirstBetPlaceTutorial saved = firstBetPlaceTutorialService.save(csw);
              return new ResponseEntity<>(saved, HttpStatus.OK);
            })
        .orElseGet(failedToUpdateImage());
  }
}
