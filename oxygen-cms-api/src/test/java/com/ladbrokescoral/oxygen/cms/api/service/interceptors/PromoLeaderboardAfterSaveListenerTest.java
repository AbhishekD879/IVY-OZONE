package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.NavigationGroupPublicDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromoLeaderboardConfigPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PromoLeaderboardConfig;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.NavItemPublicService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.PromoLeaderboardPublicService;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import lombok.Getter;
import org.junit.After;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class PromoLeaderboardAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<PromoLeaderboardConfig> {

  @Mock private PromoLeaderboardPublicService service;
  @Mock private NavItemPublicService navItemPublicService;

  @Getter @Mock private PromoLeaderboardConfig entity;

  @Getter @InjectMocks private PromoLeaderboardAfterSaveListener listener;

  @Getter private List<PromoLeaderboardConfigPublicDto> collection = null;

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"ladbrokes", "api/ladbrokes", "promo-leaderboard"},
          {"ladbrokes", "api/ladbrokes", "navigation-group"}
        });
  }

  @Before
  public void init() {
    given(service.findLeaderboardByBrand(anyString()))
        .willReturn(Collections.singletonList(new PromoLeaderboardConfigPublicDto()));
    given(navItemPublicService.getNavigationGroupByBrand(anyString()))
        .willReturn(Collections.singletonList(new NavigationGroupPublicDto()));
  }

  @After
  public void verify() {
    then(context)
        .should()
        .upload(
            brand,
            "api/ladbrokes",
            "promo-leaderboard",
            Collections.singletonList(new PromoLeaderboardConfigPublicDto()));
    then(context)
        .should()
        .upload(
            brand,
            "api/ladbrokes",
            "navigation-group",
            Collections.singletonList(new NavigationGroupPublicDto()));
  }
}
