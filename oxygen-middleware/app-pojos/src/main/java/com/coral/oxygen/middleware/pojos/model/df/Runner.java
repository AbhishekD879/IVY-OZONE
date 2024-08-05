package com.coral.oxygen.middleware.pojos.model.df;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;
import lombok.Data;

@Data
public class Runner implements Serializable {
  private String rating;
  private String dogcolour;
  private String bitchSeason;
  private String seeding;
  private String whelp;
  private String last5Runs;
  private String damName;
  private String bestRecentTime;
  private String dogSex;
  private Integer trap;
  private String lastRunTime;
  private Integer rpDogId;
  private String trainerName;
  private String dogName;
  private String sireName;
  private Map<String, Object> additionalProperties = new HashMap<>();
}
