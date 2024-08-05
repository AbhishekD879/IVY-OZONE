package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.RGYModule;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYModuleEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.RGYModuleRepository;
import java.util.*;
import org.springframework.beans.BeanUtils;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;

@Service
public class RGYModuleService extends SortableService<RGYModuleEntity> {
  private RGYModuleRepository rgyModuleRepository;

  public RGYModuleService(RGYModuleRepository rgyModuleRepository) {
    super(rgyModuleRepository);
    this.rgyModuleRepository = rgyModuleRepository;
  }

  public List<RGYModuleEntity> readByBrand(String brand) {
    List<RGYModuleEntity> rgyModules = rgyModuleRepository.findByBrand(brand);
    if (!CollectionUtils.isEmpty(rgyModules)) {
      for (RGYModuleEntity rgyModuleEntity : rgyModules) {
        mapSubModulesInfo(rgyModuleEntity);
      }
    }

    return rgyModules;
  }

  public RGYModuleEntity mapSubModulesInfo(RGYModuleEntity rgyModuleEntity) {
    if (rgyModuleEntity.isSubModuleEnabled()
        && !CollectionUtils.isEmpty(rgyModuleEntity.getSubModuleIds())) {
      List<RGYModule> subModules = new ArrayList<>();
      for (String eachSubModuleId : rgyModuleEntity.getSubModuleIds()) {
        RGYModule subModule = findByModuleId(eachSubModuleId);
        if (Objects.nonNull(subModule)) {
          subModules.add(subModule);
        }
      }
      rgyModuleEntity.setSubModules(subModules);
      rgyModuleEntity.setSubModuleIds(Collections.emptyList());
    }
    return rgyModuleEntity;
  }

  public ResponseEntity<RGYModuleEntity> deleteById(String rgyModuleId) {
    Optional<RGYModuleEntity> maybeEntity = rgyModuleRepository.findById(rgyModuleId);
    return maybeEntity
        .map(
            (RGYModuleEntity rgyModuleEntity) -> {
              rgyModuleRepository.deleteById(rgyModuleId);
              return ResponseEntity.noContent().<RGYModuleEntity>build();
            })
        .orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
  }

  public RGYModuleEntity getRGYModuleInfoWithSubModules(RGYModuleEntity rgyModuleEntity) {
    if (StringUtils.hasText(rgyModuleEntity.getId())) {
      RGYModule rgyModule = findByModuleId(rgyModuleEntity.getId());
      BeanUtils.copyProperties(rgyModule, rgyModuleEntity);
    }
    return rgyModuleEntity;
  }

  public RGYModule findByModuleId(String rgyModuleId) {
    RGYModule rgyModule = null;
    Optional<RGYModuleEntity> maybeEntity = rgyModuleRepository.findById(rgyModuleId);
    if (maybeEntity.isPresent()) {
      rgyModule = new RGYModule();
      BeanUtils.copyProperties(maybeEntity.get(), rgyModule);
      if (rgyModule.isSubModuleEnabled() && !CollectionUtils.isEmpty(rgyModule.getSubModuleIds())) {
        List<RGYModule> subModules = new ArrayList<>();
        rgyModule.setSubModules(subModules);
        for (String eachSubModuleId : rgyModule.getSubModuleIds()) {
          getSubModuleInfo(eachSubModuleId, rgyModule);
        }
      }
      rgyModule.setSubModuleIds(Collections.emptyList());
    }
    return rgyModule;
  }

  public RGYModule getSubModuleInfo(String eachSubModuleId, RGYModule rgyModule) {
    Optional<RGYModuleEntity> subModuleEntity = rgyModuleRepository.findById(eachSubModuleId);
    if (subModuleEntity.isPresent()) {
      RGYModule subModule = new RGYModule();
      BeanUtils.copyProperties(subModuleEntity.get(), subModule);
      subModule.setSubModuleIds(Collections.emptyList());
      subModule.setSubModules(Collections.emptyList());
      rgyModule.getSubModules().add(subModule);
    }
    return rgyModule;
  }
}
