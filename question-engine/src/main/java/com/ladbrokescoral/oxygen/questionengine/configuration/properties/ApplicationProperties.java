package com.ladbrokescoral.oxygen.questionengine.configuration.properties;

import lombok.Data;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@Component
@ConfigurationProperties("application")
public class ApplicationProperties {

  /*
  Infrastructure-manged.
 */
  @Value("#{'${application.allowedOrigins}'.split(',')}")
  private String[] allowedOrigins;

  private String brand;

  private Integer historyPreviousCacheSize;
  private Integer liveQuizCacheTtlDays;
  private Integer historyCacheTtlDays;
  private Integer upsellCacheTtlMinutes;
  private Integer siteServerSelectionIdsLimit;

  /*
    Infrastructure-manged.
  */
  @Value("${QE_API_KEY:}")
  private String apiKey;
}
