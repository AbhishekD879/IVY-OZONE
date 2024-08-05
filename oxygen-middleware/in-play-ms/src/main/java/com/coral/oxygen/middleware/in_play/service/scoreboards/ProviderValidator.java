package com.coral.oxygen.middleware.in_play.service.scoreboards;

import java.util.List;
import java.util.Optional;
import javax.json.JsonString;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class ProviderValidator extends Validator {

  private final List<String> SUPPORTED_PROVIDERS;

  public ProviderValidator(Validator next, List<String> supportedProviders) {
    super(next);
    this.SUPPORTED_PROVIDERS = supportedProviders;
  }

  @Override
  public boolean checkCondition(ScoreboardEvent scoreboardEvent) {
    boolean isSupportedProvider =
        SUPPORTED_PROVIDERS.stream()
            .anyMatch(
                provider ->
                    provider.equalsIgnoreCase(
                        Optional.ofNullable(
                                scoreboardEvent.getEventStructure().getJsonString("provider"))
                            .map(JsonString::getString)
                            .orElse(null)));
    if (!isSupportedProvider) {
      log.debug(
          "Scoreboard update {} for event {} is missing {} provider",
          scoreboardEvent.getSequenceId(),
          scoreboardEvent.getObEventId(),
          SUPPORTED_PROVIDERS);
    }
    return isSupportedProvider;
  }
}
