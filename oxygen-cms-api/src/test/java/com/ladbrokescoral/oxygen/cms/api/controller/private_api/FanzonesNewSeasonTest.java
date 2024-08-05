package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSeason;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesNewSeasonRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewSeasonService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.AdditionalAnswers;
import org.modelmapper.ModelMapper;
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
      FanzonesNewSeasonController.class,
      FanzonesNewSeasonRepository.class,
      FanzonesNewSeasonService.class,
      UserService.class,
      User.class,
      CreatedBy.class,
      Util.class,
      ModelMapper.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class FanzonesNewSeasonTest extends AbstractControllerTest {

  private FanzoneNewSeason fanzoneNewSeason;

  @MockBean FanzonesNewSeasonRepository fanzonesNewSeasonRepository;
  @MockBean ModelMapper modelMapper;
  @Autowired FanzonesNewSeasonService fanzonesNewSeasonService;

  @Before
  public void init() {
    fanzoneNewSeason = createFanzoneNewSeason();

    given(fanzonesNewSeasonRepository.save(any(FanzoneNewSeason.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    given(fanzonesNewSeasonRepository.findAllByBrand(anyString()))
        .willReturn(Optional.of(fanzoneNewSeason));
    given(fanzonesNewSeasonRepository.findAllByBrandAndId(anyString(), anyString()))
        .willReturn(Optional.of(fanzoneNewSeason));
  }

  @Test
  public void testToCreateFanzoneNewSeason() throws Exception {
    FanzoneNewSeason fanzoneNewSeason = createFanzoneNewSeason();
    given(modelMapper.map(any(), any())).willReturn(fanzoneNewSeason);
    given(fanzonesNewSeasonRepository.findAllByBrand(anyString())).willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/fanzone-new-season")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneNewSeason)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToCreateFanzoneNewSeasonException() throws Exception {
    FanzoneNewSeason fanzoneNewSeason = createFanzoneNewSeason();
    given(fanzonesNewSeasonRepository.findAllByBrand(anyString()))
        .willReturn(Optional.of(fanzoneNewSeason));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/fanzone-new-season")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneNewSeason)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testToDeleteAllFanzoneNewSeason() throws Exception {
    given(fanzonesNewSeasonRepository.findAllByBrand(anyString()))
        .willReturn(Optional.of(fanzoneNewSeason));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/ladbrokes/fanzone-new-season")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToReadFanzoneNewSeason() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/ladbrokes/fanzone-new-season")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToUpdateFanzoneNewSeasonById() throws Exception {
    given(modelMapper.map(any(), any())).willReturn(fanzoneNewSeason);
    given(fanzonesNewSeasonRepository.findAllByBrandAndId(anyString(), anyString()))
        .willReturn(Optional.of(fanzoneNewSeason));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/ladbrokes/fanzone-new-season/id/123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneNewSeason)))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testToUpdateFanzoneNewSeasonById1() throws Exception {
    FanzoneNewSeason fanzoneNewSeason = createFanzoneNewSeason();
    fanzoneNewSeason.setId("123");
    given(modelMapper.map(any(), any())).willReturn(fanzoneNewSeason);
    given(fanzonesNewSeasonRepository.findAllByBrandAndId(anyString(), anyString()))
        .willReturn(Optional.of(fanzoneNewSeason));
    given(fanzonesNewSeasonService.findOne(anyString())).willReturn(Optional.of(fanzoneNewSeason));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/ladbrokes/fanzone-new-season/id/123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneNewSeason)))
        .andExpect(status().is2xxSuccessful());
  }

  private static FanzoneNewSeason createFanzoneNewSeason() {
    FanzoneNewSeason entity = new FanzoneNewSeason();
    entity.setId("123");
    entity.setBrand("ladbrokes");
    entity.setFzNewSeasonHeading("Fanzone New Season");
    entity.setFzNewSeasonTitle("Fanzone New Season Pop Up Title");
    entity.setFzNewSeasonDescription("Fanzone New Season Pop Up Descriptionn");
    entity.setFzNewSeasonBgImageDesktop("Fanzone_Syc2");
    entity.setFzNewSeasonBgImageMobile("Fanzone_Syc2");
    entity.setFzNewSeasonBadgeMobile("Fanzone_Syc2");
    entity.setFzNewSeasonBadgeDesktop("Fanzone_Syc2");
    entity.setFzNewSeasonLightningMobile("Fanzone_Syc2");
    entity.setFzNewSeasonLightningDesktop("Fanzone_Syc2");
    return entity;
  }
}
