package com.coral.oxygen.middleware.pojos.model.output;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import lombok.Data;

@Data
public class OutcomeCodes {

  private String outcomeMeaningMajorCode;
  private String outcomeMeaningMinorCode;
  private String outcomeMeaningScores;
  private String outcomeStatusCode;

  @ChangeDetect
  public String getOutcomeMeaningMajorCode() {
    return outcomeMeaningMajorCode;
  }

  public void setOutcomeMeaningMajorCode(String outcomeMeaningMajorCode) {
    this.outcomeMeaningMajorCode = outcomeMeaningMajorCode;
  }

  @ChangeDetect
  public String getOutcomeMeaningMinorCode() {
    return outcomeMeaningMinorCode;
  }

  public void setOutcomeMeaningMinorCode(String outcomeMeaningMinorCode) {
    this.outcomeMeaningMinorCode = outcomeMeaningMinorCode;
  }

  @ChangeDetect
  public String getOutcomeMeaningScores() {
    return outcomeMeaningScores;
  }

  public void setOutcomeMeaningScores(String outcomeMeaningScores) {
    this.outcomeMeaningScores = outcomeMeaningScores;
  }

  @ChangeDetect
  public String getOutcomeStatusCode() {
    return outcomeStatusCode;
  }

  public void setOutcomeStatusCode(String outcomeStatusCode) {
    this.outcomeStatusCode = outcomeStatusCode;
  }
}
