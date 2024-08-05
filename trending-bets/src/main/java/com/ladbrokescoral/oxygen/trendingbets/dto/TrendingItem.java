package com.ladbrokescoral.oxygen.trendingbets.dto;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class TrendingItem {
  @JsonProperty("odds")
  float odds;

  @JsonProperty("event_start_time")
  String eventDateTime;

  @JsonProperty("event_key")
  String eventId;

  @JsonProperty("event_name")
  String eventName;

  @JsonProperty("market_key")
  String marketId;

  @JsonProperty("market_name")
  String marketName;

  @JsonProperty("selection_key")
  @JsonAlias("src_result_id")
  String selectionId;

  @JsonProperty("selection_name")
  String selectionName;

  @JsonProperty("n_bets")
  @JsonAlias("n_backed_times")
  int nBets;

  @JsonProperty("rank")
  int rank;

  int previousRank;

  private String selectionLivesChannel;
  private Boolean suspended;
  private Boolean isStarted;

  private TrendingEvent trendingEvent;
}
