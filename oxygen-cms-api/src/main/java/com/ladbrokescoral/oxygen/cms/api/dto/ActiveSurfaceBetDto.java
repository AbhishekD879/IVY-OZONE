package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
@AllArgsConstructor
public class ActiveSurfaceBetDto {
  private String id;
  private boolean disabled;
  private boolean highlightsTabOn;
  private boolean edpOn;
  private boolean displayOnDesktop;
}
