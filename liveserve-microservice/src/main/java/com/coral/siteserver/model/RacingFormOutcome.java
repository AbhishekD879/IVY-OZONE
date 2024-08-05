package com.coral.siteserver.model;

public class RacingFormOutcome {

  private String id;
  private String refRecordType;
  private String refRecordId;
  private String runnerNumber;
  private String runnerId;
  private String age;
  private String trainer;
  private String daysSinceRun;
  private String draw;
  private String jockey;
  private String owner;
  private String silkName;
  private String formGuide;
  private String overview;
  private String sireOverview;
  private String breedingOverview;
  private String weight;
  private String officialRating;
  private String formProviderRating;
  private String runnerStatusCode;
  private String colour;
  private String genderCode;

  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  public String getRefRecordType() {
    return refRecordType;
  }

  public void setRefRecordType(String refRecordType) {
    this.refRecordType = refRecordType;
  }

  public String getRefRecordId() {
    return refRecordId;
  }

  public void setRefRecordId(String refRecordId) {
    this.refRecordId = refRecordId;
  }

  public String getRunnerNumber() {
    return runnerNumber;
  }

  public void setRunnerNumber(String runnerNumber) {
    this.runnerNumber = runnerNumber;
  }

  public String getRunnerId() {
    return runnerId;
  }

  public void setRunnerId(String runnerId) {
    this.runnerId = runnerId;
  }

  public String getAge() {
    return age;
  }

  public void setAge(String age) {
    this.age = age;
  }

  public String getTrainer() {
    return trainer;
  }

  public void setTrainer(String trainer) {
    this.trainer = trainer;
  }

  public String getDaysSinceRun() {
    return daysSinceRun;
  }

  public void setDaysSinceRun(String daysSinceRun) {
    this.daysSinceRun = daysSinceRun;
  }

  public String getDraw() {
    return draw;
  }

  public void setDraw(String draw) {
    this.draw = draw;
  }

  public String getJockey() {
    return jockey;
  }

  public void setJockey(String jockey) {
    this.jockey = jockey;
  }

  public String getOwner() {
    return owner;
  }

  public void setOwner(String owner) {
    this.owner = owner;
  }

  public String getSilkName() {
    return silkName;
  }

  public void setSilkName(String silkName) {
    this.silkName = silkName;
  }

  public String getFormGuide() {
    return formGuide;
  }

  public void setFormGuide(String formGuide) {
    this.formGuide = formGuide;
  }

  public String getOverview() {
    return overview;
  }

  public void setOverview(String overview) {
    this.overview = overview;
  }

  public String getSireOverview() {
    return sireOverview;
  }

  public void setSireOverview(String sireOverview) {
    this.sireOverview = sireOverview;
  }

  public String getBreedingOverview() {
    return breedingOverview;
  }

  public void setBreedingOverview(String breedingOverview) {
    this.breedingOverview = breedingOverview;
  }

  public String getWeight() {
    return weight;
  }

  public void setWeight(String weight) {
    this.weight = weight;
  }

  public String getOfficialRating() {
    return officialRating;
  }

  public void setOfficialRating(String officialRating) {
    this.officialRating = officialRating;
  }

  public String getFormProviderRating() {
    return formProviderRating;
  }

  public void setFormProviderRating(String formProviderRating) {
    this.formProviderRating = formProviderRating;
  }

  public String getRunnerStatusCode() {
    return runnerStatusCode;
  }

  public void setRunnerStatusCode(String runnerStatusCode) {
    this.runnerStatusCode = runnerStatusCode;
  }

  public String getColour() {
    return colour;
  }

  public void setColour(String colour) {
    this.colour = colour;
  }

  public String getGenderCode() {
    return genderCode;
  }

  public void setGenderCode(String genderCode) {
    this.genderCode = genderCode;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("RacingFormOutcome{");
    sb.append("id='").append(id).append('\'');
    sb.append(", refRecordType='").append(refRecordType).append('\'');
    sb.append(", refRecordId='").append(refRecordId).append('\'');
    sb.append(", runnerNumber='").append(runnerNumber).append('\'');
    sb.append(", runnerId='").append(runnerId).append('\'');
    sb.append(", age='").append(age).append('\'');
    sb.append(", trainer='").append(trainer).append('\'');
    sb.append(", daysSinceRun='").append(daysSinceRun).append('\'');
    sb.append(", draw='").append(draw).append('\'');
    sb.append(", jockey='").append(jockey).append('\'');
    sb.append(", owner='").append(owner).append('\'');
    sb.append(", silkName='").append(silkName).append('\'');
    sb.append(", formGuide='").append(formGuide).append('\'');
    sb.append(", overview='").append(overview).append('\'');
    sb.append(", sireOverview='").append(sireOverview).append('\'');
    sb.append(", breedingOverview='").append(breedingOverview).append('\'');
    sb.append(", weight='").append(weight).append('\'');
    sb.append(", officialRating='").append(officialRating).append('\'');
    sb.append(", formProviderRating='").append(formProviderRating).append('\'');
    sb.append(", runnerStatusCode='").append(runnerStatusCode).append('\'');
    sb.append(", colour='").append(colour).append('\'');
    sb.append(", genderCode='").append(genderCode).append('\'');
    sb.append('}');
    return sb.toString();
  }
}
