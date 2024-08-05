package com.egalacoral.spark.timeform.model.horseracing;

import com.egalacoral.spark.timeform.model.OBRelatedEntity;
import com.egalacoral.spark.timeform.model.greyhound.TimeformEntry;
import com.egalacoral.spark.timeform.model.greyhound.TimeformRace;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.Collection;
import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

public class HRRace extends OBRelatedEntity implements Serializable, TimeformRace {

  @SerializedName(value = "raceId")
  private String raceId;

  @SerializedName(value = "meetingDate")
  private String meetingDate;

  @SerializedName(value = "courseId")
  private Integer courseId;

  @SerializedName(value = "raceNumber")
  private Integer raceNumber;

  @SerializedName(value = "courseName")
  private String courseName;

  @SerializedName(value = "courseAbbrev")
  private String courseAbbrev;

  @SerializedName(value = "startTimeLocalScheduled")
  private String startTimeLocalScheduled;

  @SerializedName(value = "startTimeGMTScheduled")
  private String startTimeGMTScheduled;

  @SerializedName(value = "actualTimeLocalScheduled")
  private String actualTimeLocalScheduled;

  @SerializedName(value = "actualTimeGMTScheduled")
  private String actualTimeGMTScheduled;

  @SerializedName(value = "raceSurfaceChar")
  private String raceSurfaceChar;

  @SerializedName(value = "raceSurfaceName")
  private String raceSurfaceName;

  @SerializedName(value = "raceType")
  private String raceType;

  @SerializedName(value = "distanceFurlongs")
  private Integer distanceFurlongs;

  @SerializedName(value = "distanceYards")
  private Integer distanceYards;

  @SerializedName(value = "distance")
  private Double distance;

  @SerializedName(value = "distanceText")
  private String distanceText;

  @SerializedName(value = "raceTitle")
  private String raceTitle;

  @SerializedName(value = "raceTitleShort")
  private String raceTitleShort;

  @SerializedName(value = "going")
  private String going;

  @SerializedName(value = "goingAbbrev")
  private String goingAbbrev;

  @SerializedName(value = "goingOfficial")
  private String goingOfficial;

  @SerializedName(value = "eligibilityAgeMax")
  private String eligibilityAgeMax;

  @SerializedName(value = "eligibilityAgeMin")
  private String eligibilityAgeMin;

  @SerializedName(value = "numberOfRunners")
  private Integer numberOfRunners;

  @SerializedName(value = "numberOfPlaces")
  private Integer numberOfPlaces;

  @SerializedName(value = "eligibilitySexLimit")
  private String eligibilitySexLimit;

  @SerializedName(value = "resultsStatus")
  private String resultsStatus;

  @SerializedName(value = "raceTypeChar")
  private String raceTypeChar;

  @SerializedName(value = "raceCode")
  private String raceCode;

  @SerializedName(value = "prizeFund")
  private String prizeFund;

  @SerializedName(value = "prizeFundWinner")
  private String prizeFundWinner;

  @SerializedName(value = "analystVerdict")
  private String analystVerdict;

  @SerializedName(value = "drawComment")
  private String drawComment;

  @SerializedName(value = "ipHintsGeneral")
  private String ipHintsGeneral;

  @SerializedName(value = "ipHintsPriceRunStyle")
  private String ipHintsPriceRunStyle;

  @SerializedName(value = "iPriceHistory")
  private String iPriceHistory;

  @SerializedName(value = "ipHintsOverallPace")
  private String ipHintsOverallPace;

  @SerializedName(value = "ipHintsSpecificPace")
  private String ipHintsSpecificPace;

  @SerializedName(value = "raceStateId")
  private Integer raceStateId;

  @SerializedName(value = "ratingLimitLower")
  private Integer ratingLimitLower;

  @SerializedName(value = "ratingLimitUpper")
  private Integer ratingLimitUpper;

  @SerializedName(value = "raceClass")
  private String raceClass;

  @SerializedName(value = "smartStat1")
  private String smartStat1;

  @SerializedName(value = "smartStat2")
  private String smartStat2;

  @SerializedName(value = "smartStat3")
  private String smartStat3;

  @SerializedName(value = "bfMarketId")
  private String bfMarketId;

  @SerializedName(value = "finishingTime")
  private String finishingTime;

  @SerializedName(value = "numberOfFencesJumped")
  private Integer numberOfFencesJumped;

