package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;
import org.springframework.data.annotation.Id;

@Data
public class BetReceiptBannerDto {
  @Id private String id;
  private String name;
  private String uriMedium;
  private Boolean useDirectFileUrl;
  private String directFileUrl;
  private String validityPeriodStart;
  private String validityPeriodEnd;
}
