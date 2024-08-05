package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.service.public_api.BuildYourBetPublicService;
import java.util.Arrays;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class BybAvailabilityCheckerService {

  private BuildYourBetPublicService buildYourBetPublicService;

  @Autowired
  public BybAvailabilityCheckerService(BuildYourBetPublicService buildYourBetPublicService) {
    this.buildYourBetPublicService = buildYourBetPublicService;
  }

  @Scheduled(
      fixedDelayString = "${byb.check-availability.period-millis:3000}",
      initialDelayString = "${byb.check-availability.initial-delay:0}")
  public void refreshCache() {
    // todo parallel?
    Arrays.asList("bma", "ladbrokes").forEach(this::refreshForBrand);
  }

  private void refreshForBrand(String brand) {
    try {
      buildYourBetPublicService.calculateAtLeastOneBanachEventAvailable(brand);
    } catch (Exception e) {
      log.warn("[{}] Failed to refresh buildYourBet leagues availability cache", brand, e);
    }
  }
}
