package com.coral.oxygen.edp.model.output;

import com.egalacoral.spark.siteserver.model.RacingFormOutcome;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode
public class OutputRacingFormOutcome {

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

  public static OutputRacingFormOutcome newInstance(RacingFormOutcome outcome) {
    return new OutputRacingFormOutcomeBuilder()
        .id(outcome.getId())
        .refRecordType(outcome.getRefRecordType())
        .refRecordId(outcome.getRefRecordId())
        .runnerNumber(outcome.getRunnerNumber())
        .runnerId(outcome.getRunnerId())
        .age(outcome.getAge())
        .trainer(outcome.getTrainer())
        .daysSinceRun(outcome.getDaysSinceRun())
        .draw(outcome.getDraw())
        .jockey(outcome.getJockey())
        .owner(outcome.getOwner())
        .silkName(outcome.getSilkName())
        .formGuide(outcome.getFormGuide())
        .overview(outcome.getOverview())
        .sireOverview(outcome.getSireOverview())
        .breedingOverview(outcome.getBreedingOverview())
        .weight(outcome.getWeight())
        .officialRating(outcome.getOfficialRating())
        .formProviderRating(outcome.getFormProviderRating())
        .runnerStatusCode(outcome.getRunnerStatusCode())
        .colour(outcome.getColour())
        .genderCode(outcome.getGenderCode())
        .build();
  }
}
