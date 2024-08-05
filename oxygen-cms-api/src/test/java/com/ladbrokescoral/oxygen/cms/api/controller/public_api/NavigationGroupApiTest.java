package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.NavItem;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationGroup;
import com.ladbrokescoral.oxygen.cms.api.repository.NavItemRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.NavigationGroupRepository;
import com.ladbrokescoral.oxygen.cms.api.service.NavItemService;
import com.ladbrokescoral.oxygen.cms.api.service.NavigationGroupService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.NavItemPublicService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.NavigationGroupPublicService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.Arrays;
import java.util.Collections;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({
  NavigationGroupApi.class,
  NavigationGroupPublicService.class,
  NavItemPublicService.class
})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
class NavigationGroupApiTest extends AbstractControllerTest {

  @MockBean private NavigationGroupService navigationGroupService;
  @MockBean private NavigationGroupRepository navigationGroupRepository;

  @MockBean private NavItemService navItemService;
  @MockBean private NavItemRepository navItemRepository;

  public static final String BRAND = "ladbrokes";
  private NavItem navItem;
  private NavigationGroup navigationGroup1;
  private NavigationGroup navigationGroup2;

  @BeforeEach
  public void setUp() throws Exception {
    navigationGroup1 =
        TestUtil.deserializeWithJackson(
            "controller/private_api/createNavigationGrp.json", NavigationGroup.class);
    navigationGroup1.setId("124");
    navigationGroup2 =
        TestUtil.deserializeWithJackson(
            "controller/private_api/createNavigationGrp.json", NavigationGroup.class);
    navigationGroup2.setId("125");

    navItem =
        TestUtil.deserializeWithJackson("controller/private_api/createNavItem.json", NavItem.class);
  }

  @Test
  void getNavigationGroupByBrandTest() throws Exception {
    navItem.setNavigationGroupId("124");
    when(navItemService.findAllNavItem(any())).thenReturn(Collections.singletonList(navItem));
    when(navigationGroupService.findAllActiveNavigationGroupByBrand(any()))
        .thenReturn(Arrays.asList(navigationGroup1, navigationGroup2));
    when(navItemService.getNavItemWithActiveLbr(any()))
        .thenReturn(Collections.singletonList(navItem));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/navigation-group")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  void getNavigationGroupByBrandTestWithoutNavItem() throws Exception {
    navItem.setNavigationGroupId("126");
    when(navItemService.findAllNavItem(any())).thenReturn(Arrays.asList(navItem));
    when(navigationGroupService.findAllActiveNavigationGroupByBrand(any()))
        .thenReturn(Arrays.asList(navigationGroup1, navigationGroup2));
    when(navItemService.getNavItemWithActiveLbr(any())).thenReturn(Arrays.asList(navItem));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/navigation-group")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }
}
