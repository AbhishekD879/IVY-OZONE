package com.egalacoral.spark.timeform.model;

import com.google.gson.annotations.SerializedName;

import java.io.Serializable;
import java.util.Date;
import java.util.List;
import java.util.Set;

/**
 * Created by Igor.Domshchikov on 8/3/2016.
 */
public class Race extends Identity implements Serializable {

  private static final long serialVersionUID = 6614554186053709287L;

  @SerializedName(value = "race_id")
  private Integer raceId;

  @SerializedName(value = "OB_event_ids")
  private Set<Integer> obEventIds;

  @SerializedName(value = "track_id")
  private Integer trackId;

  @SerializedName(value = "meeting_id")
  private Integer meetingId;

  @SerializedName(value = "big_race")
  private Boolean bigRace;

  @SerializedName(value = "smart_stats")
  private String smartStats;

  private String verdict;

  @SerializedName(value = "track_profile")
  private String trackProfile;

  @SerializedName(value = "track_short_name")
  private String trackShortName;

  @SerializedName(value = "race_number")
  private Integer raceNumber;

  @SerializedName(value = "race_title")
  private String raceTitle;

  @SerializedName(value = "scheduled_race_time_local")
  private Date scheduledRaceTimeLocal;

  @SerializedName(value = "scheduled_race_time_gmt")
  private Date scheduledRaceTimeGmt;

  @SerializedName(value = "actual_race_time_local")
  private Date actualRaceTimeLocal;

  @SerializedName(value = "race_state_name")
  private String raceStateName;

  @SerializedName(value = "race_type_name")
  private String raceTypeName;

  @SerializedName(value = "race_grade_name")
  private String raceGradeName;

  @SerializedName(value = "handicap_race")
  private Boolean handicapRace;

  @SerializedName(value = "race_distance")
  private Integer raceDistance;

  @SerializedName(value = "prizes")
  private String prizes;

  @SerializedName(value = "official_going")
  private Double officialGoing;

  private List<Entry> entries;
  private List<Performance> performances;

  public Race() {}

  /**
   * Gets the value of the raceId property.
   * EntityColumn: race_id | Standard
   * Summary: the unique identifier for the race
   * Remarks: the Primary Key for the race (PK)
   *
   * @return an Integer with value above 0
   */
  public Integer getRaceId() {
    return raceId;
  }

  /**
   * Gets the value of the obEventIds property.
   * EntityColumn: OB_event_ids
   * Summary: the unique identifier for the event
   * Remark:
   *
   * @return an Integer value above 0
   */
  public Set<Integer> getObEventIds() {
    return obEventIds;
  }

  /**
   * Gets the value of the trackId property.
   * EntityColumn: track_id | Standard (PA)
   * Summary: the unique identifier for the track
   * Remarks: the Primary Key for the track (FK)
   *
   * @return an Integer with value above 0
   */
  public Integer getTrackId() {
    return trackId;
  }

  /**
   * Gets the value of the meetingId property.
   * EntityColumn: meeting_id | Standard (PA)
   * Summary: the unique identifier for the meeting
   * Remarks: the Primary Key for the meeting (FK)
   *
   * @return an Integer with value above 0
   */
  public Integer getMeetingId() {
    return meetingId;
  }

  /**
   * Gets the value of the bigRace property.
   * EntityColumn: big_race | Standard
   * Summary: Indicates if the race is classed as a 'big race'
   * Remarks: an example: Coronation Cup
   *
   * @return a Boolean with true or false value
   */
  public Boolean getBigRace() {
    return bigRace;
  }

  /**
   * Gets the value of the smartStats property.
   * EntityColumn: smart_stats | Standard
   * Summary: Some noteworthy stats generated for this specific race
   * Remarks: an example: B D O'sullivan has a 33.33% winning strike rate in the last 7 days
   *
   * @return a String with Sentence Case value
   */
  public String getSmartStats() {
    return smartStats;
  }

  /**
   * Gets the value of the verdict property.
   * EntityColumn: verdict | Standard
   * Summary: Timeform's verdict on this specific race
   * Remarks: an example: Severly Damaged has the best chance albeit not by much but can't
   * afford for much to go wrong. Knockmoy Jack can emerge second best
   *
   * @return a String with Sentence Case value
   */
  public String getVerdict() {
    return verdict;
  }

  /**
   * Gets the value of the trackProfile property.
   * EntityColumn: track_profile | Standard
   * Summary: Timeform's track profile written for this track and distance
   * Remarks: Profile will be an empty string if one isn't available
   *
   * @return a String with Sentence Case value
   */
  public String getTrackProfile() {
    return trackProfile;
  }

