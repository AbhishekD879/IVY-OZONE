package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.AdditionalAnswers;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.annotation.CreatedBy;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      Fanzones.class,
      FanzonesRepository.class,
      FanzonesService.class,
      UserService.class,
      User.class,
      CreatedBy.class,
      Util.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class FanzonesTest extends AbstractControllerTest {
  @MockBean private Fanzone fanzone;
  @MockBean private FanzonesRepository fanzonesRepository;
  @Autowired private FanzonesService fanzonesService;

  @Before
  public void init() {
    fanzone = createFanzone();

    given(fanzonesRepository.save(any(Fanzone.class))).will(AdditionalAnswers.returnsFirstArg());
    given(fanzonesRepository.findByBrandAndColumn(anyString(), anyString(), anyString()))
        .willReturn(Optional.of(fanzone));
    given(fanzonesRepository.findAllFanzonesByBrand(anyString()))
        .willReturn(Optional.of(Arrays.asList(fanzone)));
  }

  @Test
  public void testToCreateFanzoneByBrandSuccess() throws Exception {
    Fanzone fanzone1 = createFanzone();
    Fanzone fanzone2 = new Fanzone();
    fanzone2.setName("hello");
    fanzone2.setTeamId("100");
    given(fanzonesRepository.findAllFanzonesByBrand(anyString()))
        .willReturn(Optional.of(Arrays.asList(fanzone2)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/fanzone")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzone1)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToSet21stteamtrue() throws Exception {
    Fanzone fanzone = createFanzone21stTeam();
    Fanzone fanzone1 = new Fanzone();
    fanzone1.setName("hello");
    fanzone1.setTeamId("100");
    fanzone1.setIs21stOrUnlistedFanzoneTeam(true);
    given(fanzonesRepository.findAllFanzonesByBrand(anyString()))
        .willReturn(Optional.of(Arrays.asList(fanzone1)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/fanzone")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzone)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToCreateFanzoneException() throws Exception {
    Fanzone fanzone1 = createFanzone();
    Fanzone fanzone2 = new Fanzone();
    fanzone2.setName("hello");
    fanzone2.setTeamId("1");
    given(fanzonesRepository.findAllFanzonesByBrand(anyString()))
        .willReturn(Optional.of(Arrays.asList(fanzone1)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/fanzone")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzone2)))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testToReadAllFanzones() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/ladbrokes/fanzone")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToReadFanzoneById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/ladbrokes/fanzone/id/123")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToUpdateFanzone() throws Exception {
    Fanzone fanzone1 = createFanzone();
    fanzone1.setName("evertonnn");
    List<Fanzone> li = new ArrayList<Fanzone>();
    li.add(fanzone1);
    li.get(0).setTeamId("23");
    li.get(0).setName("evrtom");
    Fanzone fanzone2 = createFanzone();
    fanzone2.setName("Arsenallll");
    fanzone2.setId("1234");
    fanzone2.setTeamId("9");
    li.add(fanzone2);
    li.get(1).setTeamId("27");
    li.get(1).setName("brighton");
    Fanzone fanzone3 = createFanzone();
    fanzone3.setName("brightonnnnn");
    fanzone3.setId("1236");
    fanzone3.setTeamId("20");
    li.add(fanzone3);
    String brand = "L";
    given(fanzonesRepository.findByBrandAndColumn(anyString(), anyString(), anyString()))
        .willReturn(Optional.of(fanzone1));
    given(fanzonesRepository.findAllFanzonesByBrand(anyString())).willReturn(Optional.of(li));
    given(fanzonesService.findOne(anyString())).willReturn(Optional.of(createFanzone()));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/ladbrokes/fanzone/id/123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzone1)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToDeleteAllFanzones() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/ladbrokes/fanzone")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToDeleteMultipleFanzone() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/ladbrokes/fanzone/id/123,456")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private static Fanzone createFanzone() {
    Fanzone entity = new Fanzone();
    entity.setId("616e7a3c54409d7519879827");
    entity.setBrand("ladbrokes");
    entity.setLaunchBannerUrl("www.url.com");
    entity.setName("abc");
    entity.setTeamId("1");
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
    fanzoneConfiguration.setShowCompetitionTable(true);
    fanzoneConfiguration.setShowNowNext(true);
    fanzoneConfiguration.setShowStats(false);
    fanzoneConfiguration.setShowClubs(false);
    fanzoneConfiguration.setSportsRibbon(true);
    fanzoneConfiguration.setAtozMenu(false);
    fanzoneConfiguration.setHomePage(true);
    fanzoneConfiguration.setFootballHome(false);
    fanzoneConfiguration.setLaunchBannerUrlDesktop("www.url.com");
    fanzoneConfiguration.setFanzoneBannerDesktop("www.url.com");
    fanzoneConfiguration.setShowGames(false);
    fanzoneConfiguration.setShowScratchCards(false);
    fanzoneConfiguration.setShowSlotRivals(false);
    return entity;
  }

  private static Fanzone createFanzone21stTeam() {
    Fanzone entity = new Fanzone();
    entity.setId("616e7a3c54409d7519879827");
    entity.setBrand("ladbrokes");
    entity.setLaunchBannerUrl("www.url.com");
    entity.setName("abc");
    entity.setTeamId("21");
    entity.setAssetManagementLink("www.assetManagementLink.com");
    entity.setLocation("stadium3,Nagpur,ADDA205");
    entity.setOutRightsLbl("obl");
    entity.setPremierLeagueLbl("abc");
    entity.setActive(false);
    entity.setNextGamesLbl("leicester");
    FanzoneConfiguration fanzoneConfiguration = new FanzoneConfiguration();
    fanzoneConfiguration.setShowCompetitionTable(true);
    fanzoneConfiguration.setShowNowNext(true);
    fanzoneConfiguration.setShowStats(false);
    fanzoneConfiguration.setSportsRibbon(true);
    fanzoneConfiguration.setAtozMenu(false);
    fanzoneConfiguration.setHomePage(true);
    fanzoneConfiguration.setFootballHome(false);
    fanzoneConfiguration.setLaunchBannerUrlDesktop("www.url.com");
    fanzoneConfiguration.setFanzoneBannerDesktop("www.url.com");
    return entity;
  }
}
