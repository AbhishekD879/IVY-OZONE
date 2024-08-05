package com.ladbrokescoral.oxygen.trendingbets.model;

import java.util.Set;
import lombok.Data;
import lombok.experimental.SuperBuilder;

@Data
@SuperBuilder
public class PersonalizedBetsDto extends TrendingBetsDto {

  private boolean isNewUser;

  private Set<TrendingPosition> fzYourTeamPositions;

  private Set<TrendingPosition> fzOtherTeamPositions;
}
