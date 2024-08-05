package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;
import org.springframework.data.annotation.Id;

@Data
public class FootballBanner3dDto {
  @Id private String id;
  private String name;
  private String uriMedium;
  private Integer displayDuration;
  private String validityPeriodStart;
  private String validityPeriodEnd;
}
