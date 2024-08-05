package com.egalacoral.spark.timeform.model.greyhound;

import com.egalacoral.spark.timeform.model.OBRelatedEntity;
import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.HashSet;
import java.util.Set;

public class Meeting extends OBRelatedEntity implements Serializable, TimeformMeeting {

  private static final long serialVersionUID = -5876319756871133484L;

  @SerializedName(value = "meeting_id")
  private Integer meetingId;

  private String name;

  @SerializedName(value = "pa_meeting_id")
  private Integer paMeetingId;

  @SerializedName(value = "track_id")
  private Integer trackId;

  @SerializedName(value = "track_short_name")
  private String trackShortName;

  @SerializedName(value = "meeting_number")
  private Integer meetingNumber;

  @SerializedName(value = "meeting_date")
  private String meetingDate;

  @SerializedName(value = "meeting_state_name")
  private String meetingStateName;

  @SerializedName(value = "meeting_type_name")
  private String meetingTypeName;

  @SerializedName(value = "meeting_race_type_name")
  private String meetingRaceTypeName;

  @SerializedName(value = "meeting_nap")
  private String meetingNap;

  private Set<Race> races = new HashSet<>();

  public Meeting() {
    // default constructor
  }

  /**
   * Gets the value of the meetingId property. EntityColumn: meeting_id | Standard Summary: the
   * unique identifier for the meeting Remarks:the Primary Key for the meeting (PK)
   *
   * @return an Integer with value above 0
   */
  public Integer getMeetingId() {
    return meetingId;
  }

  /**
   * Gets the value of the name property. EntityColumn: name Summary: mapped value from spreadsheet
   * Remarks: an example: Wimbledon
   *
   * @return a String with Title Case value
   */
  public String getName() {
    return name;
  }

  /**
   * Gets the value of the paMeetingId property. EntityColumn: pa_meeting_id | Standard Summary: the
   * PA unique identifier for the meeting Remarks: the PA Primary Key for the meeting (PK)
   *
   * @return an Integer with value above 0
   */
  public Integer getPaMeetingId() {
    return paMeetingId;
  }

  /**
   * Gets the value of the trackId property. EntityColumn: track_id | Standard Summary: the unique
   * identifier for the track Remarks: the Primary Key for the track (FK)
   *
   * @return an Integer with value above 0
   */
  public Integer getTrackId() {
    return trackId;
  }

  /**
   * Gets the value of the trackShortName property. EntityColumn: track_short_name | Standard (PA)
   * Summary: The short name of the track Remark: An example: Wimbledon
   *
   * @return a String with Title Case value
   */
  public String getTrackShortName() {
    return trackShortName;
  }

  /**
   * Gets the value of the meetingDate property. EntityColumn: meeting_date | Standard (PA) Summary:
   * The date the meeting is taking place Remark: Date will never be null
   *
   * @return String value
   */
  public String getMeetingDate() {
    return meetingDate;
  }

  /**
   * Gets the value of the meetingNumber property. EntityColumn: meeting_number | Standard Summary:
   * the meeting number Remarks: Meetings can be held at the same track on the same day (to
   * differentiate between meetings held in the morning, afternoon or evening)
   *
   * @return an Integer with value 1 or 2
   */
  public Integer getMeetingNumber() {
    return meetingNumber;
  }

  /**
   * Gets the value of the meetingStateName property. EntityColumn: meeting_state_name | Standard
   * (PA) Summary: the state the meeting is currently at Remarks: an example: Finished
   *
   * @return a String with Title Case value
   */
  public String getMeetingStateName() {
    return meetingStateName;
  }

  /**
   * Gets the value of the meetingTypeName property. EntityColumn: meeting_type_name | Standard (PA)
   * Summary: the type of racing at this meeting Remarks: Will be either Flat, Hurdles or Both
   *
   * @return a String with Title Case value
   */
  public String getMeetingTypeName() {
    return meetingTypeName;
  }

  /**
   * Gets the value of the meetingRaceTypeName property. EntityColumn: meeting_race_type_name |
   * Standard (PA) Summary: the type of meeting Remarks: Will be either Official Meeting or Trials
   * Meeting
   *
   * @return a String with Title Case value
   */
  public String getMeetingRaceTypeName() {
    return meetingRaceTypeName;
  }

  /**
   * Gets the value of the meetingNap property. EntityColumn: meeting_nap | Standard Summary:
   * Timeform's meeting NAP and next best Remarks: an example: NAP: Mountainview Gal. NB: Murlough
   * Bay. Will be empty in the event of trials, or if it hasn't yet been calculated
   *
   * @return a String with Title Case value
   */
  public String getMeetingNap() {
    return meetingNap;
  }

  /**
   * Gets the value of the races property. EntityColumn: race Summary: The representation of a race.
   * Remark: {@link Race }
   *
   * @return List of race entities
   */
  public Set<Race> getRaces() {
    return races;
  }

  public void setMeetingId(Integer meetingId) {
    this.meetingId = meetingId;
  }

  public void setName(String name) {
    this.name = name;
  }

  public void setPaMeetingId(Integer paMeetingId) {
    this.paMeetingId = paMeetingId;
  }

  public void setTrackId(Integer trackId) {
    this.trackId = trackId;
  }

  public void setTrackShortName(String trackShortName) {
    this.trackShortName = trackShortName;
  }

  public void setMeetingNumber(Integer meetingNumber) {
    this.meetingNumber = meetingNumber;
  }

  public void setMeetingDate(String meetingDate) {
    this.meetingDate = meetingDate;
  }

  public void setMeetingStateName(String meetingStateName) {
    this.meetingStateName = meetingStateName;
  }

  public void setMeetingTypeName(String meetingTypeName) {
    this.meetingTypeName = meetingTypeName;
  }

  public void setMeetingRaceTypeName(String meetingRaceTypeName) {
    this.meetingRaceTypeName = meetingRaceTypeName;
  }

  public void setMeetingNap(String meetingNap) {
    this.meetingNap = meetingNap;
  }

  public void setRaces(Set<Race> races) {
    this.races = races;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("Meeting{");
    sb.append("meetingId=").append(meetingId);
    sb.append(", name='").append(name).append('\'');
    sb.append(", paMeetingId=").append(paMeetingId);
    sb.append(", trackId=").append(trackId);
    sb.append(", meetingNumber=").append(meetingNumber);
    sb.append(", meetingDate=").append(meetingDate);
    sb.append(", meetingStateName='").append(meetingStateName).append('\'');
    sb.append(", meetingTypeName='").append(meetingTypeName).append('\'');
    sb.append(", meetingRaceTypeName='").append(meetingRaceTypeName).append('\'');
    sb.append(", meetingNap='").append(meetingNap).append('\'');
    sb.append(", races=").append(races);
    sb.append('}');
    return sb.toString();
  }

  @Override
  public Set<Integer> getMeetingObEventTypeId() {
    return getOpenBetIds();
  }

  @Override
  public Set<? extends TimeformRace> getMeetingRaces() {
    return getRaces();
  }
}
