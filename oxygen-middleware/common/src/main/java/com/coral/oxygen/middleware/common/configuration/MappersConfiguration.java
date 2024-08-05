package com.coral.oxygen.middleware.common.configuration;

import com.coral.oxygen.middleware.common.mappers.*;
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService;
import com.coral.oxygen.middleware.common.service.SportsConfig;
import com.coral.oxygen.middleware.common.utils.Converter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MappersConfiguration {

  @Bean(name = "featured")
  public EventMapper eventFeaturedMapper(
      MarketMapper marketMapper, MarketTemplateNameService marketTemplateNameService) {
    EventMapper mapper = new FeaturedSimpleEventMapper(marketMapper, marketTemplateNameService);
    mapper = new EventIsUSMapper(mapper);
    mapper = new EventLiveStreamAvailableMapper(mapper);
    mapper = new EventIsLiveMapper(mapper);
    mapper = new EventNameFeaturedMapper(mapper);
    // should be called first in chain as it will filter inactive events
    mapper = new FilterEventMapper(mapper);
    return mapper;
  }

  @Bean(name = "inplay")
  public EventMapper eventInplayMapper(MarketMapper inplayMarketMapper) {
    EventMapper mapper = new SimpleEventMapper(inplayMarketMapper);
    mapper = new EventIsUSMapper(mapper);
    mapper = new EventLiveStreamAvailableMapper(mapper);
    // EventTypeFlagCodesMapper should be called after EventLiveStreamAvailableMapper
    mapper = new EventTypeFlagCodesMapper(mapper);
    mapper = new EventIsLiveMapper(mapper);
    // should be called first in chain as it will filter inactive events
    mapper = new FilterEventMapper(mapper);
    return mapper;
  }

  @Bean
  public RacingForOutcomeMapper racingForOutcomeMapper() {
    return new SimpleRacingForOutcomeMapper();
  }

  @Bean
  public RacingFormEventMapper racingFormEventapper() {
    return new SimpleRacingFormEventMapper();
  }

  @Bean(name = "inplayMarketMapper")
  public MarketMapper marketMapper(
      SiteServerApi siteServerApi,
      SportsConfig sportsConfig,
      Converter<String, Integer> ordinalToNumberConverter,
      MarketTemplateNameService marketTemplateNameService) {
    MarketMapper mapper = new SimpleMarketMapper(createOutcomeMapper(sportsConfig));
    mapper = new MarketTermsMapper(mapper);
    mapper = new MarketHandicapTypeMapper(mapper, marketTemplateNameService);
    mapper = new MarketViewTypeMapper(mapper);
    mapper = new MarketNextScoreMapper(mapper, ordinalToNumberConverter, marketTemplateNameService);
    mapper = new OrderedOutcomeMarketMapper(mapper, new OrderedOutcomeMarketHelper(siteServerApi));
    return mapper;
  }

  private OutcomeMapper createOutcomeMapper(SportsConfig sportsConfig) {
    OutcomeMapper mapper = new SimpleOutcomeMapper();
    mapper = new OutcomeCorrectedMeaningMinorCodeMapper(mapper, sportsConfig);
    mapper = new OutcomeCorrectPriceTypeMapper(mapper);
    return mapper;
  }
}
