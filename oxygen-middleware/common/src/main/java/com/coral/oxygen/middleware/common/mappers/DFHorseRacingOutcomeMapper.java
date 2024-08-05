package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.df.Horse;
import com.coral.oxygen.middleware.pojos.model.df.RaceEvent;
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome;
import com.coral.oxygen.middleware.pojos.model.output.OutputRacingFormOutcome;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.util.ObjectUtils;

@Slf4j
public class DFHorseRacingOutcomeMapper implements DFRaceOutcomeMapper {

  private int categoryId;

  public DFHorseRacingOutcomeMapper(@Value("${df.category.horse}") int horseCategoryId) {
    this.categoryId = horseCategoryId;
  }

  @Override
  public void map(OutputOutcome outcome, RaceEvent raceEvent) {
    raceEvent.getHorses().stream()
        .filter(h -> outcome.getRunnerNumber().equals(h.getSaddle()))
        .findFirst()
        .ifPresent(c -> map(outcome, c));
  }

  private void map(OutputOutcome outcome, Horse horse) {

    OutputRacingFormOutcome racingFormOutcome = outcome.getRacingFormOutcome();
    if (ObjectUtils.isEmpty(racingFormOutcome)) {
      racingFormOutcome = new OutputRacingFormOutcome();
      outcome.setRacingFormOutcome(racingFormOutcome);
    }

    racingFormOutcome.setTrainer(horse.getTrainer());
    racingFormOutcome.setJockey(horse.getJockey());
    racingFormOutcome.setSilkName(horse.getSilk());
    racingFormOutcome.setFormGuide(horse.getFormfigs());
    racingFormOutcome.setDraw(horse.getDraw());
    racingFormOutcome.setAllowance(horse.getAllowance());

    log.info("Horse race data were mapped succesfully for {}", horse.getHorseName());
  }

  @Override
  public int getCategoryId() {
    return categoryId;
  }
}
