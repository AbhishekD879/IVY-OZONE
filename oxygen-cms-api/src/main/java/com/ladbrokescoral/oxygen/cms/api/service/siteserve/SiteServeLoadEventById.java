package com.ladbrokescoral.oxygen.cms.api.service.siteserve;

import com.egalacoral.spark.siteserver.api.ExistsFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventExtendedDto;
import java.time.Instant;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

@Slf4j
@Component
public class SiteServeLoadEventById extends SiteServeLoadEvent {

  private final String siteChannel;
  private final List<String> eventSortCodes;
  private final SiteServeApiProvider siteServerApiProvider;

  public SiteServeLoadEventById(
      @Value("${siteserve.outright.siteChannel}") String siteChannel,
      @Value("${siteserve.outright.eventSortCodes}") String eventSortCodes,
      @Autowired SiteServeApiProvider siteServerApiProvider) {
    this.siteChannel = siteChannel;
    this.eventSortCodes = Arrays.asList(eventSortCodes.split(","));
    this.siteServerApiProvider = siteServerApiProvider;
  }

  @Override
  public List<SiteServeEventExtendedDto> loadEvents(
      String brand, String eventId, Instant dateFrom, Instant dateTo) {
    SimpleFilter simpleFilter = (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build();
    ExistsFilter existsFilter = new ExistsFilter.ExistsFilterBuilder().build();
    Optional<List<Event>> events =
        siteServerApiProvider
            .api(brand)
            .getEventToOutcomeForEvent(
                Collections.singletonList(eventId),
                simpleFilter,
                existsFilter,
                Collections.emptyList(),
                false);
    return events.orElse(Collections.emptyList()).stream()
        .map(getMapperInstance()::toDtoWithChannels)
        .map(
            event -> {
              log.trace(
                  "EventDto -> {}; siteChannel (from config) -> {}; eventSortCodes (from config) -> {}",
                  event,
                  siteChannel,
                  eventSortCodes);
              event.setOutright(
                  event.getSiteChannels() != null
                      && event.getEventSortCode() != null
                      && event.getSiteChannels().contains(siteChannel)
                      && CollectionUtils.containsAny(
                          eventSortCodes, Arrays.asList(event.getEventSortCode().split(","))));
              return event;
            })
        .map(getMapperInstance()::toDtoWithoutChannels)
        .collect(Collectors.toList());
  }
}
