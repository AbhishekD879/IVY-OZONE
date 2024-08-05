package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.hamcrest.Matchers.hasSize;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.BetPackFilterDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackFilter;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackEnablerFilterRepository;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackEnablerFilterService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicFilterService;
import java.io.IOException;
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
      BetPackMarketPlaceFilterApi.class,
      BetPackFilter.class,
      BetPackFilterDto.class,
      BetPackMarketPlacePublicFilterService.class,
      BetPackEnablerFilterRepository.class,
      BetPackEnablerFilterService.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class BetPackMarketPlaceFilterApiTest {

  private List<BetPackFilter> betPackFilters;

  @MockBean private BetPackMarketPlacePublicFilterService betPackMarketPlacePublicFilterService;

  @MockBean private BetPackEnablerFilterService betPackEnablerFilterService;

  @MockBean private AuthenticationService authenticationService;

  @MockBean private UserService userService;

  @Autowired private MockMvc mockMvc;

  @Before
  public void init() throws IOException {
    final ObjectMapper jsonMapper = new ObjectMapper();
    jsonMapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);
    jsonMapper.registerModule(new JavaTimeModule());
    betPackFilters =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/public_api/betpack/BetpackFilter.json"),
            new TypeReference<List<BetPackFilter>>() {});
  }

  @Test
  public void testGetBetPackByBrand() throws Exception {
    given(betPackMarketPlacePublicFilterService.getActiveBetPackFilterByBrand("coral"))
        .willReturn(betPackFilters);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/coral/bet-pack/filter")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$", hasSize(8)));
  }

  @Test
  public void testGetAllBetPack() throws Exception {
    given(betPackMarketPlacePublicFilterService.getAllBetPackFilter()).willReturn(betPackFilters);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bet-pack/filters")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$", hasSize(8)));
  }
}
