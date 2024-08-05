package com.ladbrokescoral.oxygen.cms.api.service.siteserve;

import com.egalacoral.spark.siteserver.api.BaseFilter;
import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventExtendedDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventTreeNodeDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.SiteServeEventDtoMapper;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
public class SiteServeLoadEventTree extends SiteServeLoadEvent {

  protected static final Predicate<Event> FILTER_BY_NOT_SUSPENDED =
      event -> !"S".equals(event.getEventStatusCode());

  private final SiteServeApiProvider siteServerApiProvider;

  public List<SiteServeEventTreeNodeDto> loadEventsInNode(
      String brand, Integer categoryId, Instant dateFrom) {
    BaseFilter baseFilter =
        new SimpleFilter.SimpleFilterBuilder()
            .addBinaryOperation("event.startTime", BinaryOperation.greaterThanOrEqual, dateFrom)
            .addBinaryOperation("event.categoryId", BinaryOperation.equals, categoryId)
            .addBinaryOperation("event.isActive", BinaryOperation.equals, Boolean.TRUE.toString())
            .build();

    Optional<List<Event>> events =
        siteServerApiProvider
            .api(brand)
            .getEvent(
                Collections.emptyList(), Optional.of((SimpleFilter) baseFilter), Optional.empty());
    return events.orElseGet(ArrayList::new).stream()
        .filter(FILTER_BY_NOT_SUSPENDED)
        .map(getNodeMapper())
        .collect(Collectors.toList());
  }

  @Override
  public List<SiteServeEventExtendedDto> loadEvents(
      String brand, String selectionId, Instant dateFrom, Instant dateTo) {
    return Collections.emptyList();
  }

  protected Function<Event, SiteServeEventTreeNodeDto> getNodeMapper() {
    return SiteServeEventDtoMapper.INSTANCE::toDtoNode;
  }
}
