package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSignposting;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesNewSignpostingRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewSignpostingService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
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
      FanzonesNewSignposting.class,
      FanzonesNewSignpostingRepository.class,
      FanzonesNewSignpostingService.class,
      UserService.class,
      User.class,
      CreatedBy.class,
      Util.class,
      ModelMapper.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class FanzonesNewSignpostingTest extends AbstractControllerTest {

  private FanzoneNewSignposting fanzoneNewSignposting;

  @MockBean FanzonesNewSignpostingRepository fanzonesNewSignpostingRepository;
  @MockBean ModelMapper modelMapper;
  @Autowired FanzonesNewSignpostingService fanzonesNewSignpostingService;

  @Before
  public void init() {
    fanzoneNewSignposting = createFanzoneNewSignposting();

    given(fanzonesNewSignpostingRepository.save(any(FanzoneNewSignposting.class)))
        .will(AdditionalAnswers.returnsFirstArg());
    given(fanzonesNewSignpostingRepository.findAllByBrand(anyString()))
        .willReturn(Optional.of(fanzoneNewSignposting));
    given(fanzonesNewSignpostingRepository.findAllByBrandAndId(anyString(), anyString()))
        .willReturn(Optional.of(fanzoneNewSignposting));
  }

  @Test
  public void testToCreateFanzoneNewSignposting() throws Exception {
    FanzoneNewSignposting fanzoneNewSignposting = createFanzoneNewSignposting();
    given(modelMapper.map(any(), any())).willReturn(fanzoneNewSignposting);
    given(fanzonesNewSignpostingRepository.findAllByBrand(anyString()))
        .willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/fanzone-new-signposting")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneNewSignposting)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToCreateFanzoneNewSignpostingException() throws Exception {
    FanzoneNewSignposting fanzoneNewSignposting = createFanzoneNewSignposting();
    given(fanzonesNewSignpostingRepository.findAllByBrand(anyString()))
        .willReturn(Optional.of(fanzoneNewSignposting));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/ladbrokes/fanzone-new-signposting")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneNewSignposting)))
        .andExpect(status().is4xxClientError());
  }

  /*@Test
  public void testToDeleteAllFanzoneNewSeason() throws Exception {
      given(fanzonesNewSignpostingRepository.findAllByBrand(anyString()))
              .willReturn(Optional.of(fanzoneNewSignposting));
      this.mockMvc
              .perform(
                      MockMvcRequestBuilders.delete("/v1/api/ladbrokes/fanzone-new-signposting")
                              .contentType(MediaType.APPLICATION_JSON))
              .andExpect(status().is2xxSuccessful());
  }*/

  @Test
  public void testToReadFanzoneNewSignposting() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/ladbrokes/fanzone-new-signposting")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToUpdateFanzoneNewSignpostingById() throws Exception {
    given(modelMapper.map(any(), any())).willReturn(fanzoneNewSignposting);
    given(fanzonesNewSignpostingRepository.findAllByBrandAndId(anyString(), anyString()))
        .willReturn(Optional.of(fanzoneNewSignposting));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/ladbrokes/fanzone-new-signposting/id/123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneNewSignposting)))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testToUpdateFanzoneNewSignpostingById1() throws Exception {
    FanzoneNewSignposting fanzoneNewSignposting1 = createFanzoneNewSignposting();
    fanzoneNewSignposting1.setId("123");
    given(modelMapper.map(any(), any())).willReturn(fanzoneNewSignposting1);
    given(fanzonesNewSignpostingRepository.findAllByBrandAndId(anyString(), anyString()))
        .willReturn(Optional.of(fanzoneNewSignposting1));
    given(fanzonesNewSignpostingService.findOne(anyString()))
        .willReturn(Optional.of(fanzoneNewSignposting));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/ladbrokes/fanzone-new-signposting/id/123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(fanzoneNewSignposting)))
        .andExpect(status().is2xxSuccessful());
  }

  private static FanzoneNewSignposting createFanzoneNewSignposting() {
    FanzoneNewSignposting entity = new FanzoneNewSignposting();
    entity.setId("123");
    entity.setBrand("ladbrokes");
    entity.setActive(true);
    entity.setNewSignPostingIcon("new");
    entity.setStartDate(Instant.now().plus(5, ChronoUnit.DAYS));
    entity.setEndDate(Instant.now().plus(6, ChronoUnit.DAYS));
    return entity;
  }
}
