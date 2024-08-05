package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.doReturn;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.BetPackBannerDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackBanner;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceBannerService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicBannerService;
import java.io.IOException;
import java.util.Collections;
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
      BetPackMarketPlaceBannerApi.class,
      BetPackBanner.class,
      BetPackBannerDto.class,
      BetPackMarketPlacePublicBannerService.class,
      BetPackMarketPlaceBannerService.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class BetPackMarketPlaceBannerApiTest {

  private List<BetPackBanner> betPackBanner;

  @MockBean private BetPackMarketPlacePublicBannerService betPackMarketPlacePublicBannerService;

  @MockBean private BetPackMarketPlaceBannerService betPackMarketPlaceBannerService;

  @MockBean private AuthenticationService authenticationService;

  @MockBean private UserService userService;

  @Autowired private MockMvc mockMvc;

  @Before
  public void init() throws IOException {
    final ObjectMapper jsonMapper = new ObjectMapper();
    jsonMapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);
    jsonMapper.registerModule(new JavaTimeModule());
    betPackBanner =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/public_api/betpack/BetpackBanner.json"),
            new TypeReference<List<BetPackBanner>>() {});
  }

  @Test
  public void testGetBetPackByBrand() throws Exception {
    given(betPackMarketPlacePublicBannerService.getBetPackBannerByBrand("coral"))
        .willReturn(betPackBanner);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/coral/bet-pack/banner")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetBetPackByBrandEmptyList() throws Exception {
    doReturn(Collections.emptyList())
        .when(betPackMarketPlacePublicBannerService)
        .getBetPackBannerByBrand(anyString());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/coral/bet-pack/banner")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}