package com.entain.oxygen.service.siteserver;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.entain.oxygen.configuration.SiteServerApiConfig;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class SiteServerApiProviderImpl implements SiteServerApiProvider {

  private final SiteServerApiConfig config;

  @Override
  public SiteServerApi getSiteServerApi() {
    return config.siteServerAPI();
  }
}
