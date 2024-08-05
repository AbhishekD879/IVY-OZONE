package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.hamcrest.Matchers.is;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.Users;
import com.ladbrokescoral.oxygen.cms.api.entity.AssetManagement;
import com.ladbrokescoral.oxygen.cms.api.service.AssetManagementService;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.AssetManagementPublicService;
import java.util.Arrays;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      Users.class,
      AuthenticationService.class,
      AssetManagementPublicApi.class,
      AssetManagementPublicService.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class AssetManagementPublicApiTest {

  @MockBean private UserService userServiceMock;

  @MockBean private AssetManagementService assetManagementService;

  @Autowired private MockMvc mockMvc;

  private AssetManagement assetManagement;

  @Before
  public void init() {
    assetManagement = assetManagement();
    Mockito.when(
            assetManagementService.findByBrandAndNamesAndSportId(
                "bma", Arrays.asList("Liverpool"), 16))
        .thenReturn(Arrays.asList(assetManagement()));

    Mockito.when(assetManagementService.findAllByBrand("bma"))
        .thenReturn(Arrays.asList(assetManagement()));
  }

  private AssetManagement assetManagement() {
    AssetManagement assetManagement = new AssetManagement();
    assetManagement.setActive(true);
    assetManagement.setBrand("bma");
    assetManagement.setHighlightCarouselToggle(true);
    assetManagement.setSportId(16);
    assetManagement.setTeamName("Liverpool");
    return assetManagement;
  }

  @Test
  public void testFindByBrandAndNamesAndSportId() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                "/cms/api/bma/asset-management?teamNames=Liverpool&sportId=16"))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.[0].teamName", is("Liverpool")));
  }

  @Test
  public void testFindByBrand() throws Exception {
    this.mockMvc
        .perform(MockMvcRequestBuilders.get("/cms/api/bma/asset-management/brand"))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.[0].teamName", is("Liverpool")));
  }
}
