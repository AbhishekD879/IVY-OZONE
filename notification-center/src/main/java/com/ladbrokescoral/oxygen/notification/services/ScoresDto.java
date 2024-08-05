package com.ladbrokescoral.oxygen.notification.services;

import java.util.Optional;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class ScoresDto {

  private long eventId;
  private Integer homeScore;
  private Integer awayScore;
  private Integer homePenalties;
  private Integer awayPenalties;
  private String scorer;
  private String penaltiesScorer;

  public Optional<Integer> maybeGetHomeScore() {
    return Optional.ofNullable(homeScore);
  }

  public Optional<Integer> maybeGetAwayScore() {
    return Optional.ofNullable(awayScore);
  }

  public Optional<Integer> maybeGetHomePenalties() {
    return Optional.ofNullable(homePenalties);
  }

  public Optional<Integer> maybeGetAwayPenalties() {
    return Optional.ofNullable(awayPenalties);
  }

  public Optional<String> maybeGetScorer() {
    return Optional.ofNullable(scorer);
  }

  public Optional<String> maybeGetPenaltiesScorer() {
    return Optional.ofNullable(penaltiesScorer);
  }
}
