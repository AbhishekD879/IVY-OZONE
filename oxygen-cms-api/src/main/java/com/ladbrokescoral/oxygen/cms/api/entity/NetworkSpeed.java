package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class NetworkSpeed {
  private SlowNetwork slow;
  private Online online;
  private Offline offline;
}
