package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewGamingPopUp;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesNewGamingPopUpRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewGamingPopUpService;
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
      FanzonesNewGamingPopUp.class,
      FanzonesNewGamingPopUpService.class,
      FanzonesNewGamingPopUpRepository.class,
      UserService.class,
      User.class,
      CreatedBy.class,
      Util.class,
      ModelMapper.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class FanzonesNewGamingPopUpTest extends AbstractControllerTest {
  private FanzoneNewGamingPopUp fanzoneNewGamingPopUp;
  @Autowired FanzonesNewGamingPopUpService fanzonesNewGamingPopUpService;
  @MockBean FanzonesNewGamingPopUpRepository fanzonesNewGamingPopUpRepository;
  @MockBean ModelMapper modelMapper;

  @Before
  public void init() {
    fanzoneNewGamingPopUp = createFanzoneNewGamingPopUp();

    given(fanzonesNewGamingPopUpRepository.save(any(FanzoneNewGamingPopUp.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    given(fanzonesNewGamingPopUpRepository.findAllByBrand(anyString()))
        .willReturn(Optional.ofNullable(fanzoneNewGamingPopUp));
    given(fanzonesNewGamingPopUpRepository.findAllByBrandAndId(anyString(), anyString()))
        .willReturn(Optional.ofNullable(fanzoneNewGamingPopUp));
  }

  @Test
  public void testToCreateFanzoneNewGamingPopUp() throws Exception {
    FanzoneNewGamingPopUp fanzoneNewGamingPopUp = createFanzoneNewGamingPopUp();

    given(modelMapper.map(any(), any())).willReturn(fanzoneNewGamingPopUp);
    given(fanzonesNewGamingPopUpRepository.findAllByBrand(anyString()))
        .willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/fanzone-new-gaming-pop-up")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneNewGamingPopUp)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToCreateFanzoneNewGamingPopUpException() throws Exception {
    FanzoneNewGamingPopUp fanzoneNewGamingPopUp = createFanzoneNewGamingPopUp();

    given(fanzonesNewGamingPopUpRepository.findAllByBrand(anyString()))
        .willReturn(Optional.of(fanzoneNewGamingPopUp));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/fanzone-new-gaming-pop-up")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneNewGamingPopUp)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testToReadFanzoneNewGamingPopUp() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/ladbrokes/fanzone-new-gaming-pop-up")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToUpdateFanzoneNewGamingPopUpById() throws Exception {
    given(modelMapper.map(any(), any())).willReturn(fanzoneNewGamingPopUp);
    given(fanzonesNewGamingPopUpRepository.findAllByBrandAndId(anyString(), anyString()))
        .willReturn(Optional.of(fanzoneNewGamingPopUp));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/ladbrokes/fanzone-new-gaming-pop-up/id/123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneNewGamingPopUp)))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testToUpdateFanzoneNewGamingPopUpById1() throws Exception {
    FanzoneNewGamingPopUp fanzoneNewGamingPopUp = createFanzoneNewGamingPopUp();
    fanzoneNewGamingPopUp.setId("123");
    given(modelMapper.map(any(), any())).willReturn(fanzoneNewGamingPopUp);
    given(fanzonesNewGamingPopUpRepository.findAllByBrandAndId(anyString(), anyString()))
        .willReturn(Optional.of(fanzoneNewGamingPopUp));
    given(fanzonesNewGamingPopUpService.findOne(anyString()))
        .willReturn(Optional.of(fanzoneNewGamingPopUp));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/ladbrokes/fanzone-new-gaming-pop-up/id/123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneNewGamingPopUp)))
        .andExpect(status().is2xxSuccessful());
  }

  private FanzoneNewGamingPopUp createFanzoneNewGamingPopUp() {
    FanzoneNewGamingPopUp entity = new FanzoneNewGamingPopUp();
    entity.setBrand("ladbrokes");
    entity.setTitle("Fanzone New Gaming Pop Up");
    entity.setDescription("Fanzone New gaming pop up description here");
    entity.setCloseCTA("close");
    entity.setPlayCTA("play");
    return entity;
  }
}
