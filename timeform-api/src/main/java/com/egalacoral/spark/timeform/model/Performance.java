package com.egalacoral.spark.timeform.model;

import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

/**
 * Created by Igor.Domshchikov on 8/4/2016.
 */
public class Performance extends Identity implements Serializable {

  private static final long serialVersionUID = 1723169002161078192L;

  @SerializedName(value = "performance_id")
  private Integer performanceId;

  @SerializedName(value = "pa_meeting_id")
  private Integer paMeetingId;

  @SerializedName(value = "race_id")
  private Integer raceId;

  @SerializedName(value = "greyhound_id")
  private Integer greyhoundId;

  @SerializedName(value = "pa_greyhound_id")
  private Integer paGreyhoundId;

  @SerializedName(value = "greyhound_full_name")
  private String greyhoundFullName;

  @SerializedName(value = "trainer_full_name")
  private String trainerFullName;

  @SerializedName(value = "owner_full_name")
  private String ownerFullName;

  @SerializedName(value = "handicap_allowance_status")
  private String handicapAllowanceStatus;

  @SerializedName(value = "distance_beaten_decimal")
  private Double distanceBeatenDecimal;

  @SerializedName(value = "distance_beaten_cumulative_decimal")
  private Double distanceBeatenCumulativeDecimal;

  @SerializedName(value = "eye_catcher")
  private Boolean eyeCatcher;

  @SerializedName(value = "weight_kilograms")
  private Double weightKilograms;

  @SerializedName(value = "position_status")
  private String positionStatus;

  private Integer trap;

  @SerializedName(value = "bend_positions")
  private String bendPositions;

  @SerializedName(value = "run_comment")
  private String runComment;

  @SerializedName(value = "run_time")
  private Double runTime;

  @SerializedName(value = "run_time_adjusted")
  private Double runTimeAdjusted;

  @SerializedName(value = "sectional_time")
  private Double sectionalTime;

  @SerializedName(value = "starting_price_num")
  private Double startingPriceNum;

  @SerializedName(value = "starting_price_den")
  private Double startingPriceDen;

  @SerializedName(value = "starting_price_dec")
  private Double startingPriceDec;

  @SerializedName(value = "tf_odds")
  private Double tfOdds;

  @SerializedName(value = "market_position")
  private Double marketPosition;

  @SerializedName(value = "trouble_in_running_allowance")
  private Double troubleInRunningAllowance;

  @SerializedName(value = "final_time_master_rating")
  private Integer finalTimeMasterRating;

  @SerializedName(value = "sectional_time_master_rating")
  private Integer sectionalTimeMasterRating;


  @SerializedName(value = "final_run_rating")
  private Integer finalRunRating;

  @SerializedName(value = "sectional_run_rating")
  private Integer sectionalRunRating;

  @SerializedName(value = "exp_final_time")
  private Double expFinalTime;

  @SerializedName(value = "exp_sec_time")
  private Double expSecTime;

  @SerializedName(value = "tf_final_time")
  private Double tfFinalTime;

  @SerializedName(value = "tf_sectional_time")
  private Double tfSectionalTime;

  @SerializedName(value = "proxy_rating")
  private Integer proxyRating;

  public Performance() {}

  /**
   * Gets the value of the performanceId property.
   * EntityColumn: performance_id | Standard
   * Summary: the unique identifier for this performance
   * Remark: the Primary Key for the race (PK)
   *
   * @return an Integer value above 0
   */
  public Integer getPerformanceId() {
    return performanceId;
  }

  /**
   * Gets the value of the paMeetingId property.
   * EntityColumn: pa_meeting_id | Standard
   * Summary: the PA unique identifier for the meeting
   * Remark: the PA Primary Key for the meeting (PK)
   *
   * @return an Integer value above 0
   */
  public Integer getPaMeetingId() {
    return paMeetingId;
  }

  /**
   * Gets the value of the raceId property.
   * EntityColumn: race_id | Standard
   * Summary: the unique identifier for this race
   * Remark: the Primary Key for the race (FK)
   *
   * @return an Integer value above 0
   */
  public Integer getRaceId() {
    return raceId;
  }

  /**
   * Gets the value of the greyhoundId property.
   * EntityColumn: greyhound_id | Standard
   * Summary: the unique identifier for the greyhound
   * Remark: the Primary Key for the greyhound (FK)
   *
   * @return an Integer value above 0
   */
  public Integer getGreyhoundId() {
    return greyhoundId;
  }

