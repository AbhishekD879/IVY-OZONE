package com.egalacoral.spark.timeform.model.horseracing;

import com.egalacoral.spark.timeform.model.Identity;
import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.text.MessageFormat;

/** Created by llegkyy on 31.08.16. */
public class HRPerformance extends Identity implements Serializable {
  private static final long serialVersionUID = 8943169002161049657L;

  @SerializedName(value = "meetingDate")
  private String meetingDate;

  @SerializedName(value = "courseId")
  private Integer courseId;

  @SerializedName(value = "raceNumber")
  private Integer raceNumber;

  @SerializedName(value = "horseCode")
  private String horseCode;

  @SerializedName(value = "courseName")
  private String courseName;

  @SerializedName(value = "horseName")
  private String horseName;

  @SerializedName(value = "horseAge")
  private Integer horseAge;

  @SerializedName(value = "horseGender")
  private String horseGender;

  @SerializedName(value = "positionStatus")
  private String positionStatus;

  @SerializedName(value = "positionOfficial")
  private Integer positionOfficial;

  @SerializedName(value = "positionPastPost")
  private Integer positionPastPost;

  @SerializedName(value = "draw")
  private Integer draw;

  @SerializedName(value = "weightCarried")
  private Integer weightCarried;

  @SerializedName(value = "overweight")
  private Integer overweight;

  @SerializedName(value = "jockeyName")
  private String jockeyName;

  @SerializedName(value = "apprenticeClaim")
  private Integer apprenticeClaim;

  @SerializedName(value = "trainerName")
  private String trainerName;

  @SerializedName(value = "ispDecimal")
  private Double ispDecimal;

  @SerializedName(value = "ispFractional")
  private String ispFractional;

  @SerializedName(value = "ispFavText")
  private String ispFavText;

  @SerializedName(value = "betfairWinSP")
  private Double betfairWinSP;

  @SerializedName(value = "betfairPlaceSP")
  private Double betfairPlaceSP;

  @SerializedName(value = "ipMax")
  private Double ipMax;

  @SerializedName(value = "ipMin")
  private Double ipMin;

  @SerializedName(value = "BSPAdvantage")
  private Double BSPAdvantage;

  @SerializedName(value = "distanceBeaten")
  private Double distanceBeaten;

  @SerializedName(value = "distanceBeatenStatus")
  private String distanceBeatenStatus;

  @SerializedName(value = "distanceCumulative")
  private Double distanceCumulative;

  @SerializedName(value = "equipmentDescription")
  private String equipmentDescription;

  @SerializedName(value = "equipmentChar")
  private String equipmentChar;

  @SerializedName(value = "handicapMark")
  private Integer handicapMark;

  @SerializedName(value = "longHandicap")
  private Integer longHandicap;

  @SerializedName(value = "performanceComment")
  private String performanceComment;

  @SerializedName(value = "preRaceEpf")
  private Double preRaceEpf;

  @SerializedName(value = "horseInFocus")
  private Integer horseInFocus;

  @SerializedName(value = "warningHorse")
  private Integer warningHorse;

  @SerializedName(value = "jockeyUplift")
  private Integer jockeyUplift;

  @SerializedName(value = "trainerUplift")
  private Integer trainerUplift;

  @SerializedName(value = "horsesForCoursePos")
  private Integer horsesForCoursePos;

  @SerializedName(value = "horsesForCoursesNeg")
  private Integer horsesForCoursesNeg;

  @SerializedName(value = "hotTrainer")
  private Integer hotTrainer;

  @SerializedName(value = "coldTrainer")
  private Integer coldTrainer;

  @SerializedName(value = "silkCode")
  private String silkCode;

  @SerializedName(value = "equipmentFirstTime")
  private Boolean equipmentFirstTime;

  @SerializedName(value = "jockeyCode")
  private String jockeyCode;

  @SerializedName(value = "trainerCode")
  private String trainerCode;

  @SerializedName(value = "ownerCode")
  private String ownerCode;

