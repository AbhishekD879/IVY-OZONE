package com.egalacoral.spark.timeform.model.horseracing;

import com.egalacoral.spark.timeform.model.Identity;
import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.List;

/** Created by llegkyy on 14.09.16. */
public class HRHorse extends Identity implements Serializable {
  private static final long serialVersionUID = 384563900216145938L;

  @SerializedName(value = "horseCode")
  private String horseCode;

  @SerializedName(value = "horseName")
  private String horseName;

  @SerializedName(value = "horseGender")
  private String horseGender;

  @SerializedName(value = "horseAge")
  private Integer horseAge;

  @SerializedName(value = "horseColour")
  private String horseColour;

  @SerializedName(value = "foalingDate")
  private String foalingDate;

  @SerializedName(value = "damPedigreeCode")
  private String damPedigreeCode;

  @SerializedName(value = "damName")
  private String damName;

  @SerializedName(value = "sirePedigreeCode")
  private String sirePedigreeCode;

  @SerializedName(value = "sireName")
  private String sireName;

  @SerializedName(value = "damSireName")
  private String damSireName;

  @SerializedName(value = "ownerCode")
  private String ownerCode;

  @SerializedName(value = "ownerFullName")
  private String ownerFullName;

  @SerializedName(value = "trainerCode")
  private String trainerCode;

  @SerializedName(value = "trainerFullName")
  private String trainerFullName;

  @SerializedName(value = "performanceCount")
  private Integer performanceCount;

  private List<HRPerformance> performances;

  /**
   * The code of the horse and is the primary key. The primary key (PK)
   *
   * @return String(12). Not null
   */
  public String getHorseCode() {
    return horseCode;
  }

  /**
   * The full name of the horse
   *
   * @return String. Upper Case. An example: KAUTO STAR (FR)
   */
  public String getHorseName() {
    return horseName;
  }

  /**
   * The gender of the horse
   *
   * @return String. Lower Case. Values are : f - filly, m - mare, c - colt, g - gelding, h - horse
   */
  public String getHorseGender() {
    return horseGender;
  }

  /**
   * This is the age of the horse based on 1st Jan birth date. 0 if no foaling date is available,
   * above 0 if it is
   *
   * @return Integer. 0 = no foaling date, an example: 4
   */
  public Integer getHorseAge() {
    return horseAge;
  }

  /**
   * This is the colour of the horse
   *
   * @return String(14) Values are : "" if colour isn't available, an example: gr - grey
   */
  public String getHorseColour() {
    return horseColour;
  }

  /**
   * This is the date the horse was born NULL if the date isn't available, date populated in
   * yyyy-mm-ddd if it is
   *
   * @return String. NULL - no date available, an example: 2012-03-12
   */
  public String getFoalingDate() {
    return foalingDate;
  }

  /**
   * The pedigree code of the dam "" if not available, 12 char string if it is
   *
   * @return String(12). "" if not available, an example: "000000000001"
   */
  public String getDamPedigreeCode() {
    return damPedigreeCode;
  }

  /**
   * The name of the dam "" if not available, Upper Case string if it is
   *
   * @return String. "" if not available, an example: "KIND (IRE)
   */
  public String getDamName() {
    return damName;
  }

  /**
   * The pedigree code of the sire "" if not available, 12 char string if it is
   *
   * @return String. "" if not available, an example: "000000000001"
   */
  public String getSirePedigreeCode() {
    return sirePedigreeCode;
  }

  /**
   * The name of the sire "" if not available, Upper Case string if it is
   *
   * @return String. "" if not available, an example: "KING'S THEATRE (IRE)
   */
  public String getSireName() {
    return sireName;
  }

  /**
   * The name of the dam sire "" if not available, Upper Case string if it is
   *
   * @return String. "" if not available, an example: "PORT ETTIENNE(FR)
   */
  public String getDamSireName() {
    return damSireName;
  }

  /**
   * The code of the owner of the horse Can be empty if an owner is not recorded against the horse
   *
   * @return String. "" if no owner is registered , an example: "000000000001" if one has
   */
  public String getOwnerCode() {
    return ownerCode;
  }

