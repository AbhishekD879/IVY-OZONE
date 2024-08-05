package com.ladbrokescoral.oxygen.cms.api.service.impl;

import static java.util.stream.Collectors.toMap;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.model.Aggregation;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventExtendedDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SelectionType;
import com.ladbrokescoral.oxygen.cms.api.mapping.SiteServeEventDtoMapper;
import com.ladbrokescoral.oxygen.cms.api.service.HomeModuleSiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeLoadEvent;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeLoadEventFactory;
import java.time.Instant;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class HomeModuleSiteServeServiceImpl implements HomeModuleSiteServeService {

  private final SiteServeApiProvider siteServeApiProvider;
  private final SiteServeLoadEventFactory siteServeLoadEventFactory;

  private static final Comparator<SiteServeEventExtendedDto>
      SORT_BY_DISPLAY_ORDER_AND_START_TIME_AND_NAME =
          Comparator.comparing(SiteServeEventExtendedDto::getDisplayOrder)
              .thenComparing(SiteServeEventExtendedDto::getStartTime)
              .thenComparing(SiteServeEventExtendedDto::getName);

  @Override
  public List<SiteServeEventDto> loadEventsFromSiteServe(
      String brand,
      SelectionType selectionType,
      String selectionId,
      Instant dateFrom,
      Instant dateTo) {
    SiteServeLoadEvent siteServeEventLoader = siteServeLoadEventFactory.getLoader(selectionType);
    List<SiteServeEventExtendedDto> events =
        siteServeEventLoader.loadEvents(brand, selectionId, dateFrom, dateTo);
    Map<Long, Integer> eventIdAndMarketCountMap = getMarketCountForEvents(brand, events);

    return events.stream()
        .sorted(SORT_BY_DISPLAY_ORDER_AND_START_TIME_AND_NAME)
        .map(SiteServeEventDtoMapper.INSTANCE::toDto)
        .map(dto -> populateMarketCount(dto, eventIdAndMarketCountMap))
        .collect(Collectors.toList());
  }

  private Map<Long, Integer> getMarketCountForEvents(
      String brand, List<SiteServeEventExtendedDto> events) {
    List<String> ids =
        events.stream().map(SiteServeEventExtendedDto::getId).collect(Collectors.toList());
    Optional<List<Aggregation>> marketsCountForEvent =
        siteServeApiProvider
            .api(brand)
            .getMarketsCountForEvent(
                ids, (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build());
    return marketsCountForEvent
        .map(
            list ->
                list.stream().collect(toMap(Aggregation::getRefRecordId, Aggregation::getCount)))
        .orElseGet(HashMap::new);
  }

  private SiteServeEventDto populateMarketCount(
      SiteServeEventDto dto, Map<Long, Integer> mapOfIdsAndMarketCount) {
    dto.setMarketCount(mapOfIdsAndMarketCount.get(Long.parseLong(dto.getId())));
    return dto;
  }
}
