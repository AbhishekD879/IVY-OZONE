package com.ladbrokescoral.oxygen.cms.api.service.bpp.maintenance;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;

@Setter
@Getter
@RequiredArgsConstructor
public class BppMaintenanceRequest {
  private String secret;
  private final boolean active;
  // ttl in seconds expected
  private final long ttl;
}
