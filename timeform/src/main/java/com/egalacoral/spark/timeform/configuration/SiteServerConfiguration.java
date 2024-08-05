package com.egalacoral.spark.timeform.configuration;

import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.siteserver.api.SiteServerAPI.Builder;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SiteServerConfiguration {

  @Value("${siteserver.url}")
  private String url = "http://backoffice-tst2.coral.co.uk/";

  @Value("${siteserver.connectionTimeOut}")
  private int connectionTimeOut = 5;

  @Value("${siteserver.readTimeOut}")
  private int readTimeOut = 5;

  @Value("${siteserver.maxNumberOfRetries}")
  private Integer maxNumberOfRetries = 3;

  @Bean
  public SiteServerAPI getSiteServerAPI() {
    final Builder api =
        new SiteServerAPI.Builder(url)
            .setLoggingLevel(SiteServerAPI.Level.BODY)
            .setConnectionTimeout(connectionTimeOut)
            .setReadTimeout(readTimeOut)
            .setMaxNumberOfRetries(maxNumberOfRetries);
    return api.build();
  }
}
