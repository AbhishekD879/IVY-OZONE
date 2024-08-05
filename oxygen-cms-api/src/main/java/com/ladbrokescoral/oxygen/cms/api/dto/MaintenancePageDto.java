package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class MaintenancePageDto {
  private String name;
  private String uriMedium;
  private String uriOriginal;
  private String targetUri;
  private String validityPeriodStart;
  private String validityPeriodEnd;
}
