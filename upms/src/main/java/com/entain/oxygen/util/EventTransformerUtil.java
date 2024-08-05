package com.entain.oxygen.util;

import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.egalacoral.spark.siteserver.model.Price;
import com.entain.oxygen.dto.*;
import java.util.List;
import java.util.stream.Collectors;
import lombok.experimental.UtilityClass;
import org.modelmapper.ModelMapper;

@UtilityClass
public class EventTransformerUtil {
  private static final ModelMapper modelMapper = new ModelMapper();

  public List<ChildrenDto> copyEventsToEventDtos(List<Event> events) {
    return events.stream()
        .map(EventTransformerUtil::copyEventToEventDto)
        .collect(Collectors.toList());
  }

  private ChildrenDto copyEventToEventDto(Event event) {
    EventDto eventDto = modelMapper.map(event, EventDto.class);
    eventDto.setChildren(copyMarkets(event.getMarkets()));
    ChildrenDto childrenDto = new ChildrenDto();
    childrenDto.setEvent(eventDto);
    return childrenDto;
  }

  private List<ChildrenDto> copyMarkets(List<Market> markets) {
    List<ChildrenDto> marketDtoList =
        markets.stream()
            .map(EventTransformerUtil::copyMarketToMarketDto)
            .collect(Collectors.toList());
    return marketDtoList.isEmpty() ? null : marketDtoList;
  }

  private ChildrenDto copyMarketToMarketDto(Market market) {
    MarketDto marketDto = modelMapper.map(market, MarketDto.class);
    marketDto.setChildren(copyOutcomes(market.getOutcomes()));
    ChildrenDto childrenDto = new ChildrenDto();
    childrenDto.setMarket(marketDto);
    return childrenDto;
  }

  private List<ChildrenDto> copyOutcomes(List<Outcome> outcomes) {
    List<ChildrenDto> outcomeDtoList =
        outcomes.stream()
            .map(EventTransformerUtil::copyOutcomeToOutcomeDto)
            .collect(Collectors.toList());
    return outcomeDtoList.isEmpty() ? null : outcomeDtoList;
  }

  private ChildrenDto copyOutcomeToOutcomeDto(Outcome outcome) {
    OutcomeDto outcomeDto = modelMapper.map(outcome, OutcomeDto.class);
    outcomeDto.setChildren(copyPrices(outcome.getPrices()));
    ChildrenDto childrenDto = new ChildrenDto();
    childrenDto.setOutcome(outcomeDto);
    return childrenDto;
  }

  private List<ChildrenDto> copyPrices(List<Price> prices) {
    List<ChildrenDto> priceDtoList =
        prices.stream().map(EventTransformerUtil::copyPriceToPriceDto).collect(Collectors.toList());
    return priceDtoList.isEmpty() ? null : priceDtoList;
  }

  private ChildrenDto copyPriceToPriceDto(Price price) {
    ChildrenDto childrenDto = new ChildrenDto();
    childrenDto.setPrice(modelMapper.map(price, PriceDto.class));
    return childrenDto;
  }
}
