package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class PromoMsgLbConfigDto {
  private String leaderboardId;
  private String filePath;

  public PromoMsgLbConfigDto(String leaderboardId) {
    this.leaderboardId = leaderboardId;
  }
}
