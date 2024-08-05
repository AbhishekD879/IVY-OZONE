package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesClubRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesClubService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Arrays;
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
      FanzonesClub.class,
      FanzonesClubRepository.class,
      FanzonesClubService.class,
      UserService.class,
      User.class,
      CreatedBy.class,
      Util.class,
      ModelMapper.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class FanzonesClubTest extends AbstractControllerTest {
  private FanzoneClub fanzoneClub;

  @MockBean private FanzonesClubRepository fanzonesClubRepository;
  @MockBean private ModelMapper modelMapper;
  @Autowired private FanzonesClubService fanzonesClubService;

  @Before
  public void init() {
    fanzoneClub = createFanzoneClub();
    given(fanzonesClubRepository.save(any(FanzoneClub.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    given(fanzonesClubRepository.findByBrandAndColumn(anyString(), anyString(), anyString()))
        .willReturn(Optional.of(fanzoneClub));
    given(fanzonesClubRepository.findAllFanzonesByBrand(anyString()))
        .willReturn(Optional.of(Arrays.asList(fanzoneClub)));
  }

  @Test
  public void testToCreateFanzoneClub() throws Exception {
    given(modelMapper.map(any(), any())).willReturn(fanzoneClub);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/fanzone-club")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneClub)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToReadAllFanzones() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/ladbrokes/fanzone-club")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToReadFanzoneById() throws Exception {
    given(fanzonesClubService.findOne(anyString())).willReturn(Optional.of(fanzoneClub));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/ladbrokes/fanzone-club/id/123")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToUpdateFanzoneClub() throws Exception {
    FanzoneClub fanzoneClub = createFanzoneClub();
    fanzoneClub.setId("123");
    String id = "123";
    given(modelMapper.map(any(), any())).willReturn(fanzoneClub);
    given(fanzonesClubRepository.findByBrandAndColumn(anyString(), anyString(), anyString()))
        .willReturn(Optional.of(fanzoneClub));
    given(fanzonesClubService.findOne(id)).willReturn(Optional.of(fanzoneClub));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/ladbrokes/fanzone-club/id/123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneClub)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToDeleteAllFanzonesClub() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/ladbrokes/fanzone-club")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToDeleteMultipleFanzoneClub() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/ladbrokes/fanzone-club/id/123,456")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private static FanzoneClub createFanzoneClub() {
    FanzoneClub entity = new FanzoneClub();
    entity.setPageName("fanzone-club");
    entity.setId("123");
    entity.setBrand("ladbrokes");
    entity.setActive(true);
    entity.setBannerLink("www.asset.com");
    entity.setTitle("club");
    entity.setDescription("welcome to clubs");
    entity.setValidityPeriodStart(Instant.now().plus(5, ChronoUnit.DAYS));
    entity.setValidityPeriodEnd(Instant.now().plus(6, ChronoUnit.DAYS));
    return entity;
  }
}
