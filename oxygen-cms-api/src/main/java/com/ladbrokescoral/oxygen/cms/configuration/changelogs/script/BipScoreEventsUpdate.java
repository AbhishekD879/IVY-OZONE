package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfigProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfiguration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;

public class BipScoreEventsUpdate extends AbstractBrandMongoUpdate {

  private static final String CONFIG_COLLECTION_NAME = "systemconfigurations";
  private static final String BIP_CONFIG_NAME = "BipScoreEvents";
  private static final String CHECKBOX_VALUE = "checkbox";

  public void updateBipScoreEventsValue(MongockTemplate mongockTemplate, String brand) {
    List<SystemConfigProperty> items = new ArrayList<>();
    items.add(createItem("16"));
    items.add(createItem("6"));
    items.add(createItem("34"));
    items.add(createItem("51"));
    items.add(createItem("31"));
    items.add(createItem("30"));
    items.add(createItem("1"));
    items.add(createItem("5"));
    items.add(createItem("22"));
    items.add(createItem("149"));
    items.add(createItem("32"));
    items.add(createItem("53"));
    items.add(createItem("10"));

    updateConfig(mongockTemplate, brand, BIP_CONFIG_NAME, true, items);
  }

  private SystemConfigProperty createItem(String name) {
    return SystemConfigProperty.builder()
        .name(name)
        .type(CHECKBOX_VALUE)
        .value(true)
        .structureValue(true)
        .build();
  }

  private void updateConfig(
      MongockTemplate mongockTemplate,
      String brand,
      String configName,
      boolean isInitialDataConfig,
      List<SystemConfigProperty> items) {
    Query byBrandAndNameQuery =
        getFindByBrandQuery(brand).addCriteria(Criteria.where("name").is(configName));
    List<SystemConfiguration> systemConfigurations =
        mongockTemplate.find(
            byBrandAndNameQuery, SystemConfiguration.class, CONFIG_COLLECTION_NAME);
    SystemConfiguration config;
    if (systemConfigurations.isEmpty()) {
      config = new SystemConfiguration();
      config.setBrand(brand);
      config.setName(configName);
      config.setInitialDataConfig(isInitialDataConfig);
      config.setProperties(items);
      config.setCreatedAt(Instant.now());
    } else {
      config = systemConfigurations.get(0);
      List<SystemConfigProperty> configItems = new ArrayList<>(config.getProperties());
      config.setProperties(configItems);
      Map<String, SystemConfigProperty> configItemsByName =
          configItems.stream()
              .collect(Collectors.toMap(SystemConfigProperty::getName, Function.identity()));
      items.forEach(
          (SystemConfigProperty newItem) -> {
            if (configItemsByName.containsKey(newItem.getName())) {
              SystemConfigProperty configProperty = configItemsByName.get(newItem.getName());
              configProperty.setValue(newItem.getValue());
              configProperty.setStructureValue(newItem.getStructureValue());
            } else {
              configItems.add(newItem);
            }
          });
    }
    mongockTemplate.save(config, CONFIG_COLLECTION_NAME);
  }
}
