package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.OutputRacingFormOutcomeDetailed;
import com.egalacoral.spark.siteserver.model.RacingFormOutcome;

public class SimpleRacingForOutcomeMapper implements RacingForOutcomeMapper {
  @Override
  public OutputRacingFormOutcomeDetailed map(RacingFormOutcome rfo) {
    OutputRacingFormOutcomeDetailed outputRacingFormOutcome = new OutputRacingFormOutcomeDetailed();
    outputRacingFormOutcome.setId(rfo.getId());
    outputRacingFormOutcome.setRefRecordType(rfo.getRefRecordType());
    outputRacingFormOutcome.setRefRecordId(rfo.getRefRecordId());
    outputRacingFormOutcome.setRunnerNumber(rfo.getRunnerNumber());
    outputRacingFormOutcome.setRunnerId(rfo.getRunnerId());
    outputRacingFormOutcome.setAge(rfo.getAge());
    outputRacingFormOutcome.setTrainer(rfo.getTrainer());
    outputRacingFormOutcome.setDaysSinceRun(rfo.getDaysSinceRun());
    outputRacingFormOutcome.setDraw(rfo.getDraw());
    outputRacingFormOutcome.setJockey(rfo.getJockey());
    outputRacingFormOutcome.setOwner(rfo.getOwner());
    outputRacingFormOutcome.setSilkName(rfo.getSilkName());
    outputRacingFormOutcome.setFormGuide(rfo.getFormGuide());
    outputRacingFormOutcome.setOverview(rfo.getOverview());
    outputRacingFormOutcome.setSireOverview(rfo.getSireOverview());
    outputRacingFormOutcome.setBreedingOverview(rfo.getBreedingOverview());
    outputRacingFormOutcome.setWeight(rfo.getWeight());
    outputRacingFormOutcome.setOfficialRating(rfo.getOfficialRating());
    outputRacingFormOutcome.setFormProviderRating(rfo.getFormProviderRating());
    outputRacingFormOutcome.setRunnerStatusCode(rfo.getRunnerStatusCode());
    outputRacingFormOutcome.setColour(rfo.getColour());
    outputRacingFormOutcome.setGenderCode(rfo.getGenderCode());

    return outputRacingFormOutcome;
  }
}
