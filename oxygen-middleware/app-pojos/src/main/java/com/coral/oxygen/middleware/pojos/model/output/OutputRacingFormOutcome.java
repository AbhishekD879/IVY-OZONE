package com.coral.oxygen.middleware.pojos.model.output;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import java.io.Serializable;

public class OutputRacingFormOutcome implements Serializable {

  private String id;
  private String silkName;
  private String formGuide;
  private String jockey;
  private String trainer;
  private Integer allowance;
  private String draw;
  private String runnerNumber;
  private String genderCode;

  private String formFig;

  public void setFormFig(String formFig) {
    this.formFig = formFig;
  }

  public String getFormFig() {
    return formFig;
  }

  @ChangeDetect
  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  @ChangeDetect
  public String getRunnerNumber() {
    return runnerNumber;
  }

  public void setRunnerNumber(String runnerNumber) {
    this.runnerNumber = runnerNumber;
  }

  @ChangeDetect
  public String getTrainer() {
    return trainer;
  }

  public void setTrainer(String trainer) {
    this.trainer = trainer;
  }

  @ChangeDetect
  public String getDraw() {
    return draw;
  }

  public void setDraw(String draw) {
    this.draw = draw;
  }

  @ChangeDetect
  public String getJockey() {
    return jockey;
  }

  public void setJockey(String jockey) {
    this.jockey = jockey;
  }

  @ChangeDetect
  public String getSilkName() {
    return silkName;
  }

  public void setSilkName(String silkName) {
    this.silkName = silkName;
  }

  @ChangeDetect
  public String getFormGuide() {
    return formGuide;
  }

  public void setFormGuide(String formGuide) {
    this.formGuide = formGuide;
  }

  @ChangeDetect
  public String getGenderCode() {
    return genderCode;
  }

  public void setGenderCode(String genderCode) {
    this.genderCode = genderCode;
  }

  @ChangeDetect
  public Integer getAllowance() {
    return allowance;
  }

  public void setAllowance(Integer allowance) {
    this.allowance = allowance;
  }
}
