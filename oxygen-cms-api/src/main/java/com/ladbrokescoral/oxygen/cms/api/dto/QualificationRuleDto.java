package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.Map;
import lombok.Data;

@Data
public class QualificationRuleDto {
  private String brand;
  private String message;
  private int daysToCheckActivity;
  private String blacklistedUsersPath;
  private Map<String, Boolean> recurringUsers;
}
