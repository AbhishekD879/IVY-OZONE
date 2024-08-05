package com.egalacoral.spark.timeform.model.horseracing;

import com.egalacoral.spark.timeform.model.OBRelatedEntity;
import com.egalacoral.spark.timeform.model.greyhound.TimeformMeeting;
import com.egalacoral.spark.timeform.model.greyhound.TimeformRace;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.*;

public class HRMeeting extends OBRelatedEntity implements Serializable, TimeformMeeting {

  @SerializedName(value = "meetingDate")
  private String meetingDate;

  @SerializedName(value = "courseId")
  private Integer courseId;

  @SerializedName(value = "meetingStatus")
  private String meetingStatus;

  @SerializedName(value = "inspectionTime")
  private String inspectionTime;

  @SerializedName(value = "meetingGoing")
  private String meetingGoing;

  @SerializedName(value = "courseName")
  private String courseName;

  @SerializedName(value = "meetingSurfaceName")
  private String meetingSurfaceName;

  @SerializedName(value = "meetingSurfaceChar")
  private String meetingSurfaceChar;

  @SerializedName(value = "meetingRaceType")
  private String meetingRaceType;

  @SerializedName(value = "meetingNumberSuffix")
  private String meetingNumberSuffix;

  @SerializedName(value = "meetingNumber")
  private Integer meetingNumber;

  @SerializedName(value = "publishFlag")
  private Integer publishFlag;

  @JsonIgnore private HRCourse course;

  @JsonIgnore private transient HRMeetingKey key;

  private Collection<HRRace> races;

