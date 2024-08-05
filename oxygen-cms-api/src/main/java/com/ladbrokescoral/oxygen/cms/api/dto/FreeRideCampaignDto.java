package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class FreeRideCampaignDto {
  private String id;
  private String name;
  private String displayFrom;
  private String displayTo;
  private String updatedAt;
  private String createdAt;
  private String updatedByUserName;
  private String createdByUserName;
  private Boolean isPotsCreated;
}