  @SerializedName(value = "ownerFullName")
  private String ownerFullName;

  @SerializedName(value = "topRated")
  private Boolean topRated;

  private HRJockey jockey;

  /**
   * Gets the value of the meetingDate property. EntityColumn: meetingDate | Standard Summary: The
   * date of the performance and part of the primary key Remark: Meeting Date In The Format
   * yyyy-mm-dd and is part of the primary key (PK)
   *
   * @return a String with Sentence Case value
   */
  public String getMeetingDate() {
    return meetingDate;
  }

  /**
   * Gets the value of the courseId property. EntityColumn: courseId | Standard Summary: The ID of
   * the course that the performance took place at and is part of the primary key Remark: Part of
   * the primary key (PK)
   *
   * @return an Integer value above 0
   */
  public Integer getCourseId() {
    return courseId;
  }

  /**
   * Gets the value of the raceNumber property. EntityColumn: raceNumber | Standard Summary: The
   * number of the race that the performance was in and is part of the primary key Remark: Part of
   * the primary key (PK)
   *
   * @return an Integer value above 0
   */
  public Integer getRaceNumber() {
    return raceNumber;
  }

  /**
   * Gets the value of the horseCode property. EntityColumn: horseCode | Standard Summary: The code
   * of the horse and is part of the primary key Remark: Part of the primary key (PK)
   *
   * @return a String(12) not null
   */
  public String getHorseCode() {
    return horseCode;
  }

  /**
   * Gets the value of the courseName property. EntityColumn: courseName | Standard Summary: The
   * full name of the course that the performance took place at Remark: An example: HAYDOCK PARK
   *
   * @return a String with Upper Case value
   */
  public String getCourseName() {
    return courseName;
  }

  /**
   * Gets the value of the horseName property. EntityColumn: horseName | Standard Summary: The full
   * name of the horse, including breeding suffix Remark: An example: KAUTO STAR (FR)
   *
   * @return a String with Upper Case value
   */
  public String getHorseName() {
    return horseName;
  }

  /**
   * Gets the value of the horseAge property. EntityColumn: horseAge | Standard Summary: The age of
   * the horse on the day of the race Remark: An example: 7
   *
   * @return an Integer value above 0
   */
  public Integer getHorseAge() {
    return horseAge;
  }

  /**
   * Gets the value of the horseGender property. EntityColumn: horseGender | Standard Summary: The
   * gender of the horse on the day of the race Remark: Values are : f - filly, m - mare, c - colt,
   * g - gelding, h - entire horse
   *
   * @return a String with Lower Case value
   */
  public String getHorseGender() {
    return horseGender;
  }

  /**
   * Gets the value of the positionStatus property. EntityColumn: positionStatus | Standard Summary:
   * Populated if the horse failed to complete or was disqualified Remark: F - Fell, pu - pulled up,
   * d - dq'd, ur - unseated rider
   *
   * @return a String with Title Case value
   */
  public String getPositionStatus() {
    return positionStatus;
  }

  /**
   * Gets the value of the positionOfficial property. EntityColumn: positionOfficial | Standard
   * Summary: The official finishing position of the horse Remark: 0 - horse failed to finish, an
   * example 1 - first
   *
   * @return an Integer with value 0 if the horse failed to finish, positive integer otherwise
   */
  public Integer getPositionOfficial() {
    return positionOfficial;
  }

  /**
   * Gets the value of the positionPastPost property. EntityColumn: positionPastPost | Standard
   * Summary: The order in which the horse passed the winning post (may differ from the official
   * position as a result of an enquiry) Remark: an example 1 - first past the post
   *
   * @return an Integer with value Above 0 - will give non finishers a position
   */
  public Integer getPositionPastPost() {
    return positionPastPost;
  }

  /**
   * Gets the value of the draw property. EntityColumn: draw | Standard Summary: The weight in
   * pounds the horse is set to carry (prior to 4/5 day declarations) Remark: 0 - pre 4/5 day
   * declarations, greater than 0 is the weight the horse will carry
   *
   * @return an Integer can be 0
   */
  public Integer getDraw() {
    return draw;
  }