  @SerializedName(value = "publishFlag")
  private Integer publishFlag;

  private String courseMapId;

  private Collection<HREntry> entries;

  @JsonIgnore private transient HRRace.HRRaceKey key;

  /**
   * Legacy RaceID in the format Country.Course.Date.RaceNumber e.g. 1.339.1160824.6
   *
   * @return String Remarks: An example: 1.339.1160824.6
   */
  public String getRaceId() {
    return raceId;
  }

  /**
   * The date of the meeting and part of the primary key Value: Not Null
   *
   * @return Date Remarks: Meeting Date In The Format yyy-mm-dd
   */
  public String getMeetingDate() {
    return meetingDate;
  }

  /**
   * The ID of the course that the race took place at and is part of the primary key Value: Above 0
   *
   * @return Integer Remarks: Part of the primary key (PK)
   */
  public Integer getCourseId() {
    return courseId;
  }

  /**
   * The number of the race that and is part of the primary key Value:
   *
   * @return Remarks: Part of the primary key (PK)
   */
  public Integer getRaceNumber() {
    return raceNumber;
  }

  /**
   * The full name of the course that the performance took place at Value: Upper Case
   *
   * @return String Remarks: An example: HAYDOCK PARK
   */
  public String getCourseName() {
    return courseName;
  }

  /**
   * The 3 character course abbreviation Value: Title Case
   *
   * @return String(3) Remarks: An example: Hay
   */
  public String getCourseAbbrev() {
    return courseAbbrev;
  }

  /**
   * The time that the race was due to start where the race was being run Value: yyyy-mm-ddd
   * hh:mm:ss:ms
   *
   * @return Date Time Remarks: Defaults to 1990-01-01 00:00:00.000 if not available, an example:
   *     2012-02-19 13:10:00.000
   */
  public String getStartTimeLocalScheduled() {
    return startTimeLocalScheduled;
  }

  /**
   * The time that the race was due to start at GMT Value: yyyy-mm-ddd hh:mm:ss:ms
   *
   * @return Date Time Remarks: Defaults to 1990-01-01 00:00:00.000 if not available, an example:
   *     2012-02-19 13:10:00.000
   */
  public String getStartTimeGMTScheduled() {
    return startTimeGMTScheduled;
  }

  /**
   * The time that the race actually started where the race was being run Value: yyyy-mm-ddd
   * hh:mm:ss:ms
   *
   * @return Date Time Remarks: Defaults to 1990-01-01 00:00:00.000 if not available, an example:
   *     2012-02-19 13:10:00.000
   */
  public String getActualTimeLocalScheduled() {
    return actualTimeLocalScheduled;
  }

  /**
   * The time that the race actually started in GMT Value: yyyy-mm-ddd hh:mm:ss:ms
   *
   * @return Date Time Remarks: Defaults to 1990-01-01 00:00:00.000 if not available, an example:
   *     2012-02-19 13:10:00.000
   */
  public String getActualTimeGMTScheduled() {
    return actualTimeGMTScheduled;
  }

  /**
   * The type of surface that is being used for the race Value: Title Case
   *
   * @return String Remarks: Values are All Weather or Turf
   */
  public String getRaceSurfaceChar() {
    return raceSurfaceChar;
  }

  /**
   * The one character representation of the type of surface of the race Value: Title Case
   *
   * @return String Remarks: Values are A or T
   */
  public String getRaceSurfaceName() {
    return raceSurfaceName;
  }

