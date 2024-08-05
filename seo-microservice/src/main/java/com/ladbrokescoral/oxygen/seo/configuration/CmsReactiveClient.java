package com.ladbrokescoral.oxygen.seo.configuration;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.ExchangeStrategies;
import org.springframework.web.reactive.function.client.WebClient;

@Component
public class CmsReactiveClient {

  private WebClient cmsWebClient;

  public CmsReactiveClient(
      WebClient cmsWebClient,
      @Value("${cms.reactive.client.max-in-memory-size:2097152}") int maxInmemorySize) {
    this.cmsWebClient =
        cmsWebClient
            .mutate()
            .exchangeStrategies(
                ExchangeStrategies.builder()
                    .codecs(cofigurer -> cofigurer.defaultCodecs().maxInMemorySize(maxInmemorySize))
                    .build())
            .build();
  }

  public WebClient getCMSWebClient() {
    return this.cmsWebClient;
  }
}