  /**
   * Gets the value of the weightCarried property. EntityColumn: weightCarried | Standard Summary:
   * The weight in pounds the horse carried Remark: 0 - not available, greater than 0 is the weight
   * the horse carried
   *
   * @return an Integer can be 0
   */
  public Integer getWeightCarried() {
    return weightCarried;
  }

  /**
   * Gets the value of the overweight property. EntityColumn: overweight | Standard Summary: The
   * weight in pounds the jockey was found to be overweight Remark: 0 - not available, greater than
   * 0 the weight the jockey was overweight
   *
   * @return an Integer can be 0
   */
  public Integer getOverweight() {
    return overweight;
  }

  /**
   * Gets the value of the jockeyName property. EntityColumn: jockeyName | Standard Summary: The
   * full name of the jockey that rode the horse Remark: "" if no jockey was recorded, an example:
   * R. Walsh
   *
   * @return a String. Can be empty if no jockey was recorded for the ride
   */
  public String getJockeyName() {
    return jockeyName;
  }

  /**
   * Gets the value of the apprenticeClaim property. EntityColumn: apprenticeClaim | Standard
   * Summary:The amount in pounds that a horse will had removed from its weight as a result of the
   * jockey Remark: 0 = no claim, greater than 0 represents the weight that had taken off the horse
   *
   * @return an Integer can be 0
   */
  public Integer getApprenticeClaim() {
    return apprenticeClaim;
  }

  /**
   * Gets the value of the trainerName property. EntityColumn: trainerName | Standard Summary: The
   * full name of the trainer of the horse Remark: "" if no trainer is registered for the horse, an
   * example: Paul Nicholls
   *
   * @return a String. Can be empty if a trainer is not recorded against the horse
   */
  public String getTrainerName() {
    return trainerName;
  }

  /**
   * Gets the value of the ispDecimal property. EntityColumn: ispDecimal | Standard Summary: The
   * decimal price that the horse was at the start of the race Remark: 0.0 if the information wasn't
   * available, an example 1.0 = evens
   *
   * @return a Double. Will be 0.0 if the information wasn't available, greater than 0 is the price
   */
  public Double getIspDecimal() {
    return ispDecimal;
  }

  /**
   * Gets the value of the ispFractional property. EntityColumn: ispFractional | Standard Summary:
   * The price that the horse was at the start of the race Remark: "" if the information wasn't
   * available, an example: 2/1
   *
   * @return a String. Will be "" if the information wasn't available, otherwise it will be title
   *     case
   */
  public String getIspFractional() {
    return ispFractional;
  }

  /**
   * Gets the value of the ispFavText property. EntityColumn: ispFavText | Standard Summary: An
   * indicator as to whether the horse was favourite or joint favourite Remark: "" if the horse
   * wasn't favourite, an example cf - co favourite
   *
   * @return a String(2) with Title Case value
   */
  public String getIspFavText() {
    return ispFavText;
  }

  /**
   * Gets the value of the betfairWinSP property. EntityColumn: betfairWinSP | Standard Summary: The
   * decimal price that the horse was at the start of the race on Betfair to win Remark: 0.0 if the
   * information wasn't available, an example 2.0 = evens
   *
   * @return a Double. Will be 0.0 if the information wasn't available, greater than 0 is the price
   */
  public Double getBetfairWinSP() {
    return betfairWinSP;
  }

  /**
   * Gets the value of the betfairPlaceSP property. EntityColumn: betfairPlaceSP | Standard Summary:
   * The decimal price that the horse was at the start of the race on Betfair to place Remark: 0.0
   * if the information wasn't available, an example 2.0 = evens
   *
   * @return a Double. Will be 0.0 if the information wasn't available, greater than 0 is the price
   */
  public Double getBetfairPlaceSP() {
    return betfairPlaceSP;
  }

