package com.ladbrokescoral.cashout.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RedisSaverLock {

  private long timestamp;
  private String uuid;
}
