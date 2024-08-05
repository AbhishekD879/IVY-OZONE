package com.ladbrokescoral.oxygen.timeline.api.config;

import com.ladbrokescoral.oxygen.timeline.api.registrators.PagePublisherChannelRegistrator;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class PagePublisherChannelConfiguration {

  @Bean
  public PagePublisherChannelRegistrator pagePublisherChannelRegistrator() {
    return new PagePublisherChannelRegistrator();
  }
}