  /**
   * Gets the value of the ipMax property. EntityColumn: ipMax | Standard Summary: The highest price
   * the horse was matched during the race on Betfair(for a minimum stake) Remark: 0.0 if the
   * information wasn't available, an example 2.0 = evens
   *
   * @return a Double. Will be 0.0 if the information wasn't available, greater than 0 is the price
   */
  public Double getIpMax() {
    return ipMax;
  }

  /**
   * Gets the value of the ipMin property. EntityColumn: ipMin | Standard Summary: The lowest price
   * the horse was matched during the race on Betfair(for a minimum stake) Remark: 0.0 if the
   * information wasn't available, an example 2.0 = evens
   *
   * @return a Double. Will be 0.0 if the information wasn't available, greater than 0 is the price
   */
  public Double getIpMin() {
    return ipMin;
  }

  /**
   * Gets the value of the BSPAdvantage property. EntityColumn: BSPAdvantage | Standard Summary: The
   * betfair exchange advantage, displays as a percentage and takes 5% commission into account.
   * Remark: 0.0 if the information isn't available
   *
   * @return a Double. Will be 0.0 if the information wasn't available
   */
  public Double getBSPAdvantage() {
    return BSPAdvantage;
  }

  /**
   * Gets the value of the distanceBeaten property. EntityColumn: distanceBeaten | Standard Summary:
   * The decimal value for the number of lengths the horse was behind the horse that finished in
   * front of it Remark: 0.0 if the information wasn't available, an example 4.5 - 4 and a half
   * lengths
   *
   * @return a Double. Will be 0.0 if the information wasn't available, greater than 0 is the
   *     distance
   */
  public Double getDistanceBeaten() {
    return distanceBeaten;
  }

  /**
   * Gets the value of the distanceBeatenStatus property. EntityColumn: distanceBeatenStatus |
   * Standard Summary: The textual summary for the number of lengths the horse was behind the horse
   * that finished in front of it Remark: "" - information not available, an example: 1½
   *
   * @return a String. Will be ""if the information wasn't available, title case for the distance
   */
  public String getDistanceBeatenStatus() {
    return distanceBeatenStatus;
  }

  /**
   * Gets the value of the distanceCumulative property. EntityColumn: distanceCumulative | Standard
   * Summary: The decimal value for the total number of lengths the horse was behind the winner
   * Remark: 0.0 if the information wasn't available, an example 4.5 - 4 and a half lengths
   *
   * @return a Double. Will be 0.0 if the information wasn't available, greater than 0 is the
   *     distance
   */
  public Double getDistanceCumulative() {
    return distanceCumulative;
  }

  /**
   * Gets the value of the equipmentDescription property. EntityColumn: equipmentDescription |
   * Standard Summary: The full description of any headgear the horse wore Remark: "" if no
   * equipment, an example: "Blinkers"
   *
   * @return a String. Will be "" if the horse didn't wear any headgear, otherwise Title Case
   */
  public String getEquipmentDescription() {
    return equipmentDescription;
  }

  /**
   * Gets the value of the equipmentChar property. EntityColumn: equipmentChar | Standard Summary: A
   * char to represent the headgear any headgear the horse wore Remark: "" where no headgear wore,
   * an example: "b" blinkers
   *
   * @return a String(1). Will be "" if the horse isn't wearing any headgear, otherwise a single
   *     char
   */
  public String getEquipmentChar() {
    return equipmentChar;
  }

  /**
   * Gets the value of the handicapMark property. EntityColumn: handicapMark | Standard Summary: The
   * horses official handicap mark that it ran off Remark: 0 - no official mark, greater than 0 is
   * its official mark
   *
   * @return an Integer. 0 if the horse doesn't have an official rating, above 0 is its mark
   */
  public Integer getHandicapMark() {
    return handicapMark;
  }

