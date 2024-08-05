package com.coral.oxygen.middleware.ms.quickbet.converter;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputEvent;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.scoreboards.parser.api.BipParserFactory;
import com.ladbrokescoral.scoreboards.parser.model.BipComment;
import com.ladbrokescoral.scoreboards.parser.model.EventCategory;
import org.apache.commons.lang3.math.NumberUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class EventToOutputEventConverter extends BaseConverter<Event, OutputEvent> {

  private MarketToOutputMarketConverter marketToOutputMarketConverter;

  @Autowired
  public EventToOutputEventConverter(MarketToOutputMarketConverter marketToOutputMarketConverter) {
    this.marketToOutputMarketConverter = marketToOutputMarketConverter;
  }

  @Override
  protected OutputEvent populateResult(Event event, OutputEvent outputEvent) {
    outputEvent.setId(event.getId());
    BipComment bipComment =
        EventCategory.from(NumberUtils.toInt(event.getSportId()))
            .map(BipParserFactory::getParser)
            .orElse(BipParserFactory.getUnknownCategoryParser())
            .parse(event.getName());
    if (bipComment.getEventName() != null) {
      outputEvent.setName(bipComment.getEventName());
    }
    outputEvent.setEventStatusCode(event.getEventStatusCode());
    outputEvent.setIsLiveNowEvent(event.getIsLiveNowEvent());
    outputEvent.setIsStarted(event.getIsStarted());
    outputEvent.setStartTime(event.getStartTime());
    outputEvent.setTypeId(event.getTypeId());
    outputEvent.setTypeName(event.getTypeName());
    outputEvent.setCategoryId(event.getCategoryId());
    outputEvent.setCategoryName(event.getCategoryName());
    outputEvent.setClassId(event.getClassId());
    outputEvent.setClassName(event.getClassName());
    outputEvent.setDrilldownTagNames(event.getDrilldownTagNames());
    outputEvent.setIsCashoutAvailable(event.getCashoutAvail());
    if (event.getMarkets() != null) {
      outputEvent.setMarkets(marketToOutputMarketConverter.convert(event.getMarkets()));
    }
    outputEvent.setEventFlagCodes(event.getEventFlagCodes());
    return outputEvent;
  }

  @Override
  protected OutputEvent createTarget() {
    return new OutputEvent();
  }
}