  /**
   * Gets the value of the paGreyhoundId property.
   * EntityColumn: pa_greyhound_id | Standard
   * Summary: the PA unique identifier for the greyhound
   * Remark: the PA Primary Key for the greyhound (FK)
   *
   * @return an Integer value above 0
   */
  public Integer getPaGreyhoundId() {
    return paGreyhoundId;
  }

  /**
   * Gets the value of the greyHoundFullName property.
   * EntityColumn: greyhound_full_name | Standard (PA)
   * Summary: the full name of the greyhound
   * Remark: an example: Mileheight Alba
   *
   * @return a String with Title Case value
   */
  public String getGreyhoundFullName() {
    return greyhoundFullName;
  }

  /**
   * Gets the value of the trainerFullName property.
   * EntityColumn: trainer_full_name | Standard (PA)
   * Summary: the full name of the greyhound's trainer (and the track they are attached to) for this race
   * Remark: an example: D Walsh (Hove). Trainer will be 'Unknown Trainer' in the event of us not knowing it.
   * Trainer will just be the name in the event of trainer or attached track information being unavailable
   *
   * @return a String with Title Case value
   */
  public String getTrainerFullName() {
    return trainerFullName;
  }

  /**
   * Gets the value of the ownerFullName property.
   * EntityColumn: owner_full_name | Standard (PA)
   * Summary: the full name of the greyhound's owner for this race
   * Remark: an example: Courtcraft Limited.
   * Owner will be 'Unknown Owner' in the event of that information being unavailable
   *
   * @return a String with Title Case value
   */
  public String getOwnerFullName() {
    return ownerFullName;
  }

  /**
   * Gets the value of the handicapAllowanceStatus property.
   * EntityColumn: handicap_allowance_status | Standard (PA)
   * Summary: the handicap start for the greyhound in this race
   * Remark: allowance will be blank in the event of a non-handicap race
   *
   * @return a String with Title Case value
   */
  public String getHandicapAllowanceStatus() {
    return handicapAllowanceStatus;
  }

  /**
   * Gets the value of the distanceBeatenDecimal property.
   * EntityColumn: distance_beaten_decimal | Standard (PA)
   * Summary: the distance the greyhound finished behind the one in front of it
   * Remark: Distance will be 0.00 in the event of first place
   *
   * @return a Double value above or equal to 0
   */
  public Double getDistanceBeatenDecimal() {
    return distanceBeatenDecimal;
  }

  /**
   * Gets the value of the distanceBeatenCumulativeDecimal property.
   * EntityColumn: distance_beaten_cumulative_decimal | Standard (PA)
   * Summary: the distance the greyhound finished behind the winner
   * Remark: Distance will be 0.00 in the event of first place
   *
   * @return a Double value above or equal to 0
   */
  public Double getDistanceBeatenCumulativeDecimal() {
    return distanceBeatenCumulativeDecimal;
  }

  /**
   * Gets the value of the eyeCatcher property.
   * EntityColumn: eye_catcher | Premium
   * Summary: Indicates that this greyhound's last run was an eye-catching one
   * Remark: False if the greyhound didn't obviously catch the eye
   *
   * @return Boolean true or false value
   */
  public Boolean getEyeCatcher() {
    return eyeCatcher;
  }

  /**
   * Gets the value of the weightKilograms property.
   * EntityColumn: weight_kilograms | Standard (PA)
   * Summary: the weight of the greyhound
   * Remark: Weight measured in kilograms
   *
   * @return a Double value above 0
   */
  public Double getWeightKilograms() {
    return weightKilograms;
  }

  /**
   * Gets the value of the positionStatus property.
   * EntityColumn: position_status | Standard (PA)
   * Summary: the position of the greyhound in this race
   * Remark: If the greyhound didn't finish the race then it will show 'DN'
   *
   * @return a String value between 1 and 8 (or DN)
   */
  public String getPositionStatus() {
    return positionStatus;
  }

  /**
   * Gets the value of the trap property.
   * EntityColumn: trap | Standard (PA)
   * Summary: the trap this greyhound is ran from
   * Remark: an example: 3 indicates Trap 3, etc
   *
   * @return an Integer value between 1 and 8
   */
  public Integer getTrap() {
    return trap;
  }

  /**
   * Gets the value of the bendPositions property.
   * EntityColumn: bend_positions | Standard (PA)
   * Summary: the position of the greyhound at the bends, where applicable
   * Remark: an example: 1116. A '-' indicates nothing was recorded
   *
   * @return a String of Positions
   */
  public String getBendPositions() {
    return bendPositions;
  }

