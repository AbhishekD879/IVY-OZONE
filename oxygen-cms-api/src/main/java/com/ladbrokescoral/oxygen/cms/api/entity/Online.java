package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class Online extends NetworkStatus {
  private int timeout;
}
