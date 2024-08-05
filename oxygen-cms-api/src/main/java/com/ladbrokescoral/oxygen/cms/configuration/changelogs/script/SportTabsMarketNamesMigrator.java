package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import static java.util.stream.Collectors.groupingBy;
import static org.apache.commons.collections4.CollectionUtils.emptyIfNull;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTabMarket;
import com.ladbrokescoral.oxygen.cms.api.exception.MarketNamesMigratorException;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.core.io.ClassPathResource;

@Slf4j
public class SportTabsMarketNamesMigrator extends AbstractBrandMongoUpdate {

  private final ObjectMapper objectMapper;
  private final ModelMapper modelMapper;
  private MongockTemplate mongockTemplate;
  private static final String LADS_MARKET_NAMES_FILE = "/sporttab-markets/marketnames-lads.json";
  private static final String CORAL_MARKET_NAMES_FILE = "/sporttab-markets/marketnames-coral.json";
  private static final String SPORT_TABS_COLLECTION_NAME = "sporttabs";
  private static final String LADBROKES = "ladbrokes";
  private static final String MATCHES = "matches";
  private static final String COMPETITIONS = "competitions";

  public SportTabsMarketNamesMigrator(MongockTemplate mongockTemplate) {
    this.mongockTemplate = mongockTemplate;
    this.objectMapper = new ObjectMapper();
    this.modelMapper = new ModelMapper();
  }

  public void saveSportsTabMarketNames(String brand) {
    try {
      SporttabsDto sporttabsDto =
          brand.equals(LADBROKES)
              ? readJson(LADS_MARKET_NAMES_FILE, SporttabsDto.class)
              : readJson(CORAL_MARKET_NAMES_FILE, SporttabsDto.class);
      updateTabsWithMarketNames(brand, MATCHES, sporttabsDto.getMatches());
      updateTabsWithMarketNames(brand, COMPETITIONS, sporttabsDto.getCompetitions());
    } catch (Exception e) {
      log.error("SportTabs Market Names migration failed {} ", e);
      throw new MarketNamesMigratorException(e.getMessage());
    }
  }

  private void updateTabsWithMarketNames(
      String brand, String tabName, List<SporttabDto> sporttabDtos) {
    Map<Integer, List<SporttabMarketNamesDto>> sportIdSporttabMarketNamesDtoMap = new HashMap<>();
    sporttabDtos.stream()
        .forEach(
            (SporttabDto sporttabDto) ->
                sportIdSporttabMarketNamesDtoMap.put(
                    sporttabDto.getSportId(), sporttabDto.getMarketsNames()));

    List<SportTab> sportTabs =
        findByBrandAndTabName(
            mongockTemplate, brand, tabName, SPORT_TABS_COLLECTION_NAME, SportTab.class);
    Map<Integer, List<SportTab>> sportIdSportTabMap =
        sportTabs.stream().collect(groupingBy(SportTab::getSportId));

    sportIdSporttabMarketNamesDtoMap.forEach(
        (Integer catId, List<SporttabMarketNamesDto> sporttabMarketNamesDtos) -> {
          List<SportTabMarket> marketsNames =
              sporttabMarketNamesDtos.stream()
                  .map(e -> modelMapper.map(e, SportTabMarket.class))
                  .collect(Collectors.toList());
          emptyIfNull(sportIdSportTabMap.get(catId)).stream()
              .forEach(
                  (SportTab sportTab) -> {
                    sportTab.setMarketsNames(marketsNames);
                    mongockTemplate.save(sportTab);
                  });
        });
  }

  public <T> T readJson(String file, Class<T> type) throws IOException {
    ClassPathResource sportTabMarketsResource = new ClassPathResource(file);
    try (InputStream is = sportTabMarketsResource.getInputStream()) {
      return objectMapper.readValue(is, type);
    } catch (IOException e) {
      throw new MarketNamesMigratorException(e.getMessage());
    }
  }

  @JsonIgnoreProperties(ignoreUnknown = true)
  @Getter
  @AllArgsConstructor
  @Builder
  static class SporttabMarketNamesDto {
    private String templateMarketName;
    private String title;
    private boolean isAggregated;
  }

  @JsonIgnoreProperties(ignoreUnknown = true)
  @Getter
  @AllArgsConstructor
  @Builder
  static class SporttabDto {
    private int sportId;
    private List<SporttabMarketNamesDto> marketsNames;
  }

  @JsonIgnoreProperties(ignoreUnknown = true)
  @Getter
  @AllArgsConstructor
  @Builder
  static class SporttabsDto {
    private List<SporttabDto> matches;
    private List<SporttabDto> competitions;
  }
}
