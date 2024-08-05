package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SelectionType;
import java.time.Instant;
import java.util.List;

public interface HomeModuleSiteServeService {
  List<SiteServeEventDto> loadEventsFromSiteServe(
      String brand,
      SelectionType selectionType,
      String selectionId,
      Instant dateFrom,
      Instant dateTo);
}
