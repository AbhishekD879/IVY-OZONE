package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.NavigationGroupPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationGroup;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.NavItemPublicService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.NavigationGroupPublicService;
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
public class NavigationGroupAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<NavigationGroup> {

  @Mock NavigationGroupPublicService navigationGroupPublicService;

  @Mock NavItemPublicService navItemPublicService;

  @Getter @Mock private NavigationGroup entity;

  @Getter @InjectMocks private NavigationGroupAfterSaveListener listener;

  @Getter private List<?> collection = null;

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"ladbrokes", "api/ladbrokes", "navigation-group"}});
  }

  @Before
  public void init() {
    given(navigationGroupPublicService.getNavigationGroupByBrand(anyString()))
        .willReturn(Collections.singletonList(new NavigationGroupPublicDto()));
  }

  @After
  public void verify() {
    then(context)
        .should()
        .upload(
            brand,
            "api/ladbrokes",
            "navigation-group",
            Collections.singletonList(new NavigationGroupPublicDto()));
  }
}
