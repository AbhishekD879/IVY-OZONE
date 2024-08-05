package com.oxygen.publisher.model;

import lombok.Data;

/**
 * Represents the Racing Form Outcome model. Copied from Middleware Service.
 *
 * @author tvuyiv
 */
@Data
public class OutputRacingFormOutcome {

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
}
