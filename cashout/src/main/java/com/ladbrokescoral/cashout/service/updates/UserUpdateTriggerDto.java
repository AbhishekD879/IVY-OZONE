package com.ladbrokescoral.cashout.service.updates;

import java.util.Set;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class UserUpdateTriggerDto {
  private final String token;
  private Set<String> betIds;
}
