package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.Mockito.times;

import com.ladbrokescoral.oxygen.cms.api.service.public_api.BuildYourBetPublicService;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class BybAvailabilityCheckerServiceTest {

  BybAvailabilityCheckerService bybAvailabilityCheckerService;
  @Mock BuildYourBetPublicService buildYourBetPublicService;

  @Before
  public void setup() {
    bybAvailabilityCheckerService = new BybAvailabilityCheckerService(buildYourBetPublicService);
  }

  @Test
  public void executeTest() {
    bybAvailabilityCheckerService.refreshCache();

    Mockito.verify(buildYourBetPublicService, times(1))
        .calculateAtLeastOneBanachEventAvailable("bma");
    Mockito.verify(buildYourBetPublicService, times(1))
        .calculateAtLeastOneBanachEventAvailable("ladbrokes");
  }
}
