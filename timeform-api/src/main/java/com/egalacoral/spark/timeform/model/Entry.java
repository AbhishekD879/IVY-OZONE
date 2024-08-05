package com.egalacoral.spark.timeform.model;

import com.google.gson.annotations.SerializedName;

import java.io.Serializable;
import java.util.Set;

/**
 * Created by Igor.Domshchikov on 8/3/2016.
 */
public class Entry extends Identity implements Serializable {

  private static final long serialVersionUID = 5265108759531632829L;

  @SerializedName(value = "entry_id")
  private Integer entryId;

  @SerializedName(value = "openbet_ids")
  private Set<Integer> obSelectionIds;

  @SerializedName(value = "pa_meeting_id")
  private Integer paMeetingId;

  @SerializedName(value = "race_id")
  private Integer raceId;

  @SerializedName(value = "greyhound_id")
  private Integer greyhoundId;

  @SerializedName(value = "pa_greyhound_id")
  private Integer paGreyHoundId;

  @SerializedName(value = "exp_final_time")
  private Double expFinalTime;

  @SerializedName(value = "exp_sec_time")
  private Double expSecTime;

  @SerializedName(value = "fair_odds_num")
  private Double fairOddsNum;

  @SerializedName(value = "fair_odds_den")
  private Double fairOddsDen;

  @SerializedName(value = "fair_odds_dec")
  private Double fairOddsDec;

  @SerializedName(value = "position_prediction")
  private Integer positionPrediction;

  @SerializedName(value = "star_rating")
  private Integer starRating;

  @SerializedName(value = "one_line_comment")
  private String oneLineComment;

  @SerializedName(value = "best_recent_time")
  private Double bestRecentTime;

  @SerializedName(value = "meeting_entry_nap")
  private Integer meetingEntryNap;

  @SerializedName(value = "greyhound_full_name")
  private String greyHoundFullName;

  @SerializedName(value = "trainer_full_name")
  private String trainerFullName;

  @SerializedName(value = "owner_full_name")
  private String ownerFullName;

  @SerializedName(value = "handicap_allowance_status")
  private String handicapAllowanceStatus;

  @SerializedName(value = "reserve")
  private Boolean reserve;

  @SerializedName(value = "status_name")
  private String statusName;

  private Integer trap;

  @SerializedName(value = "seed_name")
  private String seedName;

  public Entry() {}

  /**
   * Gets the value of the entryId property.
   * EntityColumn: entry_id | Standard
   * Summary: the unique identifier for the entry
   * Remark: the Primary Key for the entry (PK)
   *
   * @return an Integer value above 0
   */
  public Integer getEntryId() {
    return entryId;
  }

