package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.wildfly.common.annotation.NotNull;

@Data
@NoArgsConstructor
public class NetworkStatus {
  @NotNull private String displayText;
}
