package com.coral.oxygen.edp.tracking.model;

import java.io.Serializable;
import lombok.*;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode
public class HorseDTO implements Serializable {

  private String trainer;
  private String rating;
  private String weight;
  private String silkCoral;
  private Integer horseAge;
  private String jockey;
  private String silk;
  private String starRating;
  private Integer weightLbs;
  private String courseDistanceWinner;
  private String horseName;
  private String owner;
  private String rpRating;
  private Boolean isBeatenFavourite;
  private Boolean isMostTipped;
  private String horseSuffix;
  // findOne.orElse -1
  private Integer saddle = -1;
  private String draw;
}
