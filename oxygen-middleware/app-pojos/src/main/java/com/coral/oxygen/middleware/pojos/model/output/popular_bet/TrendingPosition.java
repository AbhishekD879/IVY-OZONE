package com.coral.oxygen.middleware.pojos.model.output.popular_bet;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.IdHolder;
import com.coral.oxygen.middleware.pojos.model.output.featured.PopularBetModuleData;
import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class TrendingPosition implements Serializable, IdHolder {

  @EqualsAndHashCode.Include private PopularBetModuleData event;

  @SerializedName("nbets")
  private int nBets;

  private int rank;

  private int previousRank;

  private String position;

  @Override
  public String idForChangeDetection() {
    return event.getId().toString();
  }

  @ChangeDetect(compareNestedObject = true)
  public PopularBetModuleData getEvent() {
    return event;
  }
}
