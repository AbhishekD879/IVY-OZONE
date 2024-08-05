package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.BetSharingEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.BetSharingRepository;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      BetSharingApi.class,
      BetSharingService.class,
    })
@AutoConfigureMockMvc(addFilters = false)
public class BetSharingApiTest {
  @MockBean private BetSharingRepository repository;
  @MockBean private ModelMapper mapper;
  @MockBean private AuthenticationService authenticationService;
  @MockBean private UserService userService;

  private List<BetSharingEntity> betSharingEntities;
  @Autowired private MockMvc mockMvc;

  @Before
  public void init() throws IOException {
    final ObjectMapper jsonMapper = new ObjectMapper();
    jsonMapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);
    jsonMapper.registerModule(new JavaTimeModule());

    betSharingEntities =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/public_api/BetSharing/betSharing.json"),
            new TypeReference<List<BetSharingEntity>>() {});
  }

  @Test
  public void testGetBetSharingByBrand() throws Exception {
    given(repository.findByBrand("coral")).willReturn(betSharingEntities);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/coral/bet-sharing")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetBetSharingByBrandNoContent() throws Exception {
    given(repository.findByBrand("coral")).willReturn(Arrays.asList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/coral/bet-sharing")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }
}
