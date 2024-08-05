package com.ladbrokescoral.oxygen.cms.api.service.siteserve;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventExtendedDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.SiteServeEventDtoMapper;
import java.time.Instant;
import java.util.Collections;
import java.util.List;
import java.util.function.Function;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
public class SiteServeLoadEventBySelection extends SiteServeLoadEvent {

  private final SiteServeApiProvider siteServerApiProvider;

  @Override
  public List<SiteServeEventExtendedDto> loadEvents(
      String brand, String selectionId, Instant dateFrom, Instant dateTo) {
    return filterAndMap(
        siteServerApiProvider
            .api(brand)
            .getEventToOutcomeForOutcome(
                Collections.singletonList(selectionId),
                (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build(),
                null));
  }

  @Override
  protected Function<Event, SiteServeEventExtendedDto> getMapper() {
    return SiteServeEventDtoMapper.INSTANCE::toDtoSelection;
  }
}
