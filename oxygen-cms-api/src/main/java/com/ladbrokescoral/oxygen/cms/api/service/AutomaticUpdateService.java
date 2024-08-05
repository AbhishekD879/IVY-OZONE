package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.AliasModuleNamesDto;
import com.ladbrokescoral.oxygen.cms.api.dto.AutomaticUpdateDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYModuleEntity;
import java.util.List;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.CollectionUtils;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class AutomaticUpdateService {

  private final RGYModuleService rgyModuleService;

  private final RGYConfigUploadService rgyConfigUploadService;

  public void doUpdate(AutomaticUpdateDto dto) {

    List<RGYModuleEntity> filteredModules =
        this.rgyModuleService.readByBrand(dto.getBrand()).stream()
            .filter(predicate(dto))
            .map(rgyModuleEntity -> this.updateAliasModulesNames(rgyModuleEntity, dto))
            .collect(Collectors.toList());

    if (CollectionUtils.isNotEmpty(filteredModules)) {
      for (RGYModuleEntity entity : filteredModules) {
        this.rgyModuleService.save(entity);
        this.rgyConfigUploadService.uploadToS3(entity.getBrand());
      }
    }
  }

  private Predicate<RGYModuleEntity> predicate(AutomaticUpdateDto dto) {
    return rgyModuleEntity ->
        rgyModuleEntity.getAliasModules().stream()
            .anyMatch(aliasDto -> dto.getId().equalsIgnoreCase(aliasDto.getId()));
  }

  private RGYModuleEntity updateAliasModulesNames(RGYModuleEntity module, AutomaticUpdateDto dto) {

    List<AliasModuleNamesDto> titlesToUpdate = module.getAliasModules();

    for (AliasModuleNamesDto aliasModuleNamesDto : titlesToUpdate) {
      if (dto.getId().equalsIgnoreCase(aliasModuleNamesDto.getId())) {
        aliasModuleNamesDto.setTitle(dto.getUpdatedTitle());
      }
    }
    module.setAliasModules(titlesToUpdate);
    return module;
  }
}
