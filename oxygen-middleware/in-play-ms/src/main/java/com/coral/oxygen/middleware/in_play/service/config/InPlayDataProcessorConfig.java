package com.coral.oxygen.middleware.in_play.service.config;

import com.coral.oxygen.middleware.common.service.notification.MessagePublisher;
import com.coral.oxygen.middleware.in_play.service.InPlayDataConsumer;
import com.coral.oxygen.middleware.in_play.service.InPlayDataProcessor;
import com.coral.oxygen.middleware.in_play.service.InPlayDataSorter;
import com.coral.oxygen.middleware.in_play.service.InPlayStorageService;
import com.coral.oxygen.middleware.in_play.service.InplayLiveServerSubscriber;
import com.coral.oxygen.middleware.in_play.service.market.selector.MarketSelectorService;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.google.gson.Gson;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;

/** Created by Aliaksei Yarotski on 10/19/17. */
@Configuration
@ConditionalOnProperty(name = "inplay.scheduled.task.enabled")
public class InPlayDataProcessorConfig {

  @ConditionalOnProperty(name = "inplay.scheduled.task.enabled")
  @Component
  public static class InPlayDataProcessorBuilder {

    @Autowired private InPlayDataConsumer consumer;
    @Autowired private InPlayStorageService storageService;

    @Autowired private MessagePublisher messagePublisher;

    @Autowired private InplayLiveServerSubscriber inplayLiveServerSubscriber;
    @Autowired private Gson gson;

    @Autowired private SiteServerApi siteServerApi;

    @Autowired private MarketSelectorService marketSelectorService;

    @Autowired private InPlayDataSorter inPlayDataSorter;

    @Value("${pessimistic.mode}")
    private boolean pessimisticModeEnabled;

    private InPlayDataProcessorBuilder() {}

    public InPlayDataProcessor build() {
      return new InPlayDataProcessor(this);
    }

    public InPlayDataConsumer getConsumer() {
      return consumer;
    }

    public InPlayStorageService getStorageService() {
      return storageService;
    }

    public MessagePublisher getMessagePublisher() {
      return messagePublisher;
    }

    public InplayLiveServerSubscriber getInplayLiveServerSubscriber() {
      return inplayLiveServerSubscriber;
    }

    public Gson getGson() {
      return gson;
    }

    public SiteServerApi getSiteServerApi() {
      return siteServerApi;
    }

    public MarketSelectorService getMarketSelectorService() {
      return marketSelectorService;
    }

    public boolean isPessimisticModeEnabled() {
      return pessimisticModeEnabled;
    }

    public InPlayDataSorter getInPlayDataSorter() {
      return inPlayDataSorter;
    }
  }

  @Bean
  public InPlayDataProcessor inPlayDataProcessor(
      InPlayDataProcessorBuilder inPlayDataProcessorBuilder) {
    return inPlayDataProcessorBuilder.build();
  }
}
