package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.service.public_api.BanachService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BuildYourBetPublicService;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class BuildYourBetPublicServiceTest {

  private static final String BRAND = "bma";

  @Mock private BanachService banachService;
  @Mock private YourCallLeagueService yourCallLeagueService;

  @InjectMocks private BuildYourBetPublicService buildYourBetPublicService;

  @Test
  public void testWithBlacklistedLeagues() {
    List<Long> banachIds = new ArrayList<>(Arrays.asList(123L, 231L));
    when(banachService.getBanachLeaguesIds(BRAND)).thenReturn(banachIds);
    boolean atLeastOneBanachEventAvailable =
        buildYourBetPublicService.isAtLeastOneBanachEventAvailable(BRAND);

    boolean calc = buildYourBetPublicService.calculateAtLeastOneBanachEventAvailable(BRAND);

    Assert.assertTrue(atLeastOneBanachEventAvailable);
    Assert.assertTrue(calc);
  }

  @Test
  public void testWithEmptyBanachLeages() {
    when(banachService.getBanachLeaguesIds(BRAND)).thenReturn(Collections.emptyList());

    boolean atLeastOneBanachEventAvailable =
        buildYourBetPublicService.isAtLeastOneBanachEventAvailable(BRAND);

    boolean calc = buildYourBetPublicService.calculateAtLeastOneBanachEventAvailable(BRAND);

    Assert.assertFalse(atLeastOneBanachEventAvailable);
    Assert.assertFalse(calc);
  }
}