  /**
   * Gets the value of the trackShortName property.
   * EntityColumn: track_short_name | Standard
   * Summary: the short name of the track
   * Remarks: an example: Wimbledon
   *
   * @return a String with Sentence Case value
   */
  public String getTrackShortName() {
    return trackShortName;
  }

  /**
   * Gets the value of the raceNumber property.
   * EntityColumn: race_number | Standard (PA)
   * Summary: the race number at this meeting
   * Remarks: Assigned by race time ascending
   *
   * @return an Integer with value above 0
   */
  public Integer getRaceNumber() {
    return raceNumber;
  }

  /**
   * Gets the value of the raceTitle property.
   * EntityColumn: race_title | Standard (PA)
   * Summary: the title of the race
   * Remarks: Title will be an empty string in the event of us not knowing it
   *
   * @return a String with Title Case value
   */
  public String getRaceTitle() {
    return raceTitle;
  }

  /**
   * Gets the value of the scheduledRaceTimeLocal property.
   * EntityColumn: scheduled_race_time_local | Standard (PA)
   * Summary: the date and time the race is scheduled to start (local time)
   * Remarks: Date will be null in the event of us not knowing it yet
   *
   * @return a DataTime with any Date and Time
   */
  public Date getScheduledRaceTimeLocal() {
    return scheduledRaceTimeLocal;
  }

  /**
   * Gets the value of the scheduledRaceTimeGmt property.
   * EntityColumn: scheduled_race_time_gmt | Standard (PA)
   * Summary: the date and time the race is scheduled to start (GMT time)
   * Remarks: Date will be null in the event of us not knowing it yet
   *
   * @return a DataTime with any Date and Time
   */
  public Date getScheduledRaceTimeGmt() {
    return scheduledRaceTimeGmt;
  }

  /**
   * Gets the value of the actualRaceTimeLocal property.
   * EntityColumn: actual_race_time_local | Standard (PA)
   * Summary: the date and time the race actually started
   * Remarks: Date will be null until after the race has started
   *
   * @return a DataTime with any Date and Time
   */
  public Date getActualRaceTimeLocal() {
    return actualRaceTimeLocal;
  }

  /**
   * Gets the value of the raceStateName property.
   * EntityColumn: race_state_name | Standard (PA)
   * Summary: the state the race is currently at
   * Remarks: an example: Final Result
   *
   * @return a String with Title Case value
   */
  public String getRaceStateName() {
    return raceStateName;
  }

  /**
   * Gets the value of the raceTypeName property.
   * EntityColumn: race_type_name | Standard (PA)
   * Summary: the type of this race
   * Remarks: Will be either Flat or Hurdles
   *
   * @return a String with Title Case value
   */
  public String getRaceTypeName() {
    return raceTypeName;
  }

  /**
   * Gets the value of the raceGradeName property.
   * EntityColumn: race_grade_name | Standard (PA)
   * Summary: the grade/class of this race
   * Remarks: an example: A1
   *
   * @return a String with Uppercase value
   */
  public String getRaceGradeName() {
    return raceGradeName;
  }

  /**
   * Gets the value of the handicapRace property.
   * EntityColumn: handicap_race | Standard (PA)
   * Summary: Indicates if the race is a handicap or not
   * Remarks: If true then the race is a handicap
   *
   * @return a Boolean with True or false value
   */
  public Boolean getHandicapRace() {
    return handicapRace;
  }

  /**
   * Gets the value of the raceDistance property.
   * EntityColumn: race_distance | Standard (PA)
   * Summary: the distance of the race
   * Remarks: Distance expressed in metres
   *
   * @return an Integer with value above 0
   */
  public Integer getRaceDistance() {
    return raceDistance;
  }

  /**
   * Gets the value of the prizes property.
   * EntityColumn: prizes | Standard (PA)
   * Summary: Details about the prizes of this race
   * Remarks: an example: 1st £107, 2nd £34, Others £31 Race Total £265
   *
   * @return a String with Title Case value
   */
  public String getPrizes() {
    return prizes;
  }

  /**
   * Gets the value of the officialGoing property.
   * EntityColumn: official_going | Standard (PA)
   * Summary: the official going given to this race
   * Remarks: Official going
   *
   * @return a Decimal with value above, equal to or below 0
   */
  public Double getOfficialGoing() {
    return officialGoing;
  }