  /**
   * Gets the value of the obSelectionId property.
   * EntityColumn: openbet_id
   * Summary: the unique identifier for the selection
   * Remark:
   *
   * @return an Integer value above 0
   */
  public Set<Integer> getObSelectionIds() {
    return obSelectionIds;
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
   * Gets the value of the paGreyHoundId property.
   * EntityColumn: pa_greyhound_id | Standard
   * Summary: the PA unique identifier for the greyhound
   * Remark: the PA Primary Key for the greyhound (FK)
   *
   * @return an Integer value above 0
   */
  public Integer getPaGreyHoundId() {
    return paGreyHoundId;
  }

  /**
   * Gets the value of the expFinalTime property.
   * EntityColumn: exp_final_time | Standard
   * Summary: Timeform's expected run time for the greyhound in this race
   * Remark: a greyhound stat
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
   * Remark: a greyhound stat.
   * Time will be 0.00 in the event of a sectional time not being applicable
   *
   * @return a Double value above or equal to 0
   */
  public Double getExpSecTime() {
    return expSecTime;
  }

  /**
   * Gets the value of the fairOddsNum property.
   * EntityColumn: fair_odds_num | Standard
   * Summary: Timeform's fair odds forecast inclusive of stake
   * Remark: the numerator; get the denominator from fair_odds_den
   *
   * @return a Double value above 0
   */
  public Double getFairOddsNum() {
    return fairOddsNum;
  }

  /**
   * Gets the value of the fairOddsDen property.
   * EntityColumn: fair_odds_den | Standard
   * Summary: Timeform's fair odds forecast inclusive of stake
   * Remark: the denominator; get the numerator from fair_odds_num
   *
   * @return a Double value above 0
   */
  public Double getFairOddsDen() {
    return fairOddsDen;
  }

  /**
   * Gets the value of the fairOddsDec property.
   * EntityColumn: fair_odds_dec | Standard
   * Summary: Timeform's fair odds forecast inclusive of stake
   * Remark: the fair odds expressed as a decimal inclusive of stake
   *
   * @return a Double value above 0
   */
  public Double getFairOddsDec() {
    return fairOddsDec;
  }

  /**
   * Gets the value of the positionPrediction property.
   * EntityColumn: position_prediction | Standard
   * Summary: Timeform's 1-2-3 position prediction for this race
   * Remark: prediction will be 0 in the event of the greyhound not qualifying for the 1-2-3
   *
   * @return an Integer value between 0 and 3
   */
  public Integer getPositionPrediction() {
    return positionPrediction;
  }

  /**
   * Gets the value of the starRating property.
   * EntityColumn: star_rating | Standard
   * Summary: Timeform's star rating
   * Remark: an example: 3 indicates 3 out of 5 stars, etc
   *
   * @return an Integer value between 1 and 5
   */
  public Integer getStarRating() {
    return starRating;
  }

  /**
   * Gets the value of the oneLineComment property.
   * EntityColumn: one_line_comment | Standard
   * Summary: Timeform's comment summing up the prospect for each greyhound in this race
   * Remark: an example: Was running really well before its absence.
   * Capable of being involved in the finish
   *
   * @return a String with Sentence Case value
   */
  public String getOneLineComment() {
    return oneLineComment;
  }

  /**
   * Gets the value of the bestRecentTime property.
   * EntityColumn: best_recent_time | Standard
   * Summary: the best time the greyhound has recorded in the last 3 months or 15 runs; whichever is most recent
   * Remark: time is matched to this track and distance if not recorded here
   *
   * @return a Double value above 0
   */
  public Double getBestRecentTime() {
    return bestRecentTime;
  }

  /**
   * Gets the value of the meetingEntryNap property.
   * EntityColumn: meeting_entry_nap | Standard
   * Summary: Timeform's meeting NAP and next best
   * Remark: Timeform's betting tips for this meeting; 1 being the bet of the day and 2 the next best;
   * a value of 0 will be used where this entry didn't qualify for either of these
   *
   * @return an Integer value 0, 1 or 2
   */
  public Integer getMeetingEntryNap() {
    return meetingEntryNap;
  }

  /**
   * Gets the value of the greyHoundFullName property.
   * EntityColumn: greyhound_full_name | Standard (PA)
   * Summary: the full name of the greyhound
   * Remark: an example: Mileheight Alba
   *
   * @return a String with Title Case value
   */
  public String getGreyHoundFullName() {
    return greyHoundFullName;
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
   * Gets the value of the reserve property.
   * EntityColumn: reserve | Standard (PA)
   * Summary: indicates if this greyhound was a reserve replacing another greyhound in the race
   * Remark: if true then greyhound was a reserve
   *
   * @return Boolean true or false value
   */
  public Boolean getReserve() {
    return reserve;
  }

  /**
   * Gets the value of the statusName property.
   * EntityColumn: status_name | Standard (PA)
   * Summary: the current status of the entry
   * Remark: an example: Runner
   *
   * @return a String with Title Case value
   */
  public String getStatusName() {
    return statusName;
  }

  /**
   * Gets the value of the trap property.
   * EntityColumn: trap | Standard (PA)
   * Summary: the trap this greyhound is set to run from
   * Remark: an example: 2 indicates Trap 2, etc
   *
   * @return an Integer value between 1 and 8
   */
  public Integer getTrap() {
    return trap;
  }

  /**
   * Gets the value of the seedName property.
   * EntityColumn: seed_name | Standard (PA)
   * Summary: the greyhound's seed for this race
   * Remark: an example: Wide
   *
   * @return a String with Title Case value
   */
  public String getSeedName() {
    return seedName;
  }

  public void setEntryId(Integer entryId) {
    this.entryId = entryId;
  }

  public void setObSelectionIds(Set<Integer> obSelectionIds) {
    this.obSelectionIds = obSelectionIds;
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

  public void setPaGreyHoundId(Integer paGreyHoundId) {
    this.paGreyHoundId = paGreyHoundId;
  }

  public void setExpFinalTime(Double expFinalTime) {
    this.expFinalTime = expFinalTime;
  }

  public void setExpSecTime(Double expSecTime) {
    this.expSecTime = expSecTime;
  }

  public void setFairOddsNum(Double fairOddsNum) {
    this.fairOddsNum = fairOddsNum;
  }

  public void setFairOddsDen(Double fairOddsDen) {
    this.fairOddsDen = fairOddsDen;
  }

  public void setFairOddsDec(Double fairOddsDec) {
    this.fairOddsDec = fairOddsDec;
  }

  public void setPositionPrediction(Integer positionPrediction) {
    this.positionPrediction = positionPrediction;
  }

  public void setStarRating(Integer starRating) {
    this.starRating = starRating;
  }

  public void setOneLineComment(String oneLineComment) {
    this.oneLineComment = oneLineComment;
  }

  public void setBestRecentTime(Double bestRecentTime) {
    this.bestRecentTime = bestRecentTime;
  }

  public void setMeetingEntryNap(Integer meetingEntryNap) {
    this.meetingEntryNap = meetingEntryNap;
  }

  public void setGreyHoundFullName(String greyHoundFullName) {
    this.greyHoundFullName = greyHoundFullName;
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

  public void setReserve(Boolean reserve) {
    this.reserve = reserve;
  }

  public void setStatusName(String statusName) {
    this.statusName = statusName;
  }

  public void setTrap(Integer trap) {
    this.trap = trap;
  }

  public void setSeedName(String seedName) {
    this.seedName = seedName;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("Entry{");
    sb.append("entryId=").append(entryId);
    sb.append(", obSelectionIds=").append(obSelectionIds);
    sb.append(", paMeetingId=").append(paMeetingId);
    sb.append(", raceId=").append(raceId);
    sb.append(", greyhoundId=").append(greyhoundId);
    sb.append(", paGreyHoundId=").append(paGreyHoundId);
    sb.append(", expFinalTime=").append(expFinalTime);
    sb.append(", expSecTime=").append(expSecTime);
    sb.append(", fairOddsNum=").append(fairOddsNum);
    sb.append(", fairOddsDen=").append(fairOddsDen);
    sb.append(", fairOddsDec=").append(fairOddsDec);
    sb.append(", positionPrediction=").append(positionPrediction);
    sb.append(", starRating=").append(starRating);
    sb.append(", oneLineComment='").append(oneLineComment).append('\'');
    sb.append(", bestRecentTime=").append(bestRecentTime);
    sb.append(", meetingEntryNap=").append(meetingEntryNap);
    sb.append(", greyHoundFullName='").append(greyHoundFullName).append('\'');
    sb.append(", trainerFullName='").append(trainerFullName).append('\'');
    sb.append(", ownerFullName='").append(ownerFullName).append('\'');
    sb.append(", handicapAllowanceStatus='").append(handicapAllowanceStatus).append('\'');
    sb.append(", reserve=").append(reserve);
    sb.append(", statusName='").append(statusName).append('\'');
    sb.append(", trap=").append(trap);
    sb.append(", seedName='").append(seedName).append('\'');
    sb.append('}');
    return sb.toString();
  }
}