package com.ladbrokescoral.oxygen.cms.api.service.siteserve;

import com.egalacoral.spark.siteserver.api.BaseFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventExtendedDto;
import java.time.Instant;
import java.util.List;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
public class SiteServeLoadEventByEnhancedMultiples extends SiteServeLoadEvent {

  private final SiteServeApiProvider siteServerApiProvider;

  @Override
  public List<SiteServeEventExtendedDto> loadEvents(
      String brand, String selectionId, Instant dateFrom, Instant dateTo) {
    BaseFilter simpleFilter = getDefaultFilterBuilder(dateFrom, dateTo).build();
    return filterAndMap(
        siteServerApiProvider
            .api(brand)
            .getEventToOutcomeForType(selectionId, (SimpleFilter) simpleFilter));
  }
}
