package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class ModuleRibbonTabDto {
  private String title;
  private Boolean visible;
  private Integer hubIndex;
  private Instant displayFrom;
  private Instant displayTo;
  private Boolean bybVisble;
}