  /**
   * Gets the value of the longHandicap property. EntityColumn: longHandicap | Standard Summary: The
   * weight in pounds that the horse was out of the handicap Remark: 0 where horse wasn't out of the
   * handicap, an example: 4 where the horse was 4 pounds out of the handicap
   *
   * @return an Integer. Will be 0 if the horses wasn't out of the handicap, above 0 when it was
   */
  public Integer getLongHandicap() {
    return longHandicap;
  }

  /**
   * Gets the value of the performanceComment property. EntityColumn: performanceComment | Standard
   * Summary: The short running notes for the horses performance Remark: "" - no notes available, an
   * example: "led, quickened, won"
   *
   * @return a String. "" if not available, title case if they are
   */
  public String getPerformanceComment() {
    return performanceComment;
  }

  /**
   * Gets the value of the preRaceEpf property. EntityColumn: preRaceEpf | Standard Summary: The
   * predicted early position figure that the horse had prior to the race based on past performances
   * Remark: 0 - not available or calculated, 1 - front runner, 5 - race in rear
   *
   * @return a Double. 0 where the EPF is uncalculated or not available, greater than 0 is the
   *     predicted position
   */
  public Double getPreRaceEpf() {
    return preRaceEpf;
  }

  /**
   * Gets the value of the horseInFocus property. EntityColumn: horseInFocus | Standard Summary:
   * Indicates if the horse was a Horse In Focus for this race Remark: True - horse is Horse In
   * Focus
   *
   * @return a Boolean. True or False
   */
  public Boolean getHorseInFocus() {
    return horseInFocus == 1;
  }

  /**
   * Gets the value of the warningHorse property. EntityColumn: warningHorse | Standard Summary:
   * Indicates if the horse was a Warning Horse for this race Remark: True - horse is a Warning
   * Horse
   *
   * @return a Boolean. True or False
   */
  public Boolean getWarningHorse() {
    return warningHorse == 1;
  }

  /**
   * Gets the value of the jockeyUplift property. EntityColumn: jockeyUplift | Standard Summary:
   * Indicates if the horse is a jockey uplift for this race Remark: True - horse is a jockey uplift
   *
   * @return a Boolean. True or False
   */
  public Boolean getJockeyUplift() {
    return jockeyUplift == 1;
  }

  /**
   * Gets the value of the trainerUplift property. EntityColumn: trainerUplift | Standard Summary:
   * Indicates if the horse was a trainer uplift for this race Remark: True - horse is a trainer
   * uplift
   *
   * @return a Boolean. True or False
   */
  public Boolean getTrainerUplift() {
    return trainerUplift == 1;
  }

  /**
   * Gets the value of the horsesForCoursePos property. EntityColumn: horsesForCoursePos | Standard
   * Summary: Indicates if the horse was a positive horses for courses for this race Remark: True -
   * horse is a positive horses for courses
   *
   * @return a Boolean. True or False
   */
  public Boolean getHorsesForCoursePos() {
    return horsesForCoursePos == 1;
  }

  /**
   * Gets the value of the horsesForCoursesNeg property. EntityColumn: horsesForCoursesNeg |
   * Standard Summary: Indicates if the horse was a negative horses for courses for this race
   * Remark: True - horse is a negative horses for courses
   *
   * @return a Boolean. True or False
   */
  public Boolean getHorsesForCoursesNeg() {
    return horsesForCoursesNeg == 1;
  }

  /**
   * Gets the value of the hotTrainer property. EntityColumn: hotTrainer | Standard Summary:
   * Indicates if the horse was a hot trainer for this race Remark: True - horse has a hot trainer
   *
   * @return a Boolean. True or False
   */
  public Boolean getHotTrainer() {
    return hotTrainer == 1;
  }

  /**
   * Gets the value of the coldTrainer property. EntityColumn: coldTrainer | Standard Summary:
   * Indicates if the horse was a cold trainer for this race Remark: True - horse has a cold trainer
   *
   * @return a Boolean. True or False
   */
  public Boolean getColdTrainer() {
    return coldTrainer == 1;
  }

