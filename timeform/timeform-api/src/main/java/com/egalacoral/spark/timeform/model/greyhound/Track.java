package com.egalacoral.spark.timeform.model.greyhound;

import com.egalacoral.spark.timeform.model.Identity;
import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.List;

/** Created by Igor.Domshchikov on 8/4/2016. */
public class Track extends Identity implements Serializable {

  private static final long serialVersionUID = 812378847170851919L;

  @SerializedName(value = "track_id")
  private Integer trackId;

  @SerializedName(value = "track_full_name")
  private String trackFullName;

  @SerializedName(value = "track_short_name")
  private String trackShortName;

  @SerializedName(value = "country_full_name")
  private String countryFullName;

  private List<Meeting> meetings;

  public Track() {
    // default constructor
  }

  /**
   * Gets the value of the trackId property. EntityColumn: track_id | Standard Summary: the unique
   * identifier for the track Remarks: the Primary Key for the track (PK)
   *
   * @return an Integer with value above 0
   */
  public Integer getTrackId() {
    return trackId;
  }

  /**
   * Gets the value of the trackShortName property. EntityColumn: track_short_name | Standard (PA)
   * Summary: the short name of the track Remarks: an example: Wimbledon
   *
   * @return a String with Title Case value
   */
  public String getTrackShortName() {
    return trackShortName;
  }

  /**
   * Gets the value of the trackFullName property. EntityColumn: track_full_name | Standard (PA)
   * Summary: the full name of the track Remarks: an example: Wimbledon Stadium
   *
   * @return a String with Title Case value
   */
  public String getTrackFullName() {
    return trackFullName;
  }

  /**
   * Gets the value of the countryFullName property. EntityColumn: country_full_name | Standard
   * Summary: the full name of the country this track is situated in Remarks: an example: Great
   * Brtain
   *
   * @return a String with Title Case value
   */
  public String getCountryFullName() {
    return countryFullName;
  }

  /**
   * Gets the value of the meetings property. EntityColumn: meetings Summary: the representation of
   * a meeting. Remark: {@link Meeting }
   *
   * @return List of meeting entities
   */
  public List<Meeting> getMeetings() {
    return meetings;
  }

  public void setTrackId(Integer trackId) {
    this.trackId = trackId;
  }

  public void setTrackFullName(String trackFullName) {
    this.trackFullName = trackFullName;
  }

  public void setTrackShortName(String trackShortName) {
    this.trackShortName = trackShortName;
  }

  public void setCountryFullName(String countryFullName) {
    this.countryFullName = countryFullName;
  }

  public void setMeetings(List<Meeting> meetings) {
    this.meetings = meetings;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("Track{");
    sb.append("trackId=").append(trackId);
    sb.append(", trackFullName='").append(trackFullName).append('\'');
    sb.append(", trackShortName='").append(trackShortName).append('\'');
    sb.append(", countryFullName='").append(countryFullName).append('\'');
    sb.append(", meetings=").append(meetings);
    sb.append('}');
    return sb.toString();
  }
}
