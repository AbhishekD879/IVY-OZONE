package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.util.List;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotEmpty;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public class LeagueLinkDto extends LeagueLinkData {

  public LeagueLinkDto(
      String brand,
      boolean enabled,
      @NotEmpty List<Integer> couponIds,
      int obLeagueId,
      int dhLeagueId,
      @NotBlank String linkName) {
    super(brand, enabled, couponIds, obLeagueId, dhLeagueId, linkName);
  }
}
