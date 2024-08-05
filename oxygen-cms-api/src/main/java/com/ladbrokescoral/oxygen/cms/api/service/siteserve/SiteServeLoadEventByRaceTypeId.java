package com.ladbrokescoral.oxygen.cms.api.service.siteserve;

import com.egalacoral.spark.siteserver.api.BaseFilter;
import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventExtendedDto;
import com.ladbrokescoral.oxygen.cms.configuration.MarketTemplateFilterConfig;
import java.time.Instant;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class SiteServeLoadEventByRaceTypeId extends SiteServeLoadEvent {

  private static final String DEFAULT_TEMPLATE_NAMES = "|Win or Each Way|";

  private final SiteServeApiProvider siteServerApiProvider;
  private final MarketTemplateFilterConfig marketTemplateFilterConfig;

  @Override
  public List<SiteServeEventExtendedDto> loadEvents(
      String brand, String selectionId, Instant dateFrom, Instant dateTo) {

    BaseFilter simpleFilter =
        getDefaultFilterBuilder(dateFrom, dateTo)
            .addBinaryOperation(
                "market.templateMarketName",
                BinaryOperation.intersects,
                marketTemplateFilterConfig.getRaceTypeMarketTemplateNames(
                    brand, DEFAULT_TEMPLATE_NAMES))
            .build();

    return filterAndMap(
        siteServerApiProvider
            .api(brand)
            .getEventToOutcomeForType(selectionId, (SimpleFilter) simpleFilter));
  }
}
