package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.BetPackOnboardingDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackOnboarding;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackMarketplaceOnboardingRepository;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceOnboardingService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicOnboardingService;
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
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      BetPackMarketPlaceOnboardingApi.class,
      BetPackOnboarding.class,
      BetPackOnboardingDto.class,
      BetPackMarketPlaceOnboardingService.class,
      BetPackMarketPlacePublicOnboardingService.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class BetPackMarketPlaceOnboardingApiTest {

  @MockBean private BetPackMarketplaceOnboardingRepository repository;

  @MockBean
  private BetPackMarketPlacePublicOnboardingService betPackMarketPlacePublicOnboardingService;

  @MockBean private BetPackMarketPlaceOnboardingService betPackMarketPlaceOnboardingService;

  @MockBean private MongoTemplate mongoTemplate;

  @MockBean private ImageService imageService;

  @MockBean private AuthenticationService authenticationService;

  @MockBean private UserService userService;

  private List<BetPackOnboarding> betPackOnboardings;

  @Autowired private MockMvc mockMvc;

  @Before
  public void init() throws IOException {
    final ObjectMapper jsonMapper = new ObjectMapper();
    jsonMapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);
    jsonMapper.registerModule(new JavaTimeModule());

    betPackOnboardings =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream(
                "controller/public_api/betpack/BetpackOnboarding.json"),
            new TypeReference<List<BetPackOnboarding>>() {});
    System.out.println(betPackOnboardings);
  }

  @Test
  public void testGetBetPackByBrand() throws Exception {
    given(betPackMarketPlacePublicOnboardingService.getBpmpOnboardingByBrand("coral"))
        .willReturn(betPackOnboardings);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/coral/bet-pack/onboarding")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetBetPackByBrand_NoContent() throws Exception {
    given(betPackMarketPlacePublicOnboardingService.getBpmpOnboardingByBrand("coral"))
        .willReturn(Arrays.asList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/coral/bet-pack/onboarding")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}
