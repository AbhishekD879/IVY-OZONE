package com.ladbrokescoral.cashout.service;

import java.time.Duration;
import java.util.List;
import lombok.Builder;
import lombok.Data;
import lombok.Singular;
import org.springframework.util.CollectionUtils;

@Data
@Builder
public class BetDetailMeta {
  private String token;
  private String username;
  private Duration tokenExpiresIn;
  @Singular private List<String> betIds;
  private long connectionAgeInSeconds;
  private String reasonForUpdate;

  public boolean hasBets() {
    return !CollectionUtils.isEmpty(betIds);
  }
}