  /**
   * Gets the value of the entries property.
   * EntityColumn: entry
   * Summary: The representation of a dog in a race.
   * Remark: {@link Entry }
   *
   * @return List of performance entities
   */
  public List<Entry> getEntries() {
    return entries;
  }

  /**
   * Gets the value of the performances property.
   * EntityColumn: performance
   * Summary: the representation of a performance.
   * Remark: {@link Performance }
   *
   * @return List of performance entities
   */
  public List<Performance> getPerformances() {
    return performances;
  }

  public void setRaceId(Integer raceId) {
    this.raceId = raceId;
  }

  public void setObEventId(Set<Integer> obEventIds) {
    this.obEventIds = obEventIds;
  }

  public void setTrackId(Integer trackId) {
    this.trackId = trackId;
  }

  public void setMeetingId(Integer meetingId) {
    this.meetingId = meetingId;
  }

  public void setBigRace(Boolean bigRace) {
    this.bigRace = bigRace;
  }

  public void setSmartStats(String smartStats) {
    this.smartStats = smartStats;
  }

  public void setVerdict(String verdict) {
    this.verdict = verdict;
  }

  public void setTrackProfile(String trackProfile) {
    this.trackProfile = trackProfile;
  }

  public void setTrackShortName(String trackShortName) {
    this.trackShortName = trackShortName;
  }

  public void setRaceNumber(Integer raceNumber) {
    this.raceNumber = raceNumber;
  }

  public void setRaceTitle(String raceTitle) {
    this.raceTitle = raceTitle;
  }

  public void setScheduledRaceTimeLocal(Date scheduledRaceTimeLocal) {
    this.scheduledRaceTimeLocal = scheduledRaceTimeLocal;
  }

  public void setScheduledRaceTimeGmt(Date scheduledRaceTimeGmt) {
    this.scheduledRaceTimeGmt = scheduledRaceTimeGmt;
  }

  public void setActualRaceTimeLocal(Date actualRaceTimeLocal) {
    this.actualRaceTimeLocal = actualRaceTimeLocal;
  }

  public void setRaceStateName(String raceStateName) {
    this.raceStateName = raceStateName;
  }

  public void setRaceTypeName(String raceTypeName) {
    this.raceTypeName = raceTypeName;
  }

  public void setRaceGradeName(String raceGradeName) {
    this.raceGradeName = raceGradeName;
  }

  public void setHandicapRace(Boolean handicapRace) {
    this.handicapRace = handicapRace;
  }

  public void setRaceDistance(Integer raceDistance) {
    this.raceDistance = raceDistance;
  }

  public void setPrizes(String prizes) {
    this.prizes = prizes;
  }

  public void setOfficialGoing(Double officialGoing) {
    this.officialGoing = officialGoing;
  }

  public void setEntries(List<Entry> entries) {
    this.entries = entries;
  }

  public void setPerformances(List<Performance> performances) {
    this.performances = performances;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("Race{");
    sb.append("raceId=").append(raceId);
    sb.append(", obEventIds=").append(obEventIds);
    sb.append(", trackId=").append(trackId);
    sb.append(", meetingId=").append(meetingId);
    sb.append(", bigRace=").append(bigRace);
    sb.append(", smartStats='").append(smartStats).append('\'');
    sb.append(", verdict='").append(verdict).append('\'');
    sb.append(", trackProfile='").append(trackProfile).append('\'');
    sb.append(", trackShortName='").append(trackShortName).append('\'');
    sb.append(", raceNumber=").append(raceNumber);
    sb.append(", raceTitle='").append(raceTitle).append('\'');
    sb.append(", scheduledRaceTimeLocal=").append(scheduledRaceTimeLocal);
    sb.append(", scheduledRaceTimeGmt=").append(scheduledRaceTimeGmt);
    sb.append(", actualRaceTimeLocal=").append(actualRaceTimeLocal);
    sb.append(", raceStateName='").append(raceStateName).append('\'');
    sb.append(", raceTypeName='").append(raceTypeName).append('\'');
    sb.append(", raceGradeName='").append(raceGradeName).append('\'');
    sb.append(", handicapRace=").append(handicapRace);
    sb.append(", raceDistance=").append(raceDistance);
    sb.append(", prizes='").append(prizes).append('\'');
    sb.append(", officialGoing=").append(officialGoing);
    sb.append(", entries=").append(entries);
    sb.append(", performances=").append(performances);
    sb.append('}');
    return sb.toString();
  }
}
