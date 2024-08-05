package com.ladbrokescoral.oxygen.cms.api.service.bpp.maintenance;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class BppMaintenanceResponse {
  private String url;
  private int code;
  private String status;
  private String message;
}
