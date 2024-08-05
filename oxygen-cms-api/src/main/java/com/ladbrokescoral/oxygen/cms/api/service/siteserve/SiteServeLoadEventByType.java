package com.ladbrokescoral.oxygen.cms.api.service.siteserve;

import static java.util.stream.Collectors.toMap;

import com.egalacoral.spark.siteserver.api.BaseFilter;
import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventExtendedDto;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class SiteServeLoadEventByType extends SiteServeLoadEvent {

  private final String siteChannel;
  private final String eventSortCodes;
  private final SiteServeApiProvider siteServerApiProvider;

  public SiteServeLoadEventByType(
      @Value("${siteserve.outright.siteChannel}") String siteChannel,
      @Value("${siteserve.outright.eventSortCodes}") String eventSortCodes,
      @Autowired SiteServeApiProvider siteServerApiProvider) {
    this.siteChannel = siteChannel;
    this.eventSortCodes = eventSortCodes;
    this.siteServerApiProvider = siteServerApiProvider;
  }

  @Override
  public List<SiteServeEventExtendedDto> loadEvents(
      String brand, String selectionId, Instant dateFrom, Instant dateTo) {
    List<SiteServeEventExtendedDto> events =
        getEventsByTypeAndMarketAndMainMarkets(brand, selectionId, dateFrom, dateTo);
    List<SiteServeEventExtendedDto> outrights =
        getOutrightsDataByType(brand, selectionId, dateFrom, dateTo);
    Collection<SiteServeEventExtendedDto> result =
        Stream.concat(events.stream(), outrights.stream())
            .collect(
                toMap(SiteServeEventExtendedDto::getId, event -> event, (left, right) -> right))
            .values();
    return new ArrayList<>(result);
  }

  private List<SiteServeEventExtendedDto> getEventsByTypeAndMarketAndMainMarkets(
      String brand, String selectionId, Instant dateFrom, Instant dateTo) {
    BaseFilter simpleFilter =
        getDefaultFilterBuilder(dateFrom, dateTo)
            .addBinaryOperation("market.dispSortName", BinaryOperation.intersects, "MR,HH,3W,2W")
            .build();
    return filterAndMap(
        siteServerApiProvider
            .api(brand)
            .getEventToOutcomeForType(selectionId, (SimpleFilter) simpleFilter));
  }

  private List<SiteServeEventExtendedDto> getOutrightsDataByType(
      String brand, String selectionId, Instant dateFrom, Instant dateTo) {
    BaseFilter simpleFilter =
        getDefaultFilterBuilder(dateFrom, dateTo)
            .addBinaryOperation("event.siteChannels", BinaryOperation.contains, siteChannel)
            .addBinaryOperation("event.eventSortCode", BinaryOperation.intersects, eventSortCodes)
            .build();
    Optional<List<Event>> eventToOutcomeForType =
        siteServerApiProvider
            .api(brand)
            .getEventToOutcomeForType(selectionId, (SimpleFilter) simpleFilter);
    List<SiteServeEventExtendedDto> eventExtendedDtos = filterAndMap(eventToOutcomeForType);
    eventExtendedDtos = populateOutright(eventExtendedDtos);
    return eventExtendedDtos;
  }

  private List<SiteServeEventExtendedDto> populateOutright(List<SiteServeEventExtendedDto> input) {
    return input.stream()
        .map(
            event -> {
              event.setOutright(true);
              return event;
            })
        .collect(Collectors.toList());
  }
}