  /**
   * Gets the value of the runComment property.
   * EntityColumn: run_comment | Standard (PA)
   * Summary: the official run comment of the greyhound in this race
   * Remark: an example: StumbledStart,Rls
   *
   * @return a String with Sentence Case value
   */
  public String getRunComment() {
    return runComment;
  }

  /**
   * Gets the value of the runTime property.
   * EntityColumn: run_time | Standard (PA)
   * Summary: the official run time of the greyhound in this race
   * Remark: Time will be 0.00 in the event of a non-finish
   *
   * @return a Double value above or equal to 0
   */
  public Double getRunTime() {
    return runTime;
  }

  /**
   * Gets the value of the runTimeAdjusted property.
   * EntityColumn: run_time_adjusted | Premium Plus
   * Summary: the official run time,
   * adjusted for a Timeform-calculated going allowance and trouble-in-running,
   * of the greyhound in this race
   * Remark: Time will be 0.00 in the event of a non-finish
   *
   * @return a Double value above or equal to 0
   */
  public Double getRunTimeAdjusted() {
    return runTimeAdjusted;
  }

  /**
   * Gets the value of the sectionalTime property.
   * EntityColumn: sectional_time | Standard (PA)
   * Summary: the official sectional time of the greyhound in this race
   * Remark: Time will be 0.00 in the event of a time not being applicable, e.g. handicap races or sprints
   *
   * @return a Double value above or equal to 0
   */
  public Double getSectionalTime() {
    return sectionalTime;
  }

  /**
   * Gets the value of the startingPriceNum property.
   * EntityColumn: starting_price_num | Standard (PA)
   * Summary: the official starting price of the greyhound in this race
   * Remark: the numerator; get the denominator from starting_price_den
   *
   * @return a Double value above 0
   */
  public Double getStartingPriceNum() {
    return startingPriceNum;
  }

  /**
   * Gets the value of the startingPriceDen property.
   * EntityColumn: starting_price_den | Standard (PA)
   * Summary: the official starting price of the greyhound in this race (denominator)
   * Remark: the denominator; get the numerator from starting_price_num
   *
   * @return a Double value above 0
   */
  public Double getStartingPriceDen() {
    return startingPriceDen;
  }

  /**
   * Gets the value of the startingPriceDec property.
   * EntityColumn: starting_price_dec | Standard (PA)
   * Summary: the official starting price of the greyhound in this race
   * Remark: the official starting price expressed as a decimal
   *
   * @return a Double value above 0
   */
  public Double getStartingPriceDec() {
    return startingPriceDec;
  }

  /**
   * Gets the value of the tfOdds property.
   * EntityColumn: tf_odds | Standard
   * Summary: the official starting price converted to a 100% book
   * Remark: Odds expressed as a decimal
   *
   * @return a Double value above 0
   */
  public Double getTfOdds() {
    return tfOdds;
  }

  /**
   * Gets the value of the marketPosition property.
   * EntityColumn: market_position | Standard (PA)
   * Summary: the position of the greyhound in the market
   * Remark: an example: 1 is the favourite (or joint favourite)
   *
   * @return a Double value between 1 and 8
   */
  public Double getMarketPosition() {
    return marketPosition;
  }

  /**
   * Gets the value of the troubleInRunningAllowance property.
   * EntityColumn: trouble_in_running_allowance | Premium Plus
   * Summary: Timeform's trouble-in-running allowance given to this greyhound's run
   * Remark: the allowance deducted from the greyhound's run time if it experienced trouble in running
   *
   * @return a Double value above or equal to 0
   */
  public Double getTroubleInRunningAllowance() {
    return troubleInRunningAllowance;
  }

  /**
   * Gets the value of the finalTimeMasterRating property.
   * EntityColumn: final_time_master_rating | Premium Plus
   * Summary: Timeform's 'master rating' based on both the greyhound's recent and overall form
   * Remark: A greyhound stat
   *
   * @return an Integer value above 0
   */
  public Integer getFinalTimeMasterRating() {
    return finalTimeMasterRating;
  }

  /**
   * Gets the value of the sectionalTimeMasterRating property.
   * EntityColumn: sectional_time_master_rating | Premium Plus
   * Summary: Timeform's 'master rating' based on the greyhound's recent sectional times
   * Remark: A greyhound stat
   *
   * @return an Integer value above 0
   */
  public Integer getSectionalTimeMasterRating() {
    return sectionalTimeMasterRating;
  }

  /**
   * Gets the value of the finalRunRating property.
   * EntityColumn: final_run_rating | Premium Plus
   * Summary: Timeform's rating based on the greyhound's overall performance in this race
   * Remark: A greyhound stat. Rating will be 0 in the event of a non-finish
   *
   * @return an Integer value above 0
   */
  public Integer getFinalRunRating() {
    return finalRunRating;
  }

