package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class BadgeDto {
  private String id;
  private String brand;
  private String label;
  private String rulesDisplay;
  private boolean lastUpdatedFlag;
  private String viewButtonLabel;
  private boolean viewButton;
  private String lbrRedirectionUrl;
  private String lbrRedirectionLabel;
  private boolean viewLbrUrl;
  private boolean viewBadges;
}
