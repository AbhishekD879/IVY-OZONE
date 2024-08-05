package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.RGYConfigRequest;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYConfigurationEntity;
import com.ladbrokescoral.oxygen.cms.api.service.RGYConfigService;
import com.ladbrokescoral.oxygen.cms.api.service.RGYConfigUploadService;
import java.util.List;
import java.util.Objects;
import org.springframework.beans.BeanUtils;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RGYConfigController extends AbstractSortableController<RGYConfigurationEntity> {

  private RGYConfigService rgyConfigService;
  private RGYConfigUploadService rgyConfigUploadService;

  public RGYConfigController(
      RGYConfigService rgyConfigService, RGYConfigUploadService rgyConfigUploadService) {
    super(rgyConfigService);
    this.rgyConfigService = rgyConfigService;
    this.rgyConfigUploadService = rgyConfigUploadService;
  }

  @PostMapping("rgyConfig")
  public ResponseEntity<RGYConfigurationEntity> create(
      @RequestBody RGYConfigRequest rgyConfigRequest) {
    RGYConfigurationEntity rgyConfigurationEntity;
    RGYConfigurationEntity existingConfig =
        rgyConfigService.findByBrandAndReasonCodeAndRiskLevelCode(
            rgyConfigRequest.getBrand(),
            rgyConfigRequest.getReasonCode(),
            rgyConfigRequest.getRiskLevelCode());
    if (Objects.nonNull(existingConfig)) {
      List<String> existingModuleIds = existingConfig.getModuleIds();
      List<String> moduleIds = rgyConfigRequest.getModuleIds();
      moduleIds.removeAll(existingModuleIds);
      if (!CollectionUtils.isEmpty(moduleIds)) {
        existingModuleIds.addAll(moduleIds);
        existingConfig.setModuleIds(existingModuleIds);
        rgyConfigurationEntity = super.update(existingConfig.getId(), existingConfig);
      } else {
        rgyConfigurationEntity = existingConfig;
      }
    } else {
      rgyConfigurationEntity = new RGYConfigurationEntity();
      BeanUtils.copyProperties(rgyConfigRequest, rgyConfigurationEntity);
      rgyConfigurationEntity = super.create(rgyConfigurationEntity).getBody();
    }
    rgyConfigService.getAndMapRGYModules(rgyConfigurationEntity);
    rgyConfigUploadService.uploadToS3(rgyConfigRequest.getBrand());
    return new ResponseEntity<>(rgyConfigurationEntity, HttpStatus.OK);
  }

  @GetMapping("rgyConfig/{id}")
  public ResponseEntity<RGYConfigurationEntity> getById(@PathVariable String id) {
    return rgyConfigService.getById(id);
  }

  @PutMapping("rgyConfig/{id}")
  public RGYConfigurationEntity update(
      @PathVariable String id, @RequestBody RGYConfigRequest rgyConfigRequest) {
    RGYConfigurationEntity rgyConfigurationEntity = new RGYConfigurationEntity();
    BeanUtils.copyProperties(rgyConfigRequest, rgyConfigurationEntity);
    RGYConfigurationEntity response = super.update(id, rgyConfigurationEntity);
    rgyConfigService.getAndMapRGYModules(response);
    rgyConfigUploadService.uploadToS3(rgyConfigRequest.getBrand());
    return response;
  }

  @DeleteMapping("rgyConfig/{brand}/{id}")
  public ResponseEntity<RGYConfigurationEntity> delete(
      @PathVariable String brand, @PathVariable String id) {
    ResponseEntity<RGYConfigurationEntity> response = super.delete(id);
    rgyConfigUploadService.uploadToS3(brand);
    return response;
  }

  @GetMapping("rgyConfig/brand/{brand}")
  @Override
  public List<RGYConfigurationEntity> readByBrand(@PathVariable String brand) {
    return rgyConfigService.readByBrand(brand);
  }
}
