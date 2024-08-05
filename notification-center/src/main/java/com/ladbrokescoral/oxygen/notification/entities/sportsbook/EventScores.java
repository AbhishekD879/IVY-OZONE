package com.ladbrokescoral.oxygen.notification.entities.sportsbook;

import java.util.List;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
public class EventScores {
  private final String period;
  private final List<Team> teams;

  @Data
  @NoArgsConstructor
  public static class Team {
    private String name;

    private String roleCode;
    private int score;
    private int penalties;

    public Team(String name) {
      this.name = name;
    }

    public Team(String name, String roleCode) {
      this.name = name;
      this.roleCode = roleCode;
    }
  }
}
