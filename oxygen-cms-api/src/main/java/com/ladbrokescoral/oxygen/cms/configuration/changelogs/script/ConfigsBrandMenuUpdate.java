package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import static com.ladbrokescoral.oxygen.cms.api.entity.SystemConfigPropertyType.CHECKBOX;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.dto.BrandMenuItemDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfigProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfiguration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;

public class ConfigsBrandMenuUpdate extends AbstractBrandMongoUpdate {

  private static final String CONFIGS_COLLECTION_NAME = "systemconfigurations";
  private static final String SSR_CONFIG_NAME = "SSRConfig";
  private static final String FIVE_A_SIDE_NAME = "FiveASide";
  private static final String NATIVE_CONFIG_NAME = "NativeConfig";

  public void updateSsrConfig(MongockTemplate mongockTemplate, String brand) {
    updateBrandMenu(
        mongockTemplate,
        brand,
        BrandMenuItemDto.builder()
            .active(true)
            .path("/ssr-config")
            .label("SSR Config")
            .id(UUID.randomUUID().toString())
            .build());

    updateSSRConfigDefaultValue(mongockTemplate, brand);
  }

  public void updateSSRConfigDefaultValue(MongockTemplate mongockTemplate, String brand) {
    List<SystemConfigProperty> items = new ArrayList<>();
    items.add(
        SystemConfigProperty.builder()
            .name("ssrEnabled")
            .type(CHECKBOX.getName())
            .value(false)
            .structureValue(false)
            .build());
    items.add(
        SystemConfigProperty.builder()
            .name("ssrSeoEnabled")
            .type(CHECKBOX.getName())
            .value(false)
            .structureValue(false)
            .build());
    updateConfigIfNotExists(mongockTemplate, brand, SSR_CONFIG_NAME, items);
  }

  public void update5ASideConfig(MongockTemplate mongockTemplate, String brand) {
    List<SystemConfigProperty> items = new ArrayList<>();
    items.add(
        SystemConfigProperty.builder()
            .name("enabled")
            .type(CHECKBOX.getName())
            .value(false)
            .structureValue(false)
            .build());
    items.add(
        SystemConfigProperty.builder()
            .name("newIcon")
            .type(CHECKBOX.getName())
            .value(false)
            .structureValue(false)
            .build());
    updateConfigIfNotExists(mongockTemplate, brand, FIVE_A_SIDE_NAME, items);
  }

  public void updateNativeConfig(MongockTemplate mongockTemplate, String brand) {
    List<SystemConfigProperty> items = new ArrayList<>();
    items.add(
        SystemConfigProperty.builder()
            .name("isGroupedFeaturedOnHomePageEnabled")
            .type(CHECKBOX.getName())
            .value(false)
            .structureValue(false)
            .build());
    updateConfigIfNotExists(mongockTemplate, brand, NATIVE_CONFIG_NAME, items);
  }

  private void updateConfigIfNotExists(
      MongockTemplate mongockTemplate,
      String brand,
      String configName,
      List<SystemConfigProperty> items) {

    Query byBrandAndConfigNameQuery =
        getFindByBrandQuery(brand).addCriteria(Criteria.where("name").is(configName));
    boolean existsConfig =
        mongockTemplate.exists(
            byBrandAndConfigNameQuery, SystemConfiguration.class, CONFIGS_COLLECTION_NAME);

    if (!existsConfig) {
      SystemConfiguration newConfig = new SystemConfiguration();
      newConfig.setName(configName);
      newConfig.setProperties(items);
      newConfig.setBrand(brand);
      newConfig.setInitialDataConfig(true);
      newConfig.setCreatedAt(Instant.now());
      newConfig.setUpdatedAt(Instant.now());
      mongockTemplate.save(newConfig, CONFIGS_COLLECTION_NAME);
    }
  }

  public void updateSegmentMenu(MongockTemplate mongockTemplate, String brand) {
    updateBrandMenu(
        mongockTemplate,
        brand,
        BrandMenuItemDto.builder()
            .active(true)
            .path("/delete-segments")
            .label("Delete Segments")
            .icon("delete")
            .id(UUID.randomUUID().toString())
            .build());
  }

  public void updateOnBoardingMenu(MongockTemplate mongockTemplate, String brand) {
    updateBrandMenu(
        mongockTemplate,
        brand,
        BrandMenuItemDto.builder()
            .active(true)
            .path("/onBoarding")
            .label("onBoarding")
            .icon("onBoarding")
            .id(UUID.randomUUID().toString())
            .build());
  }
}
