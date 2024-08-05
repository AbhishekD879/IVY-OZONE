package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.hamcrest.Matchers.hasSize;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.BetPackDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackEnablerRepository;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicService;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
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
      BetPackMarketPlaceApi.class,
      BetPackEntity.class,
      BetPackDto.class,
      BetPackMarketPlacePublicService.class,
      BetPackEnablerRepository.class,
      BetPackMarketPlaceService.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class BetPackMarketPlaceApiTest {

  private List<BetPackEntity> betPackEntities;

  @MockBean private BetPackMarketPlacePublicService betPackMarketPlacePublicService;

  @MockBean private BetPackMarketPlaceService betPackMarketPlaceService;

  @MockBean private AuthenticationService authenticationService;

  @MockBean private UserService userService;

  @Autowired private MockMvc mockMvc;

  @Before
  public void init() throws IOException {
    final ObjectMapper jsonMapper = new ObjectMapper();
    jsonMapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);
    jsonMapper.registerModule(new JavaTimeModule());
    betPackEntities =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/public_api/betpack/Betpack.json"),
            new TypeReference<List<BetPackEntity>>() {});
  }

  @Test
  public void testGetBetPackByBrand() throws Exception {
    given(betPackMarketPlacePublicService.getAllBetPack()).willReturn(betPackEntities);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/coral/bet-pack")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
    // .andExpect(jsonPath("$", hasSize(1)));
  }

  @Test
  public void testGetActiveBetPackIds() throws Exception {
    given(betPackMarketPlacePublicService.getActiveBetPackId(anyString()))
        .willReturn(Arrays.asList("1", "2"));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/coral/active-bet-pack-ids")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$", hasSize(2)));
  }

  @Test
  public void testGetActiveBetPackIdsEmptyIds() throws Exception {
    given(betPackMarketPlacePublicService.getActiveBetPackId(anyString()))
        .willReturn(Arrays.asList());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/coral/active-bet-pack-ids")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetAllBetPack() throws Exception {
    given(betPackMarketPlacePublicService.getAllBetPack()).willReturn(betPackEntities);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bet-packs")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$", hasSize(3)));
  }
}
