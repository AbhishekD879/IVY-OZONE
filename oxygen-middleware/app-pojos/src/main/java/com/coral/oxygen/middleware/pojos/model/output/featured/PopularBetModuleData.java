package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "objId")
public class PopularBetModuleData extends EventsModuleData {

  private int nBets;
  private int rank;
  private int previousRank;
  // property to bind id.
  private String objId;

  private String position;

  private boolean hideEventName;

  public PopularBetModuleData() {
    this.type = "PopularBetModuleData";
  }

  @ChangeDetect
  public int getnBets() {
    return nBets;
  }

  @ChangeDetect
  public int getRank() {
    return rank;
  }

  @ChangeDetect
  public int getPreviousRank() {
    return previousRank;
  }

  public String getPosition() {
    return position;
  }
}
