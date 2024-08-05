package com.ladbrokescoral.oxygen.cms.api.service.siteserve;

import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.UnaryOperation;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventExtendedDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.SiteServeEventDtoMapper;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import org.springframework.stereotype.Component;

@Component
public abstract class SiteServeLoadEvent {

  private static final Predicate<Event> FILTER_BY_CHILDREN_AND_NOT_SUSPENDED =
      event ->
          (!event.getChildren().isEmpty() || Objects.nonNull(event.getLiveServChildrenChannels()))
              && !"S".equals(event.getEventStatusCode());

  public abstract List<SiteServeEventExtendedDto> loadEvents(
      String brand, String selectionId, Instant dateFrom, Instant dateTo);

  protected SimpleFilter.SimpleFilterBuilder getDefaultFilterBuilder(
      Instant dateFrom, Instant dateTo) {
    return new SimpleFilter.SimpleFilterBuilder()
        .addBinaryOperation("event.startTime", BinaryOperation.greaterThanOrEqual, dateFrom)
        .addBinaryOperation("event.startTime", BinaryOperation.lessThan, dateTo)
        .addBinaryOperation(
            "event.suspendAtTime",
            BinaryOperation.greaterThanOrEqual,
            Instant.now().truncatedTo(ChronoUnit.SECONDS))
        .addUnaryOperation("event.isFinished", UnaryOperation.isFalse);
  }

  protected List<SiteServeEventExtendedDto> filterAndMap(Optional<List<Event>> input) {
    return input.orElseGet(ArrayList::new).stream()
        .filter(FILTER_BY_CHILDREN_AND_NOT_SUSPENDED)
        .map(getMapper())
        .collect(Collectors.toList());
  }

  protected Function<Event, SiteServeEventExtendedDto> getMapper() {
    return getMapperInstance()::toDto;
  }

  protected SiteServeEventDtoMapper getMapperInstance() {
    return SiteServeEventDtoMapper.INSTANCE;
  }
}
