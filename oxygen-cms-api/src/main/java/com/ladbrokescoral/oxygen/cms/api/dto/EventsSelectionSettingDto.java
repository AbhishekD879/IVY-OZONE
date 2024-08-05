package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import lombok.Data;

@Data
public class EventsSelectionSettingDto {
  private Instant from;
  private Instant to;
}
