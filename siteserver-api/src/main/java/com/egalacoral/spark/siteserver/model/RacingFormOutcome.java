package com.egalacoral.spark.siteserver.model;

import lombok.Data;

@Data
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
}