  public HRMeeting() {
    // default constructor
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
   * The ID of the course of the meeting and is part of the primary key Value: Above 0
   *
   * @return Integer Remarks: Part of the primary key (PK)
   */
  public Integer getCourseId() {
    return courseId;
  }

  /**
   * The status of the meeting Value: "" If no status is availble, title case if it is
   *
   * @return String Remarks: "" - no status available, an example: Abandoned
   */
  public String getMeetingStatus() {
    return meetingStatus;
  }

  /**
   * The time that any inspection is due to take place Value: 1900-01-01 00:00:00.000 if no
   * inspection is to take place, valid date time if it is
   *
   * @return Date Time Remarks: 1900-01-01 00:00:00.000 - no inspection, an example 2015-06-01
   *     10:30:27.234
   */
  public String getInspectionTime() {
    return inspectionTime;
  }

  /**
   * The official going report for the meeting Value: "" if no report is availble, Title Case if it
   * is
   *
   * @return String Remarks: "" - no report,
   */
  public String getMeetingGoing() {
    return meetingGoing;
  }

  /**
   * The full name of the course that of the meeting Value: Upper case
   *
   * @return String Remarks: An example: HAYDOCK PARK
   */
  public String getCourseName() {
    return courseName;
  }

  /**
   * The type of surface that is raced on at the meeting Value: Title case
   *
   * @return String Remarks: Values are All Weather, Turf or Both
   */
  public String getMeetingSurfaceName() {
    return meetingSurfaceName;
  }

  /**
   * The one character representation of the type of surface that is raced on at the meeting Value:
   * One char
   *
   * @return String(1) Remarks: Values are A - All Weather, T - Turf, B - Both
   */
  public String getMeetingSurfaceChar() {
    return meetingSurfaceChar;
  }

  /**
   * The type of racing Value: Title Case
   *
   * @return Remarks: Values are Flat, Jump, Both
   */
  public String getMeetingRaceType() {
    return meetingRaceType;
  }

  /**
   * The suffix of the meeting number as per the racing calendar Value: "" if no suffix is
   * available, upper case if it is
   *
   * @return String Remarks: "" - no suffix, an example: B
   */
  public String getMeetingNumberSuffix() {
    return meetingNumberSuffix;
  }

  /**
   * The meeting number as per the racing calendar Value: 0 if no number is available, positive
   * integer if it is
   *
   * @return Integer Remarks: 0 - no meeting number, an example 255
   */
  public Integer getMeetingNumber() {
    return meetingNumber;
  }

  /**
   * Internal Publish Flag Value:
   *
   * @return Integer Remarks:
   */
  public Integer getPublishFlag() {
    return publishFlag;
  }

  public Collection<HRRace> getRaces() {
    if (races == null) {
      races = new ArrayList<>();
    }
    return races;
  }

  public HRCourse getCourse() {
    return course;
  }

  public void setMeetingDate(String meetingDate) {
    this.meetingDate = meetingDate;
  }

  public void setCourseId(Integer courseId) {
    this.courseId = courseId;
  }

  public void setMeetingStatus(String meetingStatus) {
    this.meetingStatus = meetingStatus;
  }

  public void setInspectionTime(String inspectionTime) {
    this.inspectionTime = inspectionTime;
  }

  public void setMeetingGoing(String meetingGoing) {
    this.meetingGoing = meetingGoing;
  }

  public void setCourseName(String courseName) {
    this.courseName = courseName;
  }

  public void setMeetingSurfaceName(String meetingSurfaceName) {
    this.meetingSurfaceName = meetingSurfaceName;
  }

  public void setMeetingSurfaceChar(String meetingSurfaceChar) {
    this.meetingSurfaceChar = meetingSurfaceChar;
  }

  public void setMeetingRaceType(String meetingRaceType) {
    this.meetingRaceType = meetingRaceType;
  }

  public void setMeetingNumberSuffix(String meetingNumberSuffix) {
    this.meetingNumberSuffix = meetingNumberSuffix;
  }

  public void setMeetingNumber(Integer meetingNumber) {
    this.meetingNumber = meetingNumber;
  }

  public void setPublishFlag(Integer publishFlag) {
    this.publishFlag = publishFlag;
  }

  public void setRaces(Collection<HRRace> races) {
    this.races = races;
  }

  public void setCourse(HRCourse course) {
    this.course = course;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("HRMeeting{");
    sb.append("meetingDate='").append(meetingDate).append('\'');
    sb.append(", courseId=").append(courseId);
    sb.append(", meetingStatus='").append(meetingStatus).append('\'');
    sb.append(", inspectionTime='").append(inspectionTime).append('\'');
    sb.append(", meetingGoing='").append(meetingGoing).append('\'');
    sb.append(", courseName='").append(courseName).append('\'');
    sb.append(", meetingSurfaceName='").append(meetingSurfaceName).append('\'');
    sb.append(", meetingSurfaceChar='").append(meetingSurfaceChar).append('\'');
    sb.append(", meetingRaceType='").append(meetingRaceType).append('\'');
    sb.append(", meetingNumberSuffix='").append(meetingNumberSuffix).append('\'');
    sb.append(", meetingNumber=").append(meetingNumber);
    sb.append(", publishFlag=").append(publishFlag);
    sb.append(", course=").append(course);
    sb.append(", key=").append(key);
    sb.append(", races=").append(races);
    sb.append('}');
    return sb.toString();
  }

  @JsonIgnore
  public HRMeetingKey getKey() {
    if (key == null) {
      key = new HRMeetingKey(meetingDate.trim(), courseId);
    }
    return key;
  }

  public static class HRMeetingKey implements Serializable {

    private String meetingDate;

    private int courseId;

    public HRMeetingKey() {}

    public HRMeetingKey(String meetingDate, int courseId) {
      this.meetingDate = meetingDate;
      this.courseId = courseId;
    }

    public String getMeetingDate() {
      return meetingDate;
    }

    public int getCourseId() {
      return courseId;
    }

    @Override
    public boolean equals(Object o) {
      if (this == o) return true;
      if (o == null || getClass() != o.getClass()) return false;
      HRMeetingKey that = (HRMeetingKey) o;
      return courseId == that.courseId && Objects.equals(meetingDate, that.meetingDate);
    }

    @Override
    public int hashCode() {
      return Objects.hash(meetingDate, courseId);
    }

    @Override
    public String toString() {
      final StringBuilder sb = new StringBuilder("HRMeetingKey{");
      sb.append("meetingDate='").append(meetingDate).append('\'');
      sb.append(", courseId=").append(courseId);
      sb.append('}');
      return sb.toString();
    }
  }

  @Override
  public Set<Integer> getMeetingObEventTypeId() {
    return getOpenBetIds();
  }

  @Override
  public Set<? extends TimeformRace> getMeetingRaces() {
    return new HashSet<HRRace>(getRaces());
  }
}
