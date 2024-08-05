package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;

@Data
public class BadgeType {

  @NotBlank private String name;

  @NotNull private Integer numberOfBadges;

  private String congratsMsg;

  @NotBlank private String prizeType;

  @NotNull private Integer amount;
}
