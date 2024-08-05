package com.coral.oxygen.middleware.ms.liveserv.impl.scoreboard;

import com.coral.oxygen.middleware.ms.liveserv.model.scoreboard.ScoreboardEvent;
import java.util.Optional;
import javax.json.JsonString;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class ProviderValidator extends Validator {

  private static final String SUPPORTED_PROVIDER = "opta";

  public ProviderValidator(Validator next) {
    super(next);
  }

  @Override
  protected boolean checkCondition(ScoreboardEvent event) {
    boolean providerIsOpta =
        SUPPORTED_PROVIDER.equalsIgnoreCase(
            Optional.ofNullable(event.getEventStructure().getJsonString("provider"))
                .map(JsonString::getString)
                .orElse(null));
    if (!providerIsOpta) {
      log.debug(
          "Scoreboard update {} for event {} is missing {} provider",
          event.getSequenceId(),
          event.getObEventId(),
          SUPPORTED_PROVIDER);
    }
    return providerIsOpta;
  }
}
