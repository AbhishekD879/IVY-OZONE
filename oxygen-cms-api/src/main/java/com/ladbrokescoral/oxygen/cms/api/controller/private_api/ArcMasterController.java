package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.ArcMasterDataDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ArcMasterData;
import com.ladbrokescoral.oxygen.cms.api.service.ArcMasterService;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class ArcMasterController implements Abstract {
  private ArcMasterService arcMasterService;

  @Autowired
  public ArcMasterController(ArcMasterService arcMasterService) {
    this.arcMasterService = arcMasterService;
  }

  @PostMapping("arc-master-data")
  public ResponseEntity<ArcMasterData> createMasterData(
      @RequestBody @Valid ArcMasterDataDto arcMasterDataDto) {
    ArcMasterData arcMasterData = new ArcMasterData();
    BeanUtils.copyProperties(arcMasterDataDto, arcMasterData);
    ArcMasterData arcMasterDataResponse =
        arcMasterService.getMasterDataByLineItem(arcMasterData.getMasterLineName());
    if (null == arcMasterDataResponse) {
      return arcMasterService.createMasterData(arcMasterData);
    }
    return new ResponseEntity<>(arcMasterDataResponse, HttpStatus.CONFLICT);
  }

  @PutMapping("arc-master-data/{lineItem}")
  public ResponseEntity<ArcMasterData> updateMasterData(
      @PathVariable String lineItem, @RequestBody @Valid ArcMasterDataDto arcMasterDataDto) {
    ArcMasterData arcMasterData = new ArcMasterData();
    BeanUtils.copyProperties(arcMasterDataDto, arcMasterData);
    ArcMasterData arcMasterDataResponse = arcMasterService.getMasterDataByLineItem(lineItem);
    if (null == arcMasterDataResponse) {
      return new ResponseEntity<>(arcMasterDataResponse, HttpStatus.NOT_FOUND);
    }
    Optional<ArcMasterData> existingEntity = Optional.of(arcMasterDataResponse);
    ArcMasterData updatedArcMasterDataResponse;
    try {
      updatedArcMasterDataResponse = arcMasterService.update(existingEntity, arcMasterData);
    } catch (Exception e) {
      return new ResponseEntity<>(HttpStatus.CONFLICT);
    }
    return new ResponseEntity<>(updatedArcMasterDataResponse, HttpStatus.OK);
  }

  @GetMapping("arc-master-data")
  public List<ArcMasterData> getAll() {
    return arcMasterService.getAllMetadata();
  }

  @GetMapping("arc-master-data/{lineItem}")
  public ArcMasterData getMasterDataByLineItem(@PathVariable String lineItem) {
    return arcMasterService.getMasterDataByLineItem(lineItem);
  }
}
