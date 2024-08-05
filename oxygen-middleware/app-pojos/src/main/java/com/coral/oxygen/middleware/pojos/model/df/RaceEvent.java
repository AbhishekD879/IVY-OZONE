package com.coral.oxygen.middleware.pojos.model.df;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.Data;

@Data
public class RaceEvent implements Serializable {
  private static final long serialVersionUID = -3273602747602290970L;

  private List<Integer> ladbrokesDigitalEventId = new ArrayList<>();
  private List<Integer> coralDigitalEventId = new ArrayList<>();
  private String diomed;
  private String courseName;
  private String goingCode;
  private String going;
  private String obStartTime;
  private Integer rpCourseId;
  private String courseGraphicsLadbrokes;
  private List<Horse> horses = new ArrayList<>();
  private String courseGraphicsCoral;
  private String raceName;
  private Integer yards;
  private String distance;
  private List<Newspaper> newspapers = new ArrayList<>();
  private Integer raceNo;
  private String verdict;
  private String time;
  private Integer rpRaceId;
  private Boolean isAllWeather;
  private Boolean isHandicap;
  private String flatOrJump;
  private String raceType;
  private String tv;
  private Integer raceClass;
  private String agesAllowed;
  private String ageLimitation;
  private String openAgeRace;
  private Integer runnerCount;
  private Integer thoroughbredRaceNo;
  private Integer trackFences;
  private Double prize1;
  private Double prize2;
  private Double prize3;
  private Double prize4;
  private Double prize5;
  private Double prize6;
  private List<Trend> trends = new ArrayList<>();
  private List<Keystat> keystat = new ArrayList<>();

  // Grayhound fields
  private List<Integer> ladbrokesRetailEventId = null;
  private List<Integer> coralRetailEventId = null;
  private String bags;
  private String postPick;
  private String grade;
  private Integer rpTrackId;
  private String prize;
  private String abandoned;
  private List<Runner> runners = new ArrayList<>();
  private String fileType;

  private Map<String, Object> additionalProperties = new HashMap<>();
}
