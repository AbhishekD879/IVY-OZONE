package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.fortify.annotations.FortifyXSSValidate;
import com.ladbrokescoral.oxygen.cms.api.dto.ConfigDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ConfigItemDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfiguration;
import com.ladbrokescoral.oxygen.cms.api.exception.ElementAlreadyExistException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.mapping.SystemConfigurationMapper;
import com.ladbrokescoral.oxygen.cms.api.service.ConfigsService;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class Configurations extends AbstractCrudController<SystemConfiguration> {

  private final ConfigsService configsService;

  @Autowired
  public Configurations(ConfigsService configsService) {
    super(configsService);
    this.configsService = configsService;
  }

  @FortifyXSSValidate("return")
  @PostMapping("configuration")
  public ResponseEntity<ConfigDto> create(@RequestBody @Validated ConfigDto entity) {
    List<SystemConfiguration> newConfigs =
        SystemConfigurationMapper.INSTANCE.toSystemConfigs(entity).stream()
            .map(this::createEntity)
            .collect(Collectors.toList());
    return ResponseEntity.status(HttpStatus.CREATED)
        .body(SystemConfigurationMapper.INSTANCE.toConfigDto(entity.getBrand(), newConfigs));
  }

  @Override
  protected SystemConfiguration createEntity(SystemConfiguration entity) {
    Optional<SystemConfiguration> existEntity =
        configsService.findElementByBrandAndName(entity.getBrand(), entity.getName());
    return entity.isOverwrite() && existEntity.isPresent()
        ? super.update(existEntity.get().getId(), entity)
        : super.createEntity(entity);
  }

  @GetMapping("configuration")
  public List<ConfigDto> getAll() {
    return super.readAll().stream()
        .collect(Collectors.groupingBy(SystemConfiguration::getBrand))
        .entrySet()
        .stream()
        .map(e -> SystemConfigurationMapper.INSTANCE.toConfigDto(e.getKey(), e.getValue()))
        .collect(Collectors.toList());
  }

  @GetMapping("configuration/brand/{brand}")
  public ConfigDto readAndMap(@PathVariable String brand) {
    return Optional.ofNullable(
            SystemConfigurationMapper.INSTANCE.toConfigDto(brand, super.readByBrand(brand)))
        .orElseThrow(NotFoundException::new);
  }

  @DeleteMapping("configuration/brand/{brand}")
  @Override
  public ResponseEntity<SystemConfiguration> delete(@PathVariable String brand) {
    configsService.deleteAllByBrand(brand);
    return ResponseEntity.noContent().build();
  }

  @PostMapping("configuration/brand/{brand}/element")
  public ConfigItemDto createElement(
      @PathVariable String brand, @RequestBody ConfigItemDto element) {
    configsService
        .findElementByBrandAndName(brand, element.getName())
        .ifPresent(
            (SystemConfiguration entity) -> {
              throw new ElementAlreadyExistException();
            });

    SystemConfiguration systemConfig =
        SystemConfigurationMapper.INSTANCE.toSystemConfig(brand, element);
    return SystemConfigurationMapper.INSTANCE.toConfigItemDto(super.createEntity(systemConfig));
  }

  @PutMapping("configuration/brand/{brand}/element/{elementId}")
  public ConfigItemDto updateElement(
      @PathVariable String brand,
      @PathVariable String elementId,
      @RequestBody ConfigItemDto element) {
    SystemConfiguration updated =
        super.update(elementId, SystemConfigurationMapper.INSTANCE.toSystemConfig(brand, element));
    return SystemConfigurationMapper.INSTANCE.toConfigItemDto(updated);
  }

  @DeleteMapping("configuration/brand/{brand}/element/{elementId}")
  public ResponseEntity<SystemConfiguration> deleteElement(
      @PathVariable String brand, @PathVariable String elementId) {
    return super.delete(elementId);
  }
}
