package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.service.public_api.BuildYourBetPublicService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
@Slf4j
public class BybTabAvailabilityService {
  private static final String BUILD_YOUR_BET_CONFIG_NAME = "BuildYourBet";

  private final StructureService structureService;
  private final BuildYourBetPublicService buildYourBetPublicService;

  /**
   * Returns true if build your bet is enabled in system config and at least on build you bet event
   * available
   */
  public boolean isBybEnabledAndLeaguesAvailable(String brand) {
    // todo translate brands like retail, rf .... ?
    return isBuildYourBetConfigurationEnabled(brand, false)
        && buildYourBetPublicService.isAtLeastOneBanachEventAvailable(brand);
  }

  public boolean isBuildYourBetConfigurationEnabled(String brand, boolean defaultValue) {
    try {
      return structureService
          .findByBrandAndConfigName(brand, BUILD_YOUR_BET_CONFIG_NAME)
          .map(bybConfig -> bybConfig.getOrDefault("enabled", defaultValue))
          .map(Boolean.class::cast)
          .orElse(defaultValue);
    } catch (Exception e) {
      log.warn("Encountered exception when checking buildYourBet flag in system config", e);
      return defaultValue;
    }
  }
}
