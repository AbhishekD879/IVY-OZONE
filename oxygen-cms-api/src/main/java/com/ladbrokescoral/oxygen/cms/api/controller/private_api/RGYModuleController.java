package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.RGYModule;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYModuleEntity;
import com.ladbrokescoral.oxygen.cms.api.service.RGYConfigUploadService;
import com.ladbrokescoral.oxygen.cms.api.service.RGYModuleService;
import java.util.Collections;
import java.util.List;
import org.springframework.beans.BeanUtils;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RGYModuleController extends AbstractSortableController<RGYModuleEntity> {

  private final RGYModuleService rgyModuleService;
  private RGYConfigUploadService rgyConfigUploadService;

  public RGYModuleController(
      RGYModuleService rgyModuleService, RGYConfigUploadService rgyConfigUploadService) {
    super(rgyModuleService);
    this.rgyModuleService = rgyModuleService;
    this.rgyConfigUploadService = rgyConfigUploadService;
  }

  @PostMapping("rgyModule")
  public ResponseEntity<RGYModuleEntity> create(@RequestBody RGYModule rgyModuleRequest) {
    RGYModuleEntity rgyModuleEntity = new RGYModuleEntity();
    BeanUtils.copyProperties(rgyModuleRequest, rgyModuleEntity);
    rgyModuleEntity = super.create(rgyModuleEntity).getBody();
    rgyModuleService.getRGYModuleInfoWithSubModules(rgyModuleEntity);
    rgyConfigUploadService.uploadToS3(rgyModuleRequest.getBrand());
    return new ResponseEntity<>(rgyModuleEntity, HttpStatus.OK);
  }

  @GetMapping("rgyModule/{id}")
  @Override
  public RGYModuleEntity read(@PathVariable String id) {
    RGYModuleEntity rgyModuleEntity = new RGYModuleEntity();
    RGYModule rgyModule = rgyModuleService.findByModuleId(id);
    BeanUtils.copyProperties(rgyModule, rgyModuleEntity);
    return rgyModuleEntity;
  }

  @PutMapping("rgyModule/{id}")
  public RGYModuleEntity update(@PathVariable String id, @RequestBody RGYModule rgyModuleRequest) {
    RGYModuleEntity rgyModuleEntity = new RGYModuleEntity();
    BeanUtils.copyProperties(rgyModuleRequest, rgyModuleEntity);
    rgyModuleEntity = super.update(id, rgyModuleEntity);
    RGYModule rgyModule = rgyModuleService.findByModuleId(id);
    BeanUtils.copyProperties(rgyModule, rgyModuleEntity);
    rgyModuleEntity.setSubModuleIds(Collections.emptyList());
    rgyConfigUploadService.uploadToS3(rgyModuleRequest.getBrand());
    return rgyModuleEntity;
  }

  @DeleteMapping("rgyModule/{brand}/{id}")
  public ResponseEntity<RGYModuleEntity> delete(
      @PathVariable("brand") String brand, @PathVariable("id") String rgyModuleId) {
    ResponseEntity<RGYModuleEntity> response = rgyModuleService.deleteById(rgyModuleId);
    rgyConfigUploadService.uploadToS3(brand);
    return response;
  }

  @GetMapping("rgyModule/brand/{brand}")
  @Override
  public List<RGYModuleEntity> readByBrand(@PathVariable String brand) {
    return rgyModuleService.readByBrand(brand);
  }
}
