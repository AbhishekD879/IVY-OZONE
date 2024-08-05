package com.egalacoral.spark.timeform.model.horseracing;

import com.egalacoral.spark.timeform.model.Identity;
import com.google.gson.annotations.SerializedName;
import java.io.Serializable;

/** Created by llegkyy on 16.09.16. */
public class HRCourse extends Identity implements Serializable {
  private static final long serialVersionUID = 2978556705485362495L;

  @SerializedName(value = "courseId")
  private Integer courseId;

  @SerializedName(value = "countryCode")
  private String countryCode;

  @SerializedName(value = "countryName")
  private String countryName;

  @SerializedName(value = "surfaceName")
  private String surfaceName;

  @SerializedName(value = "gmtZoneId")
  private Integer gmtZoneId;

  @SerializedName(value = "courseName")
  private String courseName;

  @SerializedName(value = "courseName2Char")
  private String courseName2Char;

  @SerializedName(value = "courseName3Char")
  private String courseName3Char;

  @SerializedName(value = "courseTvChannel")
  private String courseTvChannel;

  @SerializedName(value = "addressID")
  private Integer addressId;

  @SerializedName(value = "courseStatusId")
  private Integer courseStatusId;

  @SerializedName(value = "courseStatus")
  private String courseStatus;

  @SerializedName(value = "flatCourseDescription")
  private String flatCourseDescription;

  @SerializedName(value = "jumpCourseDescription")
  private String jumpCourseDescription;

  @SerializedName(value = "awCourseDescription")
  private String awCourseDescription;

  /**
   * The unique identifier for the course
   *
   * @note The primary key for the course (PK)
   * @return Integer above 0
   */
  public Integer getCourseId() {
    return courseId;
  }

  /**
   * The foreign key of the country to which the course belongs
   *
   * @note An example: GBR - Great Britain
   * @return String(3) UPPER CASE
   */
  public String getCountryCode() {
    return countryCode;
  }

  /**
   * The full name of the country to which the course belongs
   *
   * @note An example: Great Britain
   * @return String Title case
   */
  public String getCountryName() {
    return countryName;
  }

  /**
   * The type of surface that is raced on at the course
   *
   * @note Values are All Weather, Turf or Both
   * @return String Title case
   */
  public String getSurfaceName() {
    return surfaceName;
  }

  /**
   * The GMT Zone the course belongs to
   *
   * @note Not currently in use
   * @return Integer above o
   */
  public Integer getGmtZoneId() {
    return gmtZoneId;
  }

  /**
   * The full name of the course
   *
   * @note An example: HAYDOCK PARK
   * @return String UPPER CASE
   */
  public String getCourseName() {
    return courseName;
  }

  /**
   * A two character representation of the course name
   *
   * @note An example: As - Ascot
   * @return String title case
   */
  public String getCourseName2Char() {
    return courseName2Char;
  }

  /**
   * A three character representation of the course name
   *
   * @note An example: Asc - Ascot
   * @return String Title case
   */
  public String getCourseName3Char() {
    return courseName3Char;
  }

  /**
   * The UK TV channel that has broadcast rights to the course
   *
   * @note An example: RUK - Racing UK
   * @return String Title case
   */
  public String getCourseTvChannel() {
    return courseTvChannel;
  }

  /**
   * The integer value of the address of the course
   *
   * @note Not currently in use
   * @return Integer above 0
   */
  public Integer getAddressId() {
    return addressId;
  }

  /**
   * The integer value of the status of the course
   *
   * @note Values are 35 - Active Course, 36 - Closed Course, 37 - Redundant Course
   * @return Integer above 0
   */
  public Integer getCourseStatusId() {
    return courseStatusId;
  }

  /**
   * The textual description of the course status
   *
   * @note An example: Active Course: The course is currently active
   * @return String Title case
   */
  public String getCourseStatus() {
    return courseStatus;
  }

  /**
   * The description of the course's flat characteristics
   *
   * @note An example: Left handed, galloping oval track. The round course is about 12 furlongs long
   *     with a run-in of 4 furlongs...
   * @return String Title case
   */
  public String getFlatCourseDescription() {
    return flatCourseDescription;
  }

  /**
   * The description of the course's jump characteristics
   *
   * @note An example: The Ayr course is a left-handed circuit of one and a half miles comprising
   *     nine fences, with well-graduated turns...
   * @return String Title case
   */
  public String getJumpCourseDescription() {
    return jumpCourseDescription;
  }

  /**
   * The description of the course's all weather characteristics
   *
   * @note An example: The Ayr course is a left-handed circuit of one and a half miles comprising
   *     nine fences, with well-graduated turns....
   * @return String Title case
   */
  public String getAwCourseDescription() {
    return awCourseDescription;
  }

  public void setCourseId(Integer courseId) {
    this.courseId = courseId;
  }

  public void setCountryCode(String countryCode) {
    this.countryCode = countryCode;
  }

  public void setCountryName(String countryName) {
    this.countryName = countryName;
  }

  public void setSurfaceName(String surfaceName) {
    this.surfaceName = surfaceName;
  }

  public void setGmtZoneId(Integer gmtZoneId) {
    this.gmtZoneId = gmtZoneId;
  }

  public void setCourseName(String courseName) {
    this.courseName = courseName;
  }

  public void setCourseName2Char(String courseName2Char) {
    this.courseName2Char = courseName2Char;
  }

  public void setCourseName3Char(String courseName3Char) {
    this.courseName3Char = courseName3Char;
  }

  public void setCourseTvChannel(String courseTvChannel) {
    this.courseTvChannel = courseTvChannel;
  }

  public void setAddressId(Integer addressId) {
    this.addressId = addressId;
  }

  public void setCourseStatusId(Integer courseStatusId) {
    this.courseStatusId = courseStatusId;
  }

  public void setCourseStatus(String courseStatus) {
    this.courseStatus = courseStatus;
  }

  public void setFlatCourseDescription(String flatCourseDescription) {
    this.flatCourseDescription = flatCourseDescription;
  }

  public void setJumpCourseDescription(String jumpCourseDescription) {
    this.jumpCourseDescription = jumpCourseDescription;
  }

  public void setAwCourseDescription(String awCourseDescription) {
    this.awCourseDescription = awCourseDescription;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("HRCourse{");
    sb.append("courseId=").append(courseId);
    sb.append(", countryCode='").append(countryCode).append('\'');
    sb.append(", countryName='").append(countryName).append('\'');
    sb.append(", surfaceName='").append(surfaceName).append('\'');
    sb.append(", gmtZoneId=").append(gmtZoneId);
    sb.append(", courseName='").append(courseName).append('\'');
    sb.append(", courseName2Char='").append(courseName2Char).append('\'');
    sb.append(", courseName3Char='").append(courseName3Char).append('\'');
    sb.append(", courseTvChannel='").append(courseTvChannel).append('\'');
    sb.append(", addressId=").append(addressId);
    sb.append(", courseStatusId=").append(courseStatusId);
    sb.append(", courseStatus='").append(courseStatus).append('\'');
    sb.append(", flatCourseDescription='").append(flatCourseDescription).append('\'');
    sb.append(", jumpCourseDescription='").append(jumpCourseDescription).append('\'');
    sb.append(", awCourseDescription='").append(awCourseDescription).append('\'');
    sb.append('}');
    return sb.toString();
  }
}
