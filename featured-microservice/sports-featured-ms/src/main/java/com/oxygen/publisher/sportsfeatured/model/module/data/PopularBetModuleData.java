package com.oxygen.publisher.sportsfeatured.model.module.data;

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

  private String position;

  private String objId;

  private boolean hideEventName;
}
