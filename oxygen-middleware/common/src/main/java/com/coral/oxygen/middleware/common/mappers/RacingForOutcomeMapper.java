package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.OutputRacingFormOutcomeDetailed;
import com.egalacoral.spark.siteserver.model.RacingFormOutcome;

/** Created by idomshchikov on 12/23/16. */
public interface RacingForOutcomeMapper {

  OutputRacingFormOutcomeDetailed map(RacingFormOutcome racingFormOutcome);
}