  /**
   * Gets the value of the silkCode property. EntityColumn: silkCode | Standard Summary: The code of
   * the jockey silks to match image files Remark: "" - no silks available, an example:
   * "000000000001"
   *
   * @return a String. "" if no silks are available, string code if they are
   */
  public String getSilkCode() {
    return silkCode;
  }

  /**
   * Gets the value of the equipmentFirstTime property. EntityColumn: equipmentFirstTime | Standard
   * Summary: Flag to indicate this is the first time a horse has worn equipment Remark: True or
   * False
   *
   * @return a Boolean. True for yes, false for no
   */
  public Boolean getEquipmentFirstTime() {
    return equipmentFirstTime;
  }

  /**
   * Gets the value of the jockeyCode property. EntityColumn: jockeyCode | Standard Summary: The
   * code of the horse's jockey Remark: "" - no trainer available for the horse, an example:
   * "000000000001"
   *
   * @return a String. "" if the horse doesn't have a registered jockey for the performance, has a
   *     code if it does which corresponds to the jockey
   */
  public String getJockeyCode() {
    return jockeyCode;
  }

  /**
   * Gets the value of the trainerCode property. EntityColumn: trainerCode | Standard Summary: The
   * code of the horse's trainer Remark: "" - no trainer available for the horse, an example:
   * "000000000001"
   *
   * @return a String. "" if the horse doesn't have a registered trainer, has a code if it does
   *     which corresponds to the trainer
   */
  public String getTrainerCode() {
    return trainerCode;
  }

  /**
   * Gets the value of the ownerCode property. EntityColumn: ownerCode | Standard Summary: The code
   * of the owner of the horse Remark: "" if no owner is registered , an example: "000000000001" if
   * one has
   *
   * @return a String. Can be empty if an owner is not recorded against the horse
   */
  public String getOwnerCode() {
    return ownerCode;
  }

  /**
   * Gets the value of the ownerFullName property. EntityColumn: ownerFullName | Standard Summary:
   * The full name of the owner of the horse Remark: "" if no owner is registered for the horse, an
   * example: Gigginstown House Stud
   *
   * @return a String. Can be empty if an owner is not recorded against the horse, Title Case if it
   *     is
   */
  public String getOwnerFullName() {
    return ownerFullName;
  }

  /**
   * Gets the value of the topRated property. EntityColumn: topRated | Standard Summary: Flag to
   * indicate this horse was top rated based on Timeforms premium ratings Remark: True or False
   *
   * @return a Boolean. True for yes, false for no
   */
  public Boolean getTopRated() {
    return topRated;
  }

  /**
   * Gets the value of the jockey. EntityColumn: jockey | Standard Summary: Return value of jockeys
   * for performance Remark:
   *
   * @return HRJockey
   */
  public HRJockey getJockey() {
    return jockey;
  }

  public void setMeetingDate(String meetingDate) {
    this.meetingDate = meetingDate;
  }

  public void setCourseId(Integer courseId) {
    this.courseId = courseId;
  }

  public void setRaceNumber(Integer raceNumber) {
    this.raceNumber = raceNumber;
  }

  public void setHorseCode(String horseCode) {
    this.horseCode = horseCode;
  }

  public void setCourseName(String courseName) {
    this.courseName = courseName;
  }

  public void setHorseName(String horseName) {
    this.horseName = horseName;
  }

  public void setHorseAge(Integer horseAge) {
    this.horseAge = horseAge;
  }

  public void setHorseGender(String horseGender) {
    this.horseGender = horseGender;
  }

  public void setPositionStatus(String positionStatus) {
    this.positionStatus = positionStatus;
  }

  public void setPositionOfficial(Integer positionOfficial) {
    this.positionOfficial = positionOfficial;
  }

  public void setPositionPastPost(Integer positionPastPost) {
    this.positionPastPost = positionPastPost;
  }

  public void setDraw(Integer draw) {
    this.draw = draw;
  }

