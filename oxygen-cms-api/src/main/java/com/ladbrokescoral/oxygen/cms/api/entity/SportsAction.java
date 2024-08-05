package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;
import lombok.NonNull;

@Data
public class SportsAction {

  @NonNull private String action;
  @NonNull private String messagingContent;
  @NonNull private String gcLink;
  @NonNull private Boolean enabled;
}
