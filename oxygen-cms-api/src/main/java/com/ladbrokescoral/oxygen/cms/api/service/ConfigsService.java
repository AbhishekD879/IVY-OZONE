package com.ladbrokescoral.oxygen.cms.api.service;

import static com.ladbrokescoral.oxygen.cms.api.entity.SystemConfigPropertyType.*;

import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfigProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfiguration;
import com.ladbrokescoral.oxygen.cms.api.repository.SystemConfigurationRepository;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class ConfigsService extends AbstractService<SystemConfiguration> {

  private final SystemConfigurationRepository configsRepository;

  @Autowired
  public ConfigsService(SystemConfigurationRepository configsRepository) {
    super(configsRepository);
    this.configsRepository = configsRepository;
  }

  @Override
  public SystemConfiguration prepareModelBeforeSave(SystemConfiguration model) {
    model.getProperties().stream()
        .filter(prop -> Objects.isNull(prop.getStructureValue()))
        .forEach(
            prop ->
                prop.setStructureValue(
                    from(prop.getType()).parseDefaultStructureValue(prop.getValue())));
    return model;
  }

  @Override
  public SystemConfiguration update(
      SystemConfiguration existingEntity, SystemConfiguration updateEntity) {
    Map<String, SystemConfigProperty> existingPropertiesByName =
        existingEntity.getProperties().stream()
            .collect(Collectors.toMap(SystemConfigProperty::getName, Function.identity()));

    updateEntity.getProperties().stream()
        .filter(p -> existingPropertiesByName.containsKey(p.getName()))
        .forEach(p -> updateStructureValue(existingPropertiesByName.get(p.getName()), p));
    return super.update(existingEntity, updateEntity);
  }

  private void updateStructureValue(
      SystemConfigProperty existingSystemProperty, SystemConfigProperty newSystemProperty) {
    Object newStructureValue =
        from(newSystemProperty.getType())
            .adaptStructureValue(
                existingSystemProperty.getStructureValue(), newSystemProperty.getValue());
    newSystemProperty.setStructureValue(newStructureValue);
  }

  public void deleteAllByBrand(String brand) {
    configsRepository.deleteAllByBrand(brand);
  }

  public Optional<SystemConfiguration> findElementByBrandAndName(String brand, String name) {

    return configsRepository.findOneByBrandAndName(brand, name);
  }
}
