package com.gvc.oxygen.betreceipts.dto;

import java.io.Serializable;
import lombok.Data;

@Data
public class HorseDTO implements Serializable {

  private String trainer;
  private String rating;
  private String weight;
  private String silkCoral;
  private Integer horseAge;
  private String jockey;
  private String silkLadbrokes;
  private String silk;
  private String starRating;
  private Integer rpJockeyId;
  private Integer rpHorseId;
  private Integer rpTrainerId;
  private Integer weightLbs;
  private String courseDistanceWinner;

  private String horseName;
  private String spotlight;
  private String owner;
  private String rpRating;
  private Boolean isBeatenFavourite;
  private Boolean isMostTipped;
  private String horseSuffix;
  // findOne.orElse -1
  private Integer saddle = -1;
}
