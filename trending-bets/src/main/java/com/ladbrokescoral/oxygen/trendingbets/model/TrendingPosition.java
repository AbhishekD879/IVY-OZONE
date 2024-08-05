package com.ladbrokescoral.oxygen.trendingbets.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class TrendingPosition implements Comparable<TrendingPosition> {

  @EqualsAndHashCode.Include private TrendingEvent event;
  private int nBets;
  private int rank;
  private int previousRank;

  @JsonProperty("position")
  public String getPosition() {
    if (rank == previousRank) {
      return "-";
    } else {
      return (previousRank == 0 || rank < previousRank) ? "UP" : "DOWN";
    }
  }

  @Override
  public int compareTo(TrendingPosition o) {
    return Integer.compare(rank, o.getRank());
  }
}
