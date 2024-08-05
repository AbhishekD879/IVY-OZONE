package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class BadgeTypeDto {
  private String name;
  private Integer numberOfBadges;
  private String congratsMsg;
  private String prizeType;
  private Integer amount;
}
