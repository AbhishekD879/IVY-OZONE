package com.ladbrokescoral.oxygen.trendingbets.siteserv.converter;

import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import org.springframework.stereotype.Component;

@Component
public class EventToTrendingEventConverter extends BaseConverter<Event, TrendingEvent> {

  @Override
  protected TrendingEvent populateResult(Event event, TrendingEvent trendingEvent) {
    trendingEvent.setId(event.getId());
    trendingEvent.setName(event.getName());
    trendingEvent.setCategoryId(event.getCategoryId());
    trendingEvent.setCategoryCode(event.getCategoryCode());
    trendingEvent.setCategoryName(event.getCategoryName());
    trendingEvent.setClassName(event.getClassName());
    trendingEvent.setTypeId(event.getTypeId());
    trendingEvent.setTypeName(event.getTypeName());
    trendingEvent.setEventIsLive(event.getIsStarted());
    trendingEvent.setDisplayed(event.getIsDisplayed());
    trendingEvent.setEventStatusCode(event.getEventStatusCode());
    trendingEvent.setIsDisplayed(event.getIsDisplayed());
    trendingEvent.setIsActive(event.getIsActive());
    trendingEvent.setLiveServChannels(
        event.getLiveServChannels().contains(",")
            ? event.getLiveServChannels().split(",")[0]
            : event.getLiveServChannels());
    trendingEvent.setLiveServChildrenChannels(event.getLiveServChildrenChannels());
    trendingEvent.setDrilldownTagNames(event.getDrilldownTagNames());
    trendingEvent.setStartTime(event.getStartTime());
    return trendingEvent;
  }

  @Override
  protected TrendingEvent createTarget() {
    return new TrendingEvent();
  }
}
