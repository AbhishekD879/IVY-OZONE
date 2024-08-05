package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.RGYModule;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYConfigurationEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.RGYConfigRepository;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Service
public class RGYConfigService extends SortableService<RGYConfigurationEntity> {
  private RGYConfigRepository rgyConfigRepository;
  private RGYModuleService rgyModuleService;

  public RGYConfigService(
      RGYConfigRepository rgyConfigRepository, RGYModuleService rgyModuleService) {
    super(rgyConfigRepository);
    this.rgyConfigRepository = rgyConfigRepository;
    this.rgyModuleService = rgyModuleService;
  }

  public ResponseEntity<RGYConfigurationEntity> getById(String rgYellowConfigId) {
    Optional<RGYConfigurationEntity> rgYellowEntityInfo =
        rgyConfigRepository.findById(rgYellowConfigId);
    if (rgYellowEntityInfo.isPresent()) {
      RGYConfigurationEntity rgyConfigurationEntity = rgYellowEntityInfo.get();
      getAndMapRGYModules(rgyConfigurationEntity);
      return new ResponseEntity<>(rgyConfigurationEntity, HttpStatus.OK);
    } else {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
  }

  public List<RGYConfigurationEntity> readByBrand(String brand) {
    List<RGYConfigurationEntity> rgYellowConfig = rgyConfigRepository.findByBrand(brand);
    if (!CollectionUtils.isEmpty(rgYellowConfig)) {
      rgYellowConfig.forEach(this::getAndMapRGYModules);
    } else {
      log.error("RGY configuration is not available for {}", brand);
    }
    return rgYellowConfig;
  }

  public RGYConfigurationEntity findByBrandAndReasonCodeAndRiskLevelCode(
      String brand, int reasonCode, int riskLevelCode) {
    return rgyConfigRepository.findByBrandAndReasonCodeAndRiskLevelCode(
        brand, reasonCode, riskLevelCode);
  }

  public void getAndMapRGYModules(RGYConfigurationEntity rgyConfigurationEntity) {
    List<RGYModule> rgyModules = new ArrayList<>();
    if (!CollectionUtils.isEmpty(rgyConfigurationEntity.getModuleIds())) {
      rgyConfigurationEntity
          .getModuleIds()
          .forEach(
              (String moduleId) -> {
                RGYModule rgyModule = rgyModuleService.findByModuleId(moduleId);
                if (Objects.nonNull(rgyModule)) {
                  rgyModules.add(rgyModule);
                }
              });
    }
    rgyConfigurationEntity.setModules(rgyModules);
    rgyConfigurationEntity.setModuleIds(Collections.emptyList());
  }

  public List<RGYConfigurationEntity> readByBrandAndBonusSuppressionTrue(String brand) {
    List<RGYConfigurationEntity> rgYellowConfig =
        rgyConfigRepository.findByBrandAndBonusSuppressionTrue(brand);
    if (!CollectionUtils.isEmpty(rgYellowConfig)) {
      rgYellowConfig.forEach(this::getAndMapRGYModules);
    } else {
      log.error("RGY configuration is not available for {}", brand);
    }
    return rgYellowConfig;
  }
}
