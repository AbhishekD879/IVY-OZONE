package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.df.RaceEvent;
import com.coral.oxygen.middleware.pojos.model.df.Runner;
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome;
import com.coral.oxygen.middleware.pojos.model.output.OutputRacingFormOutcome;
import lombok.extern.slf4j.Slf4j;
import org.springframework.util.ObjectUtils;

@Slf4j
public class DFGreyhoundRacingOutcomeMapper implements DFRaceOutcomeMapper {

  private int categoryId;

  public DFGreyhoundRacingOutcomeMapper(int categoryId) {
    this.categoryId = categoryId;
  }

  @Override
  public void map(OutputOutcome outcome, RaceEvent raceEvent) {
    raceEvent.getRunners().stream()
        .filter(h -> outcome.getRunnerNumber().equals(h.getTrap()))
        .findFirst()
        .ifPresent(c -> map(outcome, c));
  }

  @Override
  public int getCategoryId() {
    return categoryId;
  }

  private void map(OutputOutcome outcome, Runner runner) {
    OutputRacingFormOutcome racingFormOutcome = outcome.getRacingFormOutcome();
    if (ObjectUtils.isEmpty(racingFormOutcome)) {
      racingFormOutcome = new OutputRacingFormOutcome();
      outcome.setRacingFormOutcome(racingFormOutcome);
    }
    racingFormOutcome.setGenderCode(runner.getDogSex());
    log.info("Horse race data were mapped succesfully for {}", runner.getDogName());
  }
}
