package com.ladbrokescoral.oxygen.cms.api.service.impl;

import java.util.Set;
import lombok.Data;

@Data
public class InvalidateCacheResult {
  private final int responseCode;
  private final String message;
  private final String serviceType;
  private final Set<String> invalidatedItems;
}
