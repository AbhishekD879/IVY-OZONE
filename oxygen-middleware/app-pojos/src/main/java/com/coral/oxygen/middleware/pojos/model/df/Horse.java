package com.coral.oxygen.middleware.pojos.model.df;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.Data;

@Data
public class Horse implements Serializable {
  private static final long serialVersionUID = 1982646659071262347L;

  private String trainer;
  private String rating;
  private String weight;
  private String breedingComment;
  private String sireComment;
  private String silkCoral;
  private Integer horseAge;
  private String jockey;
  private String silkLadbrokes;
  private String silk;
  private String starRating;
  private Integer rpJockeyId;
  private String adjustedMasterRating;
  private String daysSinceRun;
  private Integer rpHorseId;
  private String draw;
  private String diomedComment;
  private Integer rpTrainerId;
  private List<Form> form = new ArrayList<>();
  private String formfigs;
  private Integer saddle;
  private Integer weightLbs;
  private String courseDistanceWinner;
  private String horseName;
  private String spotlight;
  private String owner;
  private String officialRating;
  private String rpRating;
  private Boolean isBeatenFavourite;
  private String isReservedRunner;
  private String horseSuffix;
  private String headgear;
  private Integer allowance;
  private Map<String, Object> additionalProperties = new HashMap<>();

  public void setAdditionalProperty(String name, Object value) {
    this.additionalProperties.put(name, value);
  }
}
