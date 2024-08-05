package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.wildfly.common.annotation.NotNull;

@Data
@NoArgsConstructor
public class SlowNetwork extends NetworkStatus {
  @NotNull private String infoMsg;
}
