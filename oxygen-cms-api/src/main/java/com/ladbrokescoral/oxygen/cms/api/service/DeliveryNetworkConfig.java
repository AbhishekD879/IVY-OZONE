package com.ladbrokescoral.oxygen.cms.api.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.view.Views;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkExecutor;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkServiceImpl;
import com.ladbrokescoral.oxygen.cms.configuration.CFCacheTagProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DeliveryNetworkConfig {

  /**
   * Uploads json serialized with {@link Views.Public} {@link
   * com.fasterxml.jackson.annotation.JsonView} writer
   */
  @Bean
  public DeliveryNetworkService publicViewOnlyDelivery(
      ObjectMapper objectMapper,
      DeliveryNetworkExecutor deliveryNetworkExecutor,
      CFCacheTagProperties cfCacheTagProperties) {
    return new DeliveryNetworkServiceImpl(
        deliveryNetworkExecutor,
        objectMapper.writerWithView(Views.Public.class),
        cfCacheTagProperties);
  }
}