  public void setWeightCarried(Integer weightCarried) {
    this.weightCarried = weightCarried;
  }

  public void setOverweight(Integer overweight) {
    this.overweight = overweight;
  }

  public void setJockeyName(String jockeyName) {
    this.jockeyName = jockeyName;
  }

  public void setApprenticeClaim(Integer apprenticeClaim) {
    this.apprenticeClaim = apprenticeClaim;
  }

  public void setTrainerName(String trainerName) {
    this.trainerName = trainerName;
  }

  public void setIspDecimal(Double ispDecimal) {
    this.ispDecimal = ispDecimal;
  }

  public void setIspFractional(String ispFractional) {
    this.ispFractional = ispFractional;
  }

  public void setIspFavText(String ispFavText) {
    this.ispFavText = ispFavText;
  }

  public void setBetfairWinSP(Double betfairWinSP) {
    this.betfairWinSP = betfairWinSP;
  }

  public void setBetfairPlaceSP(Double betfairPlaceSP) {
    this.betfairPlaceSP = betfairPlaceSP;
  }

  public void setIpMax(Double ipMax) {
    this.ipMax = ipMax;
  }

  public void setIpMin(Double ipMin) {
    this.ipMin = ipMin;
  }

  public void setBSPAdvantage(Double BSPAdvantage) {
    this.BSPAdvantage = BSPAdvantage;
  }

  public void setDistanceBeaten(Double distanceBeaten) {
    this.distanceBeaten = distanceBeaten;
  }

  public void setDistanceBeatenStatus(String distanceBeatenStatus) {
    this.distanceBeatenStatus = distanceBeatenStatus;
  }

  public void setDistanceCumulative(Double distanceCumulative) {
    this.distanceCumulative = distanceCumulative;
  }

  public void setEquipmentDescription(String equipmentDescription) {
    this.equipmentDescription = equipmentDescription;
  }

  public void setEquipmentChar(String equipmentChar) {
    this.equipmentChar = equipmentChar;
  }

  public void setHandicapMark(Integer handicapMark) {
    this.handicapMark = handicapMark;
  }

  public void setLongHandicap(Integer longHandicap) {
    this.longHandicap = longHandicap;
  }

  public void setPerformanceComment(String performanceComment) {
    this.performanceComment = performanceComment;
  }

  public void setPreRaceEpf(Double preRaceEpf) {
    this.preRaceEpf = preRaceEpf;
  }

  public void setHorseInFocus(Boolean horseInFocus) {
    this.horseInFocus = horseInFocus ? 1 : 0;
  }

  public void setWarningHorse(Boolean warningHorse) {
    this.warningHorse = warningHorse ? 1 : 0;
  }

  public void setJockeyUplift(Boolean jockeyUplift) {
    this.jockeyUplift = jockeyUplift ? 1 : 0;
  }

  public void setTrainerUplift(Boolean trainerUplift) {
    this.trainerUplift = trainerUplift ? 1 : 0;
  }

  public void setHorsesForCoursePos(Boolean horsesForCoursePos) {
    this.horsesForCoursePos = horsesForCoursePos ? 1 : 0;
  }

  public void setHorsesForCoursesNeg(Boolean horsesForCoursesNeg) {
    this.horsesForCoursesNeg = horsesForCoursesNeg ? 1 : 0;
  }

  public void setHotTrainer(Boolean hotTrainer) {
    this.hotTrainer = hotTrainer ? 1 : 0;
  }

  public void setColdTrainer(Boolean coldTrainer) {
    this.coldTrainer = coldTrainer ? 1 : 0;
  }

  public void setSilkCode(String silkCode) {
    this.silkCode = silkCode;
  }

  public void setEquipmentFirstTime(Boolean equipmentFirstTime) {
    this.equipmentFirstTime = equipmentFirstTime;
  }

  public void setJockeyCode(String jockeyCode) {
    this.jockeyCode = jockeyCode;
  }

  public void setTrainerCode(String trainerCode) {
    this.trainerCode = trainerCode;
  }

