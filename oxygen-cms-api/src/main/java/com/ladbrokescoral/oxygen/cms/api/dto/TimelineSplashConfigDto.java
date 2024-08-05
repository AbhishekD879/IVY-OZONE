package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class TimelineSplashConfigDto {
  private String id;

  private boolean showSplashPage;
  private String text;
}
