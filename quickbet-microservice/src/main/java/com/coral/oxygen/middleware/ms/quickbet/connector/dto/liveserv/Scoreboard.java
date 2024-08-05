package com.coral.oxygen.middleware.ms.quickbet.connector.dto.liveserv;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import lombok.Data;

@Data
public class Scoreboard {

  @JsonProperty("ALL")
  private List<ScoreboardDetails> all;

  @JsonProperty("CURRENT")
  private List<ScoreboardDetails> current;

  @JsonProperty("SUBPERIOD")
  private List<ScoreboardDetails> subperiod;
}
