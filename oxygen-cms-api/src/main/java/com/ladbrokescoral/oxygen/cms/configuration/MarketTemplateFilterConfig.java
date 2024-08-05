package com.ladbrokescoral.oxygen.cms.configuration;

import java.util.Map;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@Slf4j
@Component
@EnableConfigurationProperties
@ConfigurationProperties(prefix = "siteserve.marketfilter")
public class MarketTemplateFilterConfig {

  private Map<String, String> raceTypeTemplateNames;

  public String getRaceTypeMarketTemplateNames(String brand, String defaultIfEmpty) {
    return raceTypeTemplateNames.getOrDefault(brand, defaultIfEmpty);
  }
}
