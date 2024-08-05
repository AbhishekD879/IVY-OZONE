package com.ladbrokescoral.oxygen.cms.api.service.siteserve;

import static java.util.stream.Collectors.toMap;

import com.egalacoral.spark.siteserver.api.BaseFilter;
import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventExtendedDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.SiteServeEventDtoMapper;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
public class SiteServeLoadEventByCategory extends SiteServeLoadEvent {

  private final SiteServeApiProvider siteServerApiProvider;

  @Override
  public List<SiteServeEventExtendedDto> loadEvents(
      String brand, String obCategoryId, Instant dateFrom, Instant dateTo) {
    List<SiteServeEventExtendedDto> events =
        getEventsByObCategory(brand, obCategoryId, dateFrom, dateTo);
    Collection<SiteServeEventExtendedDto> result =
        events.stream()
            .collect(
                toMap(SiteServeEventExtendedDto::getId, event -> event, (left, right) -> right))
            .values();
    return new ArrayList<>(result);
  }

  private List<SiteServeEventExtendedDto> getEventsByObCategory(
      String brand, String obCategoryId, Instant dateFrom, Instant dateTo) {
    BaseFilter simpleFilter =
        getDefaultFilterBuilder(dateFrom, dateTo)
            .addBinaryOperation("event.siteChannels", BinaryOperation.contains, "M")
            .addBinaryOperation("event.categoryId", BinaryOperation.equals, obCategoryId)
            .build();
    Optional<List<Event>> events =
        siteServerApiProvider.api(brand).getEvents((SimpleFilter) simpleFilter);
    return events.orElseGet(ArrayList::new).stream()
        .map(SiteServeEventDtoMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
