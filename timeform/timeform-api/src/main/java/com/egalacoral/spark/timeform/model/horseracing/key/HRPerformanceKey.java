package com.egalacoral.spark.timeform.model.horseracing.key;

import com.egalacoral.spark.timeform.model.horseracing.HRPerformance;
import java.io.Serializable;

/** Created by llegkyy on 01.09.16. */
public class HRPerformanceKey implements Serializable {
  private String meetingDate;
  private Integer courseId;
  private Integer raceNumber;
  private String horseCode;

  public HRPerformanceKey() {}

  public HRPerformanceKey(
      String meetingDate, Integer courseId, Integer raceNumber, String horseCode) {
    this.meetingDate = meetingDate;
    this.courseId = courseId;
    this.raceNumber = raceNumber;
    this.horseCode = horseCode;
  }

  public HRPerformanceKey(HRPerformance hrPerformance) {
    this.meetingDate = hrPerformance.getMeetingDate();
    this.courseId = hrPerformance.getCourseId();
    this.raceNumber = hrPerformance.getRaceNumber();
    this.horseCode = hrPerformance.getHorseCode();
  }

  public String getMeetingDate() {
    return meetingDate;
  }

  public void setMeetingDate(String meetingDate) {
    this.meetingDate = meetingDate;
  }

  public Integer getCourseId() {
    return courseId;
  }

  public void setCourseId(Integer courseId) {
    this.courseId = courseId;
  }

  public Integer getRaceNumber() {
    return raceNumber;
  }

  public void setRaceNumber(Integer raceNumber) {
    this.raceNumber = raceNumber;
  }

  public String getHorseCode() {
    return horseCode;
  }

  public void setHorseCode(String horseCode) {
    this.horseCode = horseCode;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }

    HRPerformanceKey that = (HRPerformanceKey) o;

    if (meetingDate != null ? !meetingDate.equals(that.meetingDate) : that.meetingDate != null) {
      return false;
    }
    if (courseId != null ? !courseId.equals(that.courseId) : that.courseId != null) {
      return false;
    }
    if (raceNumber != null ? !raceNumber.equals(that.raceNumber) : that.raceNumber != null) {
      return false;
    }
    return horseCode != null ? horseCode.equals(that.horseCode) : that.horseCode == null;
  }

  @Override
  public int hashCode() {
    int result = meetingDate != null ? meetingDate.hashCode() : 0;
    result = 31 * result + (courseId != null ? courseId.hashCode() : 0);
    result = 31 * result + (raceNumber != null ? raceNumber.hashCode() : 0);
    result = 31 * result + (horseCode != null ? horseCode.hashCode() : 0);
    return result;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("HRPerformanceKey{");
    sb.append("meetingDate='").append(meetingDate).append('\'');
    sb.append(", courseId=").append(courseId);
    sb.append(", raceNumber=").append(raceNumber);
    sb.append(", horseCode='").append(horseCode).append('\'');
    sb.append('}');
    return sb.toString();
  }
}
