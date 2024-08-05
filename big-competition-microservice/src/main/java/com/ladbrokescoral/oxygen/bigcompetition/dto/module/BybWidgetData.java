package com.ladbrokescoral.oxygen.bigcompetition.dto.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.EventDto;
import java.time.Instant;
import java.util.List;
import lombok.Data;

@Data
public class BybWidgetData {

  private String title;
  private String eventId;
  private String marketId;
  private Instant displayFrom;
  private Instant displayTo;
  private Double sortOrder;
  private List<String> locations;
  private EventDto event;
}