  /**
   * The full name of the owner of the horse Can be empty if an owner is not recorded against the
   * horse, Title Case if it is
   *
   * @return String. "" if no owner is registered for the horse, an example: Gigginstown House Stud
   */
  public String getOwnerFullName() {
    return ownerFullName;
  }

  /**
   * The code of the trainer of the horse Can be empty if a trainer is not recorded against the
   * horse
   *
   * @return String. "" if no trainer is registered , an example: "000000000001" if one has
   */
  public String getTrainerCode() {
    return trainerCode;
  }

  /**
   * The full name of the trainer of the horse Can be empty if a trainer is not recorded against the
   * horse, title case if it is
   *
   * @return String. "" if no trainer is registered for the horse, an example: Paul Nicholls
   */
  public String getTrainerFullName() {
    return trainerFullName;
  }

  /**
   * The number of performances available for the horse 0 if the horse hasn't run before, above 0 if
   * it has
   *
   * @return Integer. 0 - horse hasn't run before, an example: 7
   */
  public Integer getPerformanceCount() {
    return performanceCount;
  }

  public List<HRPerformance> getPerformances() {
    return performances;
  }

  public void setHorseCode(String horseCode) {
    this.horseCode = horseCode;
  }

  public void setHorseName(String horseName) {
    this.horseName = horseName;
  }

  public void setHorseGender(String horseGender) {
    this.horseGender = horseGender;
  }

  public void setHorseAge(Integer horseAge) {
    this.horseAge = horseAge;
  }

  public void setHorseColour(String horseColour) {
    this.horseColour = horseColour;
  }

  public void setFoalingDate(String foalingDate) {
    this.foalingDate = foalingDate;
  }

  public void setDamPedigreeCode(String damPedigreeCode) {
    this.damPedigreeCode = damPedigreeCode;
  }

  public void setDamName(String damName) {
    this.damName = damName;
  }

  public void setSirePedigreeCode(String sirePedigreeCode) {
    this.sirePedigreeCode = sirePedigreeCode;
  }

  public void setSireName(String sireName) {
    this.sireName = sireName;
  }

  public void setDamSireName(String damSireName) {
    this.damSireName = damSireName;
  }

  public void setOwnerCode(String ownerCode) {
    this.ownerCode = ownerCode;
  }

  public void setOwnerFullName(String ownerFullName) {
    this.ownerFullName = ownerFullName;
  }

  public void setTrainerCode(String trainerCode) {
    this.trainerCode = trainerCode;
  }

  public void setTrainerFullName(String trainerFullName) {
    this.trainerFullName = trainerFullName;
  }

  public void setPerformanceCount(Integer performanceCount) {
    this.performanceCount = performanceCount;
  }

  public void setPerformances(List<HRPerformance> performances) {
    this.performances = performances;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("HRHorse{");
    sb.append("horseCode='").append(horseCode).append('\'');
    sb.append(", horseName='").append(horseName).append('\'');
    sb.append(", horseGender='").append(horseGender).append('\'');
    sb.append(", horseAge=").append(horseAge);
    sb.append(", horseColour='").append(horseColour).append('\'');
    sb.append(", foalingDate='").append(foalingDate).append('\'');
    sb.append(", damPedigreeCode='").append(damPedigreeCode).append('\'');
    sb.append(", damName='").append(damName).append('\'');
    sb.append(", sirePedigreeCode='").append(sirePedigreeCode).append('\'');
    sb.append(", sireName='").append(sireName).append('\'');
    sb.append(", damSireName='").append(damSireName).append('\'');
    sb.append(", ownerCode='").append(ownerCode).append('\'');
    sb.append(", ownerFullName='").append(ownerFullName).append('\'');
    sb.append(", trainerCode='").append(trainerCode).append('\'');
    sb.append(", trainerFullName='").append(trainerFullName).append('\'');
    sb.append(", performanceCount=").append(performanceCount);
    sb.append(", performances=").append(performances);
    sb.append('}');
    return sb.toString();
  }
}
