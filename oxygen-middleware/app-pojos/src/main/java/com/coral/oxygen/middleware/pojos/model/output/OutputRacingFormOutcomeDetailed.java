package com.coral.oxygen.middleware.pojos.model.output;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import java.io.Serializable;

public class OutputRacingFormOutcomeDetailed extends OutputRacingFormOutcome
    implements Serializable {

  private String refRecordType;
  private String refRecordId;
  private String runnerId;
  private String age;
  private String daysSinceRun;
  private String owner;
  private String overview;
  private String sireOverview;
  private String breedingOverview;
  private String weight;
  private String officialRating;
  private String formProviderRating;
  private String runnerStatusCode;
  private String colour;

  @ChangeDetect
  public String getRefRecordType() {
    return refRecordType;
  }

  public void setRefRecordType(String refRecordType) {
    this.refRecordType = refRecordType;
  }

  @ChangeDetect
  public String getRefRecordId() {
    return refRecordId;
  }

  public void setRefRecordId(String refRecordId) {
    this.refRecordId = refRecordId;
  }

  @ChangeDetect
  public String getRunnerId() {
    return runnerId;
  }

  public void setRunnerId(String runnerId) {
    this.runnerId = runnerId;
  }

  @ChangeDetect
  public String getAge() {
    return age;
  }

  public void setAge(String age) {
    this.age = age;
  }

  @ChangeDetect
  public String getDaysSinceRun() {
    return daysSinceRun;
  }

  public void setDaysSinceRun(String daysSinceRun) {
    this.daysSinceRun = daysSinceRun;
  }

  @ChangeDetect
  public String getOwner() {
    return owner;
  }

  public void setOwner(String owner) {
    this.owner = owner;
  }

  @ChangeDetect
  public String getOverview() {
    return overview;
  }

  public void setOverview(String overview) {
    this.overview = overview;
  }

  @ChangeDetect
  public String getSireOverview() {
    return sireOverview;
  }

  public void setSireOverview(String sireOverview) {
    this.sireOverview = sireOverview;
  }

  @ChangeDetect
  public String getBreedingOverview() {
    return breedingOverview;
  }

  public void setBreedingOverview(String breedingOverview) {
    this.breedingOverview = breedingOverview;
  }

  @ChangeDetect
  public String getWeight() {
    return weight;
  }

  public void setWeight(String weight) {
    this.weight = weight;
  }

  @ChangeDetect
  public String getOfficialRating() {
    return officialRating;
  }

  public void setOfficialRating(String officialRating) {
    this.officialRating = officialRating;
  }

  @ChangeDetect
  public String getFormProviderRating() {
    return formProviderRating;
  }

  public void setFormProviderRating(String formProviderRating) {
    this.formProviderRating = formProviderRating;
  }

  @ChangeDetect
  public String getRunnerStatusCode() {
    return runnerStatusCode;
  }

  public void setRunnerStatusCode(String runnerStatusCode) {
    this.runnerStatusCode = runnerStatusCode;
  }

  @ChangeDetect
  public String getColour() {
    return colour;
  }

  public void setColour(String colour) {
    this.colour = colour;
  }
}
