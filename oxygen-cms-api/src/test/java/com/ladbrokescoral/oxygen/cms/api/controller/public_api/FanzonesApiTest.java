package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesService;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(value = {FanzonesService.class, FanzonesApi.class})
@AutoConfigureMockMvc(addFilters = false)
public class FanzonesApiTest extends AbstractControllerTest {

  private Fanzone fanzone;

  @MockBean FanzonesRepository fanzonesRepository;

  @Before
  public void init() {
    fanzone = createFanzone();
    given(fanzonesRepository.findAllFanzonesByBrand(anyString()))
        .willReturn(Optional.of(Arrays.asList(fanzone)));
  }

  @Test
  public void testToReadAllFanzones() throws Exception {
    given(fanzonesRepository.findAllFanzonesByBrand(anyString()))
        .willReturn(Optional.of(Arrays.asList(fanzone)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/fanzone")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private static Fanzone createFanzone() {
    Fanzone entity = new Fanzone();
    entity.setId("616e7a3c54409d7519879827");
    entity.setBrand("ladbrokes");
    entity.setLaunchBannerUrl("www.url.com");
    entity.setName("Fanzone");
    entity.setTeamId("310");
    entity.setOpenBetID("OB567800");
    entity.setAssetManagementLink("www.assetManagementLink.com");
    entity.setPrimaryCompetitionId("990,991,992");
    entity.setSecondaryCompetitionId("1,2,3");
    entity.setClubIds("990,991,992");
    entity.setLocation("stadium3,Nagpur,ADDA205");
    entity.setOutRightsLbl("obl");
    entity.setPremierLeagueLbl("abc");
    entity.setActive(false);
    entity.setNextGamesLbl("leicester");
    FanzoneConfiguration fanzoneConfiguration = new FanzoneConfiguration();
    fanzoneConfiguration.setShowNowNext(true);
    fanzoneConfiguration.setShowStats(false);
    fanzoneConfiguration.setShowClubs(false);
    fanzoneConfiguration.setSportsRibbon(true);
    fanzoneConfiguration.setAtozMenu(false);
    fanzoneConfiguration.setHomePage(true);
    fanzoneConfiguration.setFootballHome(false);
    fanzoneConfiguration.setLaunchBannerUrlDesktop("www.url.com");
    fanzoneConfiguration.setFanzoneBannerDesktop("www.url.com");
    fanzoneConfiguration.setShowGames(true);

    return entity;
  }
}
