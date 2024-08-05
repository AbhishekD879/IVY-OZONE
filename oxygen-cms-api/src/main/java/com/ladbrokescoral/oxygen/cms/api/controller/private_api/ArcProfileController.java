package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.ArcProfileDataDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ArcProfile;
import com.ladbrokescoral.oxygen.cms.api.service.ArcProfileService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.beans.BeanUtils;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class ArcProfileController extends AbstractSortableController<ArcProfile> {
  private final ArcProfileService arcProfileService;

  public ArcProfileController(ArcProfileService arcProfileService) {
    super(arcProfileService);
    this.arcProfileService = arcProfileService;
  }

  @PostMapping("arc-profile")
  public ResponseEntity<ArcProfile> createArcProfile(
      @RequestBody @Valid ArcProfileDataDto arcProfileDataDto) {
    ArcProfile entity = new ArcProfile();
    BeanUtils.copyProperties(arcProfileDataDto, entity);
    ArcProfile arcProfile =
        arcProfileService.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
            entity.getBrand(), entity.getModelRiskLevel(), entity.getReasonCode());
    if (null == arcProfile) {
      return super.create(entity);
    }
    return new ResponseEntity<>(arcProfile, HttpStatus.CONFLICT);
  }

  @GetMapping("arc-profile/{id}")
  public ArcProfile readById(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("arc-profiles")
  public List<ArcProfile> readAllArcProfiles() {
    return super.readAll();
  }

  @GetMapping("arc-profiles/brand/{brand}")
  public List<ArcProfile> readArcProfileByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @GetMapping("arc-profile/{brand}/{modelAndRiskLevel}/{reasonCode}")
  public ResponseEntity<ArcProfile> read(
      @PathVariable String brand,
      @PathVariable Integer modelAndRiskLevel,
      @PathVariable Integer reasonCode) {
    ArcProfile arcProfile =
        arcProfileService.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
            brand, modelAndRiskLevel, reasonCode);
    if (null == arcProfile) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
    return new ResponseEntity<>(arcProfile, HttpStatus.OK);
  }

  @DeleteMapping("arc-profile/{id}")
  public ResponseEntity<ArcProfile> deleteById(@PathVariable String id) {
    return super.delete(id);
  }

  @DeleteMapping("arc-profile/{brand}/{modelAndRiskLevel}/{reasonCode}")
  public ResponseEntity<Long> delete(
      @PathVariable String brand,
      @PathVariable Integer modelAndRiskLevel,
      @PathVariable Integer reasonCode) {
    Long deletedStatus =
        arcProfileService.deleteArcProfileByBrandAndModelRiskLevelAndReasonCode(
            brand, modelAndRiskLevel, reasonCode);
    return 1l == deletedStatus
        ? new ResponseEntity<>(deletedStatus, HttpStatus.ACCEPTED)
        : new ResponseEntity<>(deletedStatus, HttpStatus.NOT_FOUND);
  }

  @PutMapping("arc-profiles/{brand}")
  public List<ArcProfile> updateArcProfiles(
      @PathVariable String brand, @RequestBody List<ArcProfileDataDto> arcProfileDataDtos) {
    arcProfileDataDtos.forEach(
        arcProfileDataDto -> {
          ArcProfile entity = new ArcProfile();
          BeanUtils.copyProperties(arcProfileDataDto, entity);
          ArcProfile arcProfile =
              arcProfileService.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
                  brand, arcProfileDataDto.getModelRiskLevel(), arcProfileDataDto.getReasonCode());
          if (null == arcProfile) {
            super.create(entity);
          } else if (arcProfile.getId().equals(entity.getId())) {
            super.update(arcProfile.getId(), entity);
          }
        });
    return super.readByBrand(brand);
  }

  @PostMapping("arc-profiles/{brand}")
  public List<ArcProfile> createArcProfiles(
      @PathVariable String brand, @RequestBody @Valid List<ArcProfileDataDto> arcProfileDataDtos) {
    arcProfileDataDtos.forEach(
        arcProfileDataDto -> {
          ArcProfile entity = new ArcProfile();
          BeanUtils.copyProperties(arcProfileDataDto, entity);
          ArcProfile arcProfile =
              arcProfileService.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
                  brand, arcProfileDataDto.getModelRiskLevel(), arcProfileDataDto.getReasonCode());
          if (null == arcProfile) {
            super.create(entity);
          }
        });
    return super.readByBrand(brand);
  }
}
