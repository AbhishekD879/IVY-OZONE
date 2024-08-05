package com.ladbrokescoral.oxygen.trendingbets.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import lombok.Builder;
import lombok.Getter;

@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ADARequestModel {

  @JsonProperty("players")
  private List<String> players;

  @JsonProperty("max_legs_to_rec")
  private Integer maxLegsToRec;

  @JsonProperty("player_max_rec_count")
  private Integer playerMaxRecCount;

  @JsonProperty("handle_missing_players")
  private boolean handleMissingPlayers;

  @JsonProperty("recommend_modal_bet")
  private boolean recommendModelBet;

  @JsonProperty("personalized_recs")
  private boolean personalizedRecs;

  @JsonProperty("fanzone_widget_recs")
  @Getter
  private boolean fanzoneWidgetRecs;

  @JsonProperty("fanzone_team_id")
  private String fanzoneTeamId;
}
