package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.dto.LeagueLinkData;
import java.util.List;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotEmpty;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "leaguelinks")
@EqualsAndHashCode(callSuper = true)
@CompoundIndex(
    name = "coupon_league_unique_idx",
    def = "{'brand': 1, 'obLeagueId': 1, 'couponIds': 1}",
    unique = true)
@NoArgsConstructor
public class LeagueLink extends LeagueLinkData {

  public LeagueLink(
      String brand,
      boolean enabled,
      @NotEmpty List<Integer> couponIds,
      int obLeagueId,
      int dhLeagueId,
      @NotBlank String linkName) {
    super(brand, enabled, couponIds, obLeagueId, dhLeagueId, linkName);
  }
}