  /**
   * The type of racing Value: Title Case
   *
   * @return Remarks: Values are Flat, Hurdle, Chase, Bumper
   */
  public String getRaceType() {
    return raceType;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public Integer getDistanceFurlongs() {
    return distanceFurlongs;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public Integer getDistanceYards() {
    return distanceYards;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public Double getDistance() {
    return distance;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getDistanceText() {
    return distanceText;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getRaceTitle() {
    return raceTitle;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getRaceTitleShort() {
    return raceTitleShort;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getGoing() {
    return going;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getGoingAbbrev() {
    return goingAbbrev;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getGoingOfficial() {
    return goingOfficial;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getEligibilityAgeMax() {
    return eligibilityAgeMax;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getEligibilityAgeMin() {
    return eligibilityAgeMin;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public Integer getNumberOfRunners() {
    return numberOfRunners;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public Integer getNumberOfPlaces() {
    return numberOfPlaces;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getEligibilitySexLimit() {
    return eligibilitySexLimit;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getResultsStatus() {
    return resultsStatus;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getRaceTypeChar() {
    return raceTypeChar;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getRaceCode() {
    return raceCode;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getPrizeFund() {
    return prizeFund;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getPrizeFundWinner() {
    return prizeFundWinner;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getAnalystVerdict() {
    return analystVerdict;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getDrawComment() {
    return drawComment;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getIpHintsGeneral() {
    return ipHintsGeneral;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getIpHintsPriceRunStyle() {
    return ipHintsPriceRunStyle;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getiPriceHistory() {
    return iPriceHistory;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getIpHintsOverallPace() {
    return ipHintsOverallPace;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getIpHintsSpecificPace() {
    return ipHintsSpecificPace;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public Integer getRaceStateId() {
    return raceStateId;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public Integer getRatingLimitLower() {
    return ratingLimitLower;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public Integer getRatingLimitUpper() {
    return ratingLimitUpper;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getRaceClass() {
    return raceClass;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getSmartStat1() {
    return smartStat1;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getSmartStat2() {
    return smartStat2;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getSmartStat3() {
    return smartStat3;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getBfMarketId() {
    return bfMarketId;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public String getFinishingTime() {
    return finishingTime;
  }

  /**
   * Shows the number of fences jumped during the race, not available until 24 hours after the race:
   * Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public Integer getNumberOfFencesJumped() {
    return numberOfFencesJumped;
  }

  /**
   * The number of complete furlongs the race will be run over Value: Above 0
   *
   * @return Integer Remarks: an example: 8
   */
  public Integer getPublishFlag() {
    return publishFlag;
  }

  public String getCourseMapId() {
    return courseMapId;
  }

  public void setRaceId(String raceId) {
    this.raceId = raceId;
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

  public void setCourseName(String courseName) {
    this.courseName = courseName;
  }

  public void setCourseAbbrev(String courseAbbrev) {
    this.courseAbbrev = courseAbbrev;
  }

  public void setStartTimeLocalScheduled(String startTimeLocalScheduled) {
    this.startTimeLocalScheduled = startTimeLocalScheduled;
  }

  public void setStartTimeGMTScheduled(String startTimeGMTScheduled) {
    this.startTimeGMTScheduled = startTimeGMTScheduled;
  }

  public void setActualTimeLocalScheduled(String actualTimeLocalScheduled) {
    this.actualTimeLocalScheduled = actualTimeLocalScheduled;
  }

  public void setActualTimeGMTScheduled(String actualTimeGMTScheduled) {
    this.actualTimeGMTScheduled = actualTimeGMTScheduled;
  }

  public void setRaceSurfaceChar(String raceSurfaceChar) {
    this.raceSurfaceChar = raceSurfaceChar;
  }

  public void setRaceSurfaceName(String raceSurfaceName) {
    this.raceSurfaceName = raceSurfaceName;
  }

  public void setRaceType(String raceType) {
    this.raceType = raceType;
  }

  public void setDistanceFurlongs(Integer distanceFurlongs) {
    this.distanceFurlongs = distanceFurlongs;
  }

  public void setDistanceYards(Integer distanceYards) {
    this.distanceYards = distanceYards;
  }

  public void setDistance(Double distance) {
    this.distance = distance;
  }

  public void setDistanceText(String distanceText) {
    this.distanceText = distanceText;
  }

  public void setRaceTitle(String raceTitle) {
    this.raceTitle = raceTitle;
  }

  public void setRaceTitleShort(String raceTitleShort) {
    this.raceTitleShort = raceTitleShort;
  }

  public void setGoing(String going) {
    this.going = going;
  }

  public void setGoingAbbrev(String goingAbbrev) {
    this.goingAbbrev = goingAbbrev;
  }

  public void setGoingOfficial(String goingOfficial) {
    this.goingOfficial = goingOfficial;
  }

  public void setEligibilityAgeMax(String eligibilityAgeMax) {
    this.eligibilityAgeMax = eligibilityAgeMax;
  }

  public void setEligibilityAgeMin(String eligibilityAgeMin) {
    this.eligibilityAgeMin = eligibilityAgeMin;
  }

  public void setNumberOfRunners(Integer numberOfRunners) {
    this.numberOfRunners = numberOfRunners;
  }

  public void setNumberOfPlaces(Integer numberOfPlaces) {
    this.numberOfPlaces = numberOfPlaces;
  }

  public void setEligibilitySexLimit(String eligibilitySexLimit) {
    this.eligibilitySexLimit = eligibilitySexLimit;
  }

  public void setResultsStatus(String resultsStatus) {
    this.resultsStatus = resultsStatus;
  }

  public void setRaceTypeChar(String raceTypeChar) {
    this.raceTypeChar = raceTypeChar;
  }

  public void setRaceCode(String raceCode) {
    this.raceCode = raceCode;
  }

  public void setPrizeFund(String prizeFund) {
    this.prizeFund = prizeFund;
  }

  public void setPrizeFundWinner(String prizeFundWinner) {
    this.prizeFundWinner = prizeFundWinner;
  }

  public void setAnalystVerdict(String analystVerdict) {
    this.analystVerdict = analystVerdict;
  }

  public void setDrawComment(String drawComment) {
    this.drawComment = drawComment;
  }

  public void setIpHintsGeneral(String ipHintsGeneral) {
    this.ipHintsGeneral = ipHintsGeneral;
  }

  public void setIpHintsPriceRunStyle(String ipHintsPriceRunStyle) {
    this.ipHintsPriceRunStyle = ipHintsPriceRunStyle;
  }

  public void setiPriceHistory(String iPriceHistory) {
    this.iPriceHistory = iPriceHistory;
  }

  public void setIpHintsOverallPace(String ipHintsOverallPace) {
    this.ipHintsOverallPace = ipHintsOverallPace;
  }

  public void setIpHintsSpecificPace(String ipHintsSpecificPace) {
    this.ipHintsSpecificPace = ipHintsSpecificPace;
  }

  public void setRaceStateId(Integer raceStateId) {
    this.raceStateId = raceStateId;
  }

  public void setRatingLimitLower(Integer ratingLimitLower) {
    this.ratingLimitLower = ratingLimitLower;
  }

  public void setRatingLimitUpper(Integer ratingLimitUpper) {
    this.ratingLimitUpper = ratingLimitUpper;
  }

  public void setRaceClass(String raceClass) {
    this.raceClass = raceClass;
  }

  public void setSmartStat1(String smartStat1) {
    this.smartStat1 = smartStat1;
  }

  public void setSmartStat2(String smartStat2) {
    this.smartStat2 = smartStat2;
  }

  public void setSmartStat3(String smartStat3) {
    this.smartStat3 = smartStat3;
  }

  public void setBfMarketId(String bfMarketId) {
    this.bfMarketId = bfMarketId;
  }

  public void setFinishingTime(String finishingTime) {
    this.finishingTime = finishingTime;
  }

  public void setNumberOfFencesJumped(Integer numberOfFencesJumped) {
    this.numberOfFencesJumped = numberOfFencesJumped;
  }

  public void setPublishFlag(Integer publishFlag) {
    this.publishFlag = publishFlag;
  }

  public void setCourseMapId(String course_map_id) {
    this.courseMapId = course_map_id;
  }

  public Collection<HREntry> getEntries() {
    return entries;
  }

  public void setEntries(Collection<HREntry> entries) {
    this.entries = entries;
  }

  @JsonIgnore
  public HRRaceKey getKey() {
    if (key == null) {
      key = new HRRaceKey(courseId, raceNumber);
    }
    return key;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("HRRace{");
    sb.append("raceId='").append(raceId).append('\'');
    sb.append(", meetingDate='").append(meetingDate).append('\'');
    sb.append(", courseId=").append(courseId);
    sb.append(", raceNumber=").append(raceNumber);
    sb.append(", courseName='").append(courseName).append('\'');
    sb.append(", courseAbbrev='").append(courseAbbrev).append('\'');
    sb.append(", startTimeLocalScheduled='").append(startTimeLocalScheduled).append('\'');
    sb.append(", startTimeGMTScheduled='").append(startTimeGMTScheduled).append('\'');
    sb.append(", actualTimeLocalScheduled='").append(actualTimeLocalScheduled).append('\'');
    sb.append(", actualTimeGMTScheduled='").append(actualTimeGMTScheduled).append('\'');
    sb.append(", raceSurfaceChar='").append(raceSurfaceChar).append('\'');
    sb.append(", raceSurfaceName='").append(raceSurfaceName).append('\'');
    sb.append(", raceType='").append(raceType).append('\'');
    sb.append(", distanceFurlongs=").append(distanceFurlongs);
    sb.append(", distanceYards=").append(distanceYards);
    sb.append(", distance=").append(distance);
    sb.append(", distanceText='").append(distanceText).append('\'');
    sb.append(", raceTitle='").append(raceTitle).append('\'');
    sb.append(", raceTitleShort='").append(raceTitleShort).append('\'');
    sb.append(", going='").append(going).append('\'');
    sb.append(", goingAbbrev='").append(goingAbbrev).append('\'');
    sb.append(", goingOfficial='").append(goingOfficial).append('\'');
    sb.append(", eligibilityAgeMax='").append(eligibilityAgeMax).append('\'');
    sb.append(", eligibilityAgeMin='").append(eligibilityAgeMin).append('\'');
    sb.append(", numberOfRunners=").append(numberOfRunners);
    sb.append(", numberOfPlaces=").append(numberOfPlaces);
    sb.append(", eligibilitySexLimit='").append(eligibilitySexLimit).append('\'');
    sb.append(", resultsStatus='").append(resultsStatus).append('\'');
    sb.append(", raceTypeChar='").append(raceTypeChar).append('\'');
    sb.append(", raceCode='").append(raceCode).append('\'');
    sb.append(", prizeFund='").append(prizeFund).append('\'');
    sb.append(", prizeFundWinner='").append(prizeFundWinner).append('\'');
    sb.append(", analystVerdict='").append(analystVerdict).append('\'');
    sb.append(", drawComment='").append(drawComment).append('\'');
    sb.append(", ipHintsGeneral='").append(ipHintsGeneral).append('\'');
    sb.append(", ipHintsPriceRunStyle='").append(ipHintsPriceRunStyle).append('\'');
    sb.append(", iPriceHistory='").append(iPriceHistory).append('\'');
    sb.append(", ipHintsOverallPace='").append(ipHintsOverallPace).append('\'');
    sb.append(", ipHintsSpecificPace='").append(ipHintsSpecificPace).append('\'');
    sb.append(", raceStateId=").append(raceStateId);
    sb.append(", ratingLimitLower=").append(ratingLimitLower);
    sb.append(", ratingLimitUpper=").append(ratingLimitUpper);
    sb.append(", raceClass='").append(raceClass).append('\'');
    sb.append(", smartStat1='").append(smartStat1).append('\'');
    sb.append(", smartStat2='").append(smartStat2).append('\'');
    sb.append(", smartStat3='").append(smartStat3).append('\'');
    sb.append(", bfMarketId='").append(bfMarketId).append('\'');
    sb.append(", finishingTime='").append(finishingTime).append('\'');
    sb.append(", numberOfFencesJumped=").append(numberOfFencesJumped);
    sb.append(", publishFlag=").append(publishFlag);
    sb.append(", courseMapId=").append(courseMapId);
    sb.append(", entries=").append(entries);
    sb.append(", key=").append(key);
    sb.append('}');
    return sb.toString();
  }

  public static class HRRaceKey implements Serializable {

    private final int raceNumber;
    private final int courseId;

    public HRRaceKey(int courseId, int raceNumber) {
      this.courseId = courseId;
      this.raceNumber = raceNumber;
    }

    public int getRaceNumber() {
      return raceNumber;
    }

    public int getCourseId() {
      return courseId;
    }

    @Override
    public boolean equals(Object o) {
      if (this == o) return true;
      if (o == null || getClass() != o.getClass()) return false;
      HRRace.HRRaceKey that = (HRRace.HRRaceKey) o;
      return this.courseId == that.courseId && this.raceNumber == that.raceNumber;
    }

    @Override
    public int hashCode() {
      return Objects.hash(courseId, raceNumber);
    }

    @Override
    public String toString() {
      final StringBuilder sb = new StringBuilder("HRMeetingKey{");
      sb.append(", courseId=").append(courseId);
      sb.append(", raceNumber=").append(raceNumber);
      sb.append('}');
      return sb.toString();
    }
  }

  @Override
  public Set<Integer> getRaceObEventIds() {
    return getOpenBetIds();
  }

  @Override
  public Set<? extends TimeformEntry> getRaceEntries() {
    return new HashSet<HREntry>(getEntries());
  }
}
