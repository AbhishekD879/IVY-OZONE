package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.NetworkSpeed;
import lombok.Data;
import org.wildfly.common.annotation.NotNull;

@Data
public class NetworkIndicatorRequest {
  @NotNull private boolean networkIndicatorEnabled;
  private boolean debugLogEnabled;
  private int pollingInterval;
  private NetworkSpeed networkSpeed;
  private int thresholdTime;
  private int slowTimeout;
  private String imageURL;
  private String brand;
}
