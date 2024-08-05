package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.OddsCardHeaderType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicReference;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.io.ClassPathResource;

@Slf4j
public class SportCategoriesMigrator extends AbstractBrandMongoUpdate {
  private static final String SPORT_CONFIGS_FILE = "/configuration/default-category-configs.json";
  private MongockTemplate mongockTemplate;
  private final ObjectMapper objectMapper;

  public SportCategoriesMigrator(MongockTemplate mongockTemplate) {
    this.mongockTemplate = mongockTemplate;
    this.objectMapper = new ObjectMapper();
  }

  public void updateSportsTier(String brand) {
    this.updateSport(
        brand,
        (category, settings) ->
            category.setTier(SportTier.from(settings.tier).orElse(SportTier.UNTIED)),
        SportSettingsDto.builder().tier(SportTier.UNTIED.value).build());
  }

  public void updateSportSettings(String brand) {
    this.updateSport(
        brand,
        (SportCategory category, SportSettingsDto settings) -> {
          category.setPrimaryMarkets(settings.primaryMarkets);
          category.setDispSortNames(settings.dispSortNames);
          category.setOutrightSport(settings.outrightSport);
          category.setMultiTemplateSport(settings.multiTemplateSport);
          category.setOddsCardHeaderType(
              OddsCardHeaderType.from(settings.oddsCardHeaderType).orElse(null));
        });
  }

  private void updateSport(String brand, SportSettingsMapper mapper) {
    updateSport(brand, mapper, null);
  }

  private void updateSport(
      String brand, SportSettingsMapper mapper, SportSettingsDto defaultSettingsDto) {
    AtomicReference<String> sportKey = new AtomicReference<>();
    try {
      Map<Integer, SportSettingsDto> sportSettingsMap = getSportSettingsMap();
      findAllByBrand(mongockTemplate, brand, SportCategory.class)
          .forEach(
              (SportCategory sportCategory) -> {
                sportKey.set(
                    String.format(
                        "Category: %s, %s", sportCategory.getCategoryId(), sportCategory.getId()));
                SportSettingsDto sportSetting =
                    sportSettingsMap.getOrDefault(
                        sportCategory.getCategoryId(), defaultSettingsDto);
                if (sportSetting != null) {
                  mapper.map(sportCategory, sportSetting);
                  mongockTemplate.save(sportCategory);
                }
              });
    } catch (Exception e) {
      log.error("Sports migration failed, " + sportKey, e);
      throw new IllegalArgumentException(e);
    }
  }

  private Map<Integer, SportSettingsDto> getSportSettingsMap() throws IOException {
    Map<Integer, SportSettingsDto> sportSettingsMap = new HashMap<>();
    SportSettingsDto[] sportsSettings = readJson(SPORT_CONFIGS_FILE, SportSettingsDto[].class);
    for (SportSettingsDto sportSettings : sportsSettings) {
      sportSettingsMap.put(sportSettings.getCategoryId(), sportSettings);
    }
    return sportSettingsMap;
  }

  private <T> T readJson(String file, Class<T> type) throws IOException {
    ClassPathResource sportsConfigsResource = new ClassPathResource(file);
    try (InputStream is = sportsConfigsResource.getInputStream()) {
      return objectMapper.readValue(is, type);
    } catch (IOException e) {
      throw e;
    }
  }

  interface SportSettingsMapper {
    void map(SportCategory sportCategory, SportSettingsDto sportSettings);
  }

  @JsonIgnoreProperties(ignoreUnknown = true)
  @Getter
  @AllArgsConstructor
  @Builder
  static class SportSettingsDto {
    private int categoryId;
    private String ssCategoryCode;
    private int tier;
    private boolean outrightSport;
    private boolean multiTemplateSport;
    private String oddsCardHeaderType;
    private String dispSortNames;
    private String primaryMarkets;
  }
}
