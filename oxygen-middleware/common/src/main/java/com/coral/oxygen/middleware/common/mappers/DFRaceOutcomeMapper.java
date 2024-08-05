package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.df.RaceEvent;
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome;

public interface DFRaceOutcomeMapper {

  void map(OutputOutcome outcome, RaceEvent raceEvent);

  int getCategoryId();
}
