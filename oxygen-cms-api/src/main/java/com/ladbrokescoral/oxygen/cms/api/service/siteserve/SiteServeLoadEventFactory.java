package com.ladbrokescoral.oxygen.cms.api.service.siteserve;

import com.ladbrokescoral.oxygen.cms.api.entity.SelectionType;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class SiteServeLoadEventFactory {

  private final SiteServeLoadEventByEnhancedMultiples siteServeLoadEventByEnhancedMultiples;
  private final SiteServeLoadEventByRaceTypeId siteServeLoadEventByRaceTypeId;
  private final SiteServeLoadEventBySelection siteServeLoadEventBySelection;
  private final SiteServeLoadEventByType siteServeLoadEventByType;
  private final SiteServeLoadEventByClass siteServeLoadEventByClass;
  private final SiteServeLoadEventByCategory siteServeLoadEventByCategory;
  private final SiteServeLoadEventByMarket siteServeLoadEventByMarket;
  private final SiteServeLoadEventById siteServeLoadEventById;

  public SiteServeLoadEvent getLoader(SelectionType selectionType) {
    switch (selectionType) {
      case CATEGORY:
        return siteServeLoadEventByCategory;
      case CLASS:
        return siteServeLoadEventByClass;
      case RACE_TYPE_ID:
        return siteServeLoadEventByRaceTypeId;
      case TYPE:
        return siteServeLoadEventByType;
      case SELECTION:
        return siteServeLoadEventBySelection;
      case ENHANCED_MULTIPLES:
        return siteServeLoadEventByEnhancedMultiples;
      case MARKET:
        return siteServeLoadEventByMarket;
      case EVENT:
        return siteServeLoadEventById;
      default:
        throw new IllegalArgumentException("SiteServeLoadEvent not found");
    }
  }
}
