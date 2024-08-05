package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.ToString;
import lombok.Value;

@Value
public class AccountCredentials {
  private final String username;
  @ToString.Exclude private final String password;
}
