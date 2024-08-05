package com.oxygen.publisher.sportsfeatured.model.module.data;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class TrendingPosition {

  @EqualsAndHashCode.Include private PopularBetModuleData event;

  private int nBets;

  private int rank;

  private int previousRank;

  private String position;
}
