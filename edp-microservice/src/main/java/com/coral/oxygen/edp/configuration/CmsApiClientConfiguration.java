package com.coral.oxygen.edp.configuration;

import com.ladbrokescoral.oxygen.cms.client.api.CmsApiClient;
import com.ladbrokescoral.oxygen.cms.client.api.CmsApiClientImpl;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class CmsApiClientConfiguration {

  @Bean
  CmsApiClient cmsApiClient(@Value("${cms.base.url}") String cmsApiBaseUrl) {
    return new CmsApiClientImpl(cmsApiBaseUrl);
  }
}
