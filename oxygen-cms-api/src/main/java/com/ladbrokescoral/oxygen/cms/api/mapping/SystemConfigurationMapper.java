package com.ladbrokescoral.oxygen.cms.api.mapping;

import static java.util.Comparator.*;

import com.fortify.annotations.FortifyXSSValidate;
import com.ladbrokescoral.oxygen.cms.api.dto.ConfigDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ConfigItemDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ConfigItemPropertyDto;
import com.ladbrokescoral.oxygen.cms.api.dto.StructureDto;
import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfigProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfiguration;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;
import org.springframework.util.CollectionUtils;

@Mapper
public interface SystemConfigurationMapper {

  SystemConfigurationMapper INSTANCE = Mappers.getMapper(SystemConfigurationMapper.class);

  @Mapping(target = "brand", source = "brand")
  @Mapping(target = "properties", source = "config.items")
  @Mapping(target = "createdAt", ignore = true)
  @Mapping(target = "createdBy", ignore = true)
  @Mapping(target = "createdByUserName", ignore = true)
  @Mapping(target = "updatedAt", ignore = true)
  @Mapping(target = "updatedBy", ignore = true)
  @Mapping(target = "updatedByUserName", ignore = true)
  SystemConfiguration toSystemConfig(String brand, ConfigItemDto config);

  @Mapping(target = "structureValue", ignore = true)
  SystemConfigProperty toSystemConfigProperty(ConfigItemPropertyDto propertyDto);

  @Mapping(target = "items", source = "properties")
  ConfigItemDto toConfigItemDto(SystemConfiguration config);

  ConfigItemPropertyDto toConfigPropertyDto(SystemConfigProperty item);

  default List<SystemConfiguration> toSystemConfigs(final ConfigDto dto) {
    return dto.getConfig().stream()
        .map(s -> toSystemConfig(dto.getBrand(), s))
        .collect(Collectors.toList());
  }

  @FortifyXSSValidate("return")
  default ConfigDto toConfigDto(String brand, Collection<SystemConfiguration> savedConfigs) {
    if (CollectionUtils.isEmpty(savedConfigs)) {
      return null;
    }
    ConfigDto dto = new ConfigDto();
    dto.setId(brand);
    dto.setBrand(brand);
    dto.setConfig(savedConfigs.stream().map(this::toConfigItemDto).collect(Collectors.toList()));
    setCreatedAndUpdatedData(dto, savedConfigs);
    return dto;
  }

  default StructureDto toStructureDto(
      String brand, Collection<SystemConfiguration> configurations) {
    Map<String, Map<String, Object>> structureMap =
        configurations.stream()
            .collect(
                Collectors.toMap(
                    SystemConfiguration::getName, c -> getStructureProperties(c.getProperties())));

    StructureDto dto = new StructureDto();
    dto.setBrand(brand);
    dto.setId(brand);
    dto.setStructure(structureMap);
    setCreatedAndUpdatedData(dto, configurations);
    return dto;
  }

  default Map<String, Object> getStructureProperties(List<SystemConfigProperty> properties) {
    // cannot use Collectors.toMap, cause it throws NPE on null values
    // https://bugs.openjdk.java.net/browse/JDK-8148463
    return properties.stream()
        .collect(
            HashMap::new,
            (map, item) -> map.put(item.getName(), item.getStructureValueOrDefault()),
            HashMap::putAll);
  }

  default void setCreatedAndUpdatedData(
      AbstractEntity dto, Collection<SystemConfiguration> configurations) {
    configurations.stream()
        .min(comparing(SystemConfiguration::getCreatedAt, nullsLast(naturalOrder())))
        .ifPresent(
            (SystemConfiguration config) -> {
              dto.setCreatedAt(config.getCreatedAt());
              dto.setCreatedBy(config.getCreatedBy());
              dto.setCreatedByUserName(config.getCreatedByUserName());
            });
    configurations.stream()
        .max(comparing(SystemConfiguration::getUpdatedAt, nullsFirst(naturalOrder())))
        .ifPresent(
            (SystemConfiguration config) -> {
              dto.setUpdatedAt(config.getUpdatedAt());
              dto.setUpdatedBy(config.getUpdatedBy());
              dto.setUpdatedByUserName(config.getUpdatedByUserName());
            });
  }
}