  /**
   * Gets the value of the sectionalRunRating property.
   * EntityColumn: sectional_run_rating | Premium Plus
   * Summary: Timeform's rating based on the greyhound's sectional performance in this race
   * Remark: A greyhound stat. Rating will be 0 in the event of a non-finish
   *
   * @return an Integer value above 0
   */
  public Integer getSectionalRunRating() {
    return sectionalRunRating;
  }

  /**
   * Gets the value of the expFinalTime property.
   * EntityColumn: exp_final_time | Standard
   * Summary: Timeform's expected run time for the greyhound in this race
   * Remark: A greyhound stat.
   *
   * @return a Double value above 0
   */
  public Double getExpFinalTime() {
    return expFinalTime;
  }

  /**
   * Gets the value of the expSecTime property.
   * EntityColumn: exp_sec_time | Standard
   * Summary: Timeform's expected sectional time for the greyhound in this race
   * Remark: A greyhound stat. Time will be 0.00 in the event of a sectional time not being applicable
   *
   * @return a Double value above or equal to 0
   */
  public Double getExpSecTime() {
    return expSecTime;
  }

  /**
   * Gets the value of the tfFinalTime property.
   * EntityColumn: tf_final_time | Premium
   * Summary: Timeform's adjusted run time for the greyhound in this race
   * Remark: A greyhound stat.
   *
   * @return a Double value above 0
   */
  public Double getTfFinalTime() {
    return tfFinalTime;
  }

  /**
   * Gets the value of the tfSectionalTime property.
   * EntityColumn: tf_sectional_time | Premium
   * Summary: Timeform's adjusted sectional time for the greyhound in this race
   * Remark: A greyhound stat.
   * Time will be 0.00 in the event of a sectional time not being applicable
   *
   * @return a Double value above or equal to 0
   */
  public Double getTfSectionalTime() {
    return tfSectionalTime;
  }

  /**
   * Gets the value of the proxyRating property.
   * EntityColumn: proxy_rating | Premium Plus
   * Summary: Timeform's proxy mark for the greyhound in this race
   * Remark: an assessment of the overall strength of the race;
   * effectively the 'handicap mark' the greyhound was running off in the race
   *
   * @return an Integer value above 0
   */
  public Integer getProxyRating() {
    return proxyRating;
  }

  public void setPerformanceId(Integer performanceId) {
    this.performanceId = performanceId;
  }

  public void setPaMeetingId(Integer paMeetingId) {
    this.paMeetingId = paMeetingId;
  }

  public void setRaceId(Integer raceId) {
    this.raceId = raceId;
  }

  public void setGreyhoundId(Integer greyhoundId) {
    this.greyhoundId = greyhoundId;
  }

  public void setPaGreyhoundId(Integer paGreyhoundId) {
    this.paGreyhoundId = paGreyhoundId;
  }

  public void setGreyhoundFullName(String greyhoundFullName) {
    this.greyhoundFullName = greyhoundFullName;
  }

  public void setTrainerFullName(String trainerFullName) {
    this.trainerFullName = trainerFullName;
  }

  public void setOwnerFullName(String ownerFullName) {
    this.ownerFullName = ownerFullName;
  }

  public void setHandicapAllowanceStatus(String handicapAllowanceStatus) {
    this.handicapAllowanceStatus = handicapAllowanceStatus;
  }

  public void setDistanceBeatenDecimal(Double distanceBeatenDecimal) {
    this.distanceBeatenDecimal = distanceBeatenDecimal;
  }

  public void setDistanceBeatenCumulativeDecimal(Double distanceBeatenCumulativeDecimal) {
    this.distanceBeatenCumulativeDecimal = distanceBeatenCumulativeDecimal;
  }

  public void setEyeCatcher(Boolean eyeCatcher) {
    this.eyeCatcher = eyeCatcher;
  }

  public void setWeightKilograms(Double weightKilograms) {
    this.weightKilograms = weightKilograms;
  }

  public void setPositionStatus(String positionStatus) {
    this.positionStatus = positionStatus;
  }

  public void setTrap(Integer trap) {
    this.trap = trap;
  }

  public void setBendPositions(String bendPositions) {
    this.bendPositions = bendPositions;
  }

  public void setRunComment(String runComment) {
    this.runComment = runComment;
  }

  public void setRunTime(Double runTime) {
    this.runTime = runTime;
  }

