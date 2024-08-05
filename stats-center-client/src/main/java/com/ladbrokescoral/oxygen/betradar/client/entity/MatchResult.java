package com.ladbrokescoral.oxygen.betradar.client.entity;

import java.util.List;
import lombok.Data;

@Data
public class MatchResult {

  private String commentary;
  private List<Score> scores;
}