  public void setOwnerCode(String ownerCode) {
    this.ownerCode = ownerCode;
  }

  public void setOwnerFullName(String ownerFullName) {
    this.ownerFullName = ownerFullName;
  }

  public void setTopRated(Boolean topRated) {
    this.topRated = topRated;
  }

  public void setJockey(HRJockey jockey) {
    this.jockey = jockey;
  }

  public String getPerfomanceId() {
    return MessageFormat.format("{0}:{1}:{2}:{3}", meetingDate, courseId, raceNumber, horseCode);
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("HRPerformance{");
    sb.append("meetingDate='").append(meetingDate).append('\'');
    sb.append(", courseId=").append(courseId);
    sb.append(", raceNumber=").append(raceNumber);
    sb.append(", horseCode='").append(horseCode).append('\'');
    sb.append(", courseName='").append(courseName).append('\'');
    sb.append(", horseName='").append(horseName).append('\'');
    sb.append(", horseAge=").append(horseAge);
    sb.append(", horseGender='").append(horseGender).append('\'');
    sb.append(", positionStatus='").append(positionStatus).append('\'');
    sb.append(", positionOfficial=").append(positionOfficial);
    sb.append(", positionPastPost=").append(positionPastPost);
    sb.append(", draw=").append(draw);
    sb.append(", weightCarried=").append(weightCarried);
    sb.append(", overweight=").append(overweight);
    sb.append(", jockeyName='").append(jockeyName).append('\'');
    sb.append(", apprenticeClaim=").append(apprenticeClaim);
    sb.append(", trainerName='").append(trainerName).append('\'');
    sb.append(", ispDecimal=").append(ispDecimal);
    sb.append(", ispFractional='").append(ispFractional).append('\'');
    sb.append(", ispFavText='").append(ispFavText).append('\'');
    sb.append(", betfairWinSP=").append(betfairWinSP);
    sb.append(", betfairPlaceSP=").append(betfairPlaceSP);
    sb.append(", ipMax=").append(ipMax);
    sb.append(", ipMin=").append(ipMin);
    sb.append(", BSPAdvantage=").append(BSPAdvantage);
    sb.append(", distanceBeaten=").append(distanceBeaten);
    sb.append(", distanceBeatenStatus='").append(distanceBeatenStatus).append('\'');
    sb.append(", distanceCumulative=").append(distanceCumulative);
    sb.append(", equipmentDescription='").append(equipmentDescription).append('\'');
    sb.append(", equipmentChar='").append(equipmentChar).append('\'');
    sb.append(", handicapMark=").append(handicapMark);
    sb.append(", longHandicap=").append(longHandicap);
    sb.append(", performanceComment='").append(performanceComment).append('\'');
    sb.append(", preRaceEpf=").append(preRaceEpf);
    sb.append(", horseInFocus=").append(horseInFocus);
    sb.append(", warningHorse=").append(warningHorse);
    sb.append(", jockeyUplift=").append(jockeyUplift);
    sb.append(", trainerUplift=").append(trainerUplift);
    sb.append(", horsesForCoursePos=").append(horsesForCoursePos);
    sb.append(", horsesForCoursesNeg=").append(horsesForCoursesNeg);
    sb.append(", hotTrainer=").append(hotTrainer);
    sb.append(", coldTrainer=").append(coldTrainer);
    sb.append(", silkCode='").append(silkCode).append('\'');
    sb.append(", equipmentFirstTime=").append(equipmentFirstTime);
    sb.append(", jockeyCode='").append(jockeyCode).append('\'');
    sb.append(", trainerCode='").append(trainerCode).append('\'');
    sb.append(", ownerCode='").append(ownerCode).append('\'');
    sb.append(", ownerFullName='").append(ownerFullName).append('\'');
    sb.append(", topRated=").append(topRated);
    sb.append(", jockey=").append(jockey);
    sb.append('}');
    return sb.toString();
  }
}