  public void setRunTimeAdjusted(Double runTimeAdjusted) {
    this.runTimeAdjusted = runTimeAdjusted;
  }

  public void setSectionalTime(Double sectionalTime) {
    this.sectionalTime = sectionalTime;
  }

  public void setStartingPriceNum(Double startingPriceNum) {
    this.startingPriceNum = startingPriceNum;
  }

  public void setStartingPriceDen(Double startingPriceDen) {
    this.startingPriceDen = startingPriceDen;
  }

  public void setStartingPriceDec(Double startingPriceDec) {
    this.startingPriceDec = startingPriceDec;
  }

  public void setTfOdds(Double tfOdds) {
    this.tfOdds = tfOdds;
  }

  public void setMarketPosition(Double marketPosition) {
    this.marketPosition = marketPosition;
  }

  public void setTroubleInRunningAllowance(Double troubleInRunningAllowance) {
    this.troubleInRunningAllowance = troubleInRunningAllowance;
  }

  public void setFinalTimeMasterRating(Integer finalTimeMasterRating) {
    this.finalTimeMasterRating = finalTimeMasterRating;
  }

  public void setSectionalTimeMasterRating(Integer sectionalTimeMasterRating) {
    this.sectionalTimeMasterRating = sectionalTimeMasterRating;
  }

  public void setFinalRunRating(Integer finalRunRating) {
    this.finalRunRating = finalRunRating;
  }

  public void setSectionalRunRating(Integer sectionalRunRating) {
    this.sectionalRunRating = sectionalRunRating;
  }

  public void setExpFinalTime(Double expFinalTime) {
    this.expFinalTime = expFinalTime;
  }

  public void setExpSecTime(Double expSecTime) {
    this.expSecTime = expSecTime;
  }

  public void setTfFinalTime(Double tfFinalTime) {
    this.tfFinalTime = tfFinalTime;
  }

  public void setTfSectionalTime(Double tfSectionalTime) {
    this.tfSectionalTime = tfSectionalTime;
  }

  public void setProxyRating(Integer proxyRating) {
    this.proxyRating = proxyRating;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("Performance{");
    sb.append("performanceId=").append(performanceId);
    sb.append(", paMeetingId=").append(paMeetingId);
    sb.append(", raceId=").append(raceId);
    sb.append(", greyhoundId=").append(greyhoundId);
    sb.append(", paGreyhoundId=").append(paGreyhoundId);
    sb.append(", greyhoundFullName='").append(greyhoundFullName).append('\'');
    sb.append(", trainerFullName='").append(trainerFullName).append('\'');
    sb.append(", ownerFullName='").append(ownerFullName).append('\'');
    sb.append(", handicapAllowanceStatus='").append(handicapAllowanceStatus).append('\'');
    sb.append(", distanceBeatenDecimal=").append(distanceBeatenDecimal);
    sb.append(", distanceBeatenCumulativeDecimal=").append(distanceBeatenCumulativeDecimal);
    sb.append(", eyeCatcher=").append(eyeCatcher);
    sb.append(", weightKilograms=").append(weightKilograms);
    sb.append(", positionStatus='").append(positionStatus).append('\'');
    sb.append(", trap=").append(trap);
    sb.append(", bendPositions='").append(bendPositions).append('\'');
    sb.append(", runComment='").append(runComment).append('\'');
    sb.append(", runTime=").append(runTime);
    sb.append(", runTimeAdjusted=").append(runTimeAdjusted);
    sb.append(", sectionalTime=").append(sectionalTime);
    sb.append(", startingPriceNum=").append(startingPriceNum);
    sb.append(", startingPriceDen=").append(startingPriceDen);
    sb.append(", startingPriceDec=").append(startingPriceDec);
    sb.append(", tfOdds=").append(tfOdds);
    sb.append(", marketPosition=").append(marketPosition);
    sb.append(", troubleInRunningAllowance=").append(troubleInRunningAllowance);
    sb.append(", finalTimeMasterRating=").append(finalTimeMasterRating);
    sb.append(", sectionalTimeMasterRating=").append(sectionalTimeMasterRating);
    sb.append(", finalRunRating=").append(finalRunRating);
    sb.append(", sectionalRunRating=").append(sectionalRunRating);
    sb.append(", expFinalTime=").append(expFinalTime);
    sb.append(", expSecTime=").append(expSecTime);
    sb.append(", tfFinalTime=").append(tfFinalTime);
    sb.append(", tfSectionalTime=").append(tfSectionalTime);
    sb.append(", proxyRating=").append(proxyRating);
    sb.append('}');
    return sb.toString();
  }
}
