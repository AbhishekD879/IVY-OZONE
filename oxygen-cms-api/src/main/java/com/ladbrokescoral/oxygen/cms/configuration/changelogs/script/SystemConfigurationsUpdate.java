package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import static org.springframework.data.mongodb.core.BulkOperations.BulkMode.ORDERED;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.Config;
import com.ladbrokescoral.oxygen.cms.api.entity.Structure;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfigProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfiguration;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@RequiredArgsConstructor
@Slf4j
public class SystemConfigurationsUpdate extends AbstractBrandMongoUpdate {

  private static final String SYSTEM_CONFIGURATIONS_COLLECTION_NAME = "systemconfigurations";
  private static final String CONFIGS_COLLECTION_NAME = "configs";
  private static final String STRUCTURES_COLLECTION_NAME = "structures";

  private final MongockTemplate mongockTemplate;

  public void migrateAllConfigs() {
    List<SystemConfiguration> existingConfigs =
        mongockTemplate.findAll(SystemConfiguration.class, SYSTEM_CONFIGURATIONS_COLLECTION_NAME);
    List<Config> allConfigs = mongockTemplate.findAll(Config.class, CONFIGS_COLLECTION_NAME);
    List<Structure> allStructures =
        mongockTemplate.findAll(Structure.class, STRUCTURES_COLLECTION_NAME);
    Map<String, List<Structure>> structuresByBrand =
        allStructures.stream().collect(Collectors.groupingBy(Structure::getBrand));
    Map<String, Map<String, Map<String, Object>>> structureValues =
        structuresByBrand.entrySet().stream()
            .collect(Collectors.toMap(Map.Entry::getKey, e -> toConfigNameItemsMap(e.getValue())));

    List<SystemConfiguration> newConfigs =
        allConfigs.stream()
            .flatMap(
                c ->
                    toSystemConfigurationsStream(
                        c, structureValues.getOrDefault(c.getBrand(), Collections.emptyMap())))
            .filter(c -> !existingConfigs.contains(c))
            .distinct()
            .collect(Collectors.toList());
    int insertedCount =
        newConfigs.isEmpty()
            ? 0
            : mongockTemplate
                .bulkOps(ORDERED, SystemConfiguration.class, SYSTEM_CONFIGURATIONS_COLLECTION_NAME)
                .insert(newConfigs)
                .execute()
                .getInsertedCount();
    log.info("Migrated {} configs to systemconfigurations", insertedCount);
  }

  private Map<String, Map<String, Object>> toConfigNameItemsMap(List<Structure> brandStructures) {
    return brandStructures.stream()
        .flatMap(s -> s.getStructure().entrySet().stream())
        .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue, this::joinMaps));
  }

  private Map<String, Object> joinMaps(Map<String, Object> v1, Map<String, Object> v2) {
    Map<String, Object> joinedMaps = new HashMap<>();
    joinedMaps.putAll(v1);
    joinedMaps.putAll(v2);
    return joinedMaps;
  }

  private Stream<SystemConfiguration> toSystemConfigurationsStream(
      Config config, Map<String, Map<String, Object>> brandStructures) {
    return config.getConfig().entrySet().stream()
        .map(
            e ->
                createSystemConfiguration(
                    config, e, brandStructures.getOrDefault(e.getKey(), Collections.emptyMap())));
  }

  private SystemConfiguration createSystemConfiguration(
      Config config,
      Map.Entry<String, List<SystemConfigProperty>> configItem,
      Map<String, Object> structureProperties) {
    SystemConfiguration systemConfig = new SystemConfiguration();
    systemConfig.setBrand(config.getBrand());
    systemConfig.setInitialDataConfig(true);
    systemConfig.setName(configItem.getKey());
    systemConfig.setProperties(configItem.getValue());

    systemConfig
        .getProperties()
        .forEach(item -> item.setStructureValue(structureProperties.get(item.getName())));

    systemConfig.setCreatedAt(config.getCreatedAt());
    systemConfig.setCreatedBy(config.getCreatedBy());
    systemConfig.setCreatedByUserName(config.getCreatedByUserName());

    systemConfig.setUpdatedAt(config.getUpdatedAt());
    systemConfig.setUpdatedBy(config.getUpdatedBy());
    systemConfig.setUpdatedByUserName(config.getUpdatedByUserName());
    return systemConfig;
  }
}
