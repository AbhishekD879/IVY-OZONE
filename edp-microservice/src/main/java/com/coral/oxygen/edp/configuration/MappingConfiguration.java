package com.coral.oxygen.edp.configuration;

import com.coral.oxygen.edp.model.mapping.EventIsLiveMapper;
import com.coral.oxygen.edp.model.mapping.EventIsUSMapper;
import com.coral.oxygen.edp.model.mapping.EventLiveStreamAvailableMapper;
import com.coral.oxygen.edp.model.mapping.EventMapper;
import com.coral.oxygen.edp.model.mapping.MarketHandicapTypeMapper;
import com.coral.oxygen.edp.model.mapping.MarketMapper;
import com.coral.oxygen.edp.model.mapping.MarketNextScoreMapper;
import com.coral.oxygen.edp.model.mapping.MarketTermsMapper;
import com.coral.oxygen.edp.model.mapping.MarketViewTypeMapper;
import com.coral.oxygen.edp.model.mapping.OutcomeCorrectPriceTypeMapper;
import com.coral.oxygen.edp.model.mapping.OutcomeCorrectedMeaningMinorCodeMapper;
import com.coral.oxygen.edp.model.mapping.OutcomeMapper;
import com.coral.oxygen.edp.model.mapping.SimpleEventMapper;
import com.coral.oxygen.edp.model.mapping.SimpleMarketMapper;
import com.coral.oxygen.edp.model.mapping.SimpleOutcomeMapper;
import com.coral.oxygen.edp.model.mapping.VirtualEventMapper;
import com.coral.oxygen.edp.model.mapping.config.SportsConfig;
import com.coral.oxygen.edp.model.mapping.converter.Converter;
import com.coral.oxygen.edp.model.mapping.converter.MarketGroupAndSortConverter;
import java.util.List;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Created by azayats on 27.12.17. */
@Configuration
public class MappingConfiguration {

  @Bean
  public EventMapper eventMapper(
      SportsConfig sportsConfig,
      Converter<String, Integer> ordinalToNumberConverter,
      @Value("#{'${virtual.racing.id}'.split(',')}") List<String> virtualRacingIds) {
    EventMapper mapper =
        new SimpleEventMapper(
            createMarketMapper(sportsConfig, ordinalToNumberConverter),
            new MarketGroupAndSortConverter(),
            virtualRacingIds);
    mapper = new EventIsUSMapper(mapper);
    mapper = new EventLiveStreamAvailableMapper(mapper);
    mapper = new EventIsLiveMapper(mapper);
    mapper = new VirtualEventMapper(mapper);
    return mapper;
  }

  private MarketMapper createMarketMapper(
      SportsConfig sportsConfig, Converter<String, Integer> ordinalToNumberConverter) {
    MarketMapper mapper = new SimpleMarketMapper(createOutcomeMapper(sportsConfig));
    mapper = new MarketTermsMapper(mapper);
    mapper = new MarketHandicapTypeMapper(mapper);
    mapper = new MarketViewTypeMapper(mapper);
    mapper = new MarketNextScoreMapper(mapper, ordinalToNumberConverter);
    return mapper;
  }

  private OutcomeMapper createOutcomeMapper(SportsConfig sportsConfig) {
    OutcomeMapper mapper = new SimpleOutcomeMapper();
    mapper = new OutcomeCorrectedMeaningMinorCodeMapper(mapper, sportsConfig);
    mapper = new OutcomeCorrectPriceTypeMapper(mapper);
    return mapper;
  }
}
