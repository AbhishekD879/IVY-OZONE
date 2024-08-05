package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.SpotlightEvents;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.spotlight.SpotlightEventInfo;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineSpotlightService;
import java.time.Instant;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.apache.commons.lang3.StringUtils;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("v1/api/timeline/spotlight")
public class TimelineSpotlightController {
  public static final String DEFAULT_CLASSID_STRING = "226";

  private final TimelineSpotlightService service;

  public TimelineSpotlightController(TimelineSpotlightService crudService) {
    this.service = crudService;
  }

  @GetMapping("/brand/{brand}/campaignId/{campaignId}/spotlight-data/{eventId}")
  public SpotlightEventInfo fetchSpotlightDataForEventId(
      @PathVariable("brand") String brand,
      @PathVariable("campaignId") String campaignId,
      @PathVariable("eventId") String eventId) {
    return this.service.fetchSpotlightData(brand, eventId);
  }

  @PostMapping("/brand/{brand}/related-events")
  public SpotlightEvents refreshData(
      @PathVariable("brand") String brand, @RequestBody RefreshSiteserveEventsQuery query) {
    verifyQuery(query);
    return this.service.fetchSiteServeDataForBrandByApi(brand, query);
  }

  private void verifyQuery(RefreshSiteserveEventsQuery query) {
    if (query.getRefreshEventsFrom() == null) {
      query.setRefreshEventsFrom(Instant.now());
    }
    if (StringUtils.isBlank(query.getRefreshEventsClassesString())) {
      query.setRefreshEventsClassesString(DEFAULT_CLASSID_STRING);
    }
  }

  @Data
  @AllArgsConstructor
  @NoArgsConstructor
  public static class RefreshSiteserveEventsQuery {
    private Instant refreshEventsFrom;
    private String refreshEventsClassesString;
    private boolean restrictToUkAndIre = true;
  }
}
