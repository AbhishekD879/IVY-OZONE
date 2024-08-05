package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.PromoLeaderboardConfig;
import com.ladbrokescoral.oxygen.cms.api.repository.PromoLeaderboardRepository;
import com.ladbrokescoral.oxygen.cms.api.service.PromoLeaderboardService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.PromoLeaderboardPublicService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.Arrays;
import java.util.Collections;
import org.junit.Before;
import org.junit.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({PromoLeaderboardApi.class, PromoLeaderboardPublicService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class PromoLeaderboardApiTest extends AbstractControllerTest {

  @MockBean private PromoLeaderboardService promoLeaderboardService;
  @MockBean private PromoLeaderboardRepository promoLeaderboardRepository;
  private PromoLeaderboardConfig promoLeaderboardConfig;

  @Before
  public void init() throws Exception {
    promoLeaderboardConfig =
        TestUtil.deserializeWithJackson(
            "controller/private_api/createPromoLeaderboard.json", PromoLeaderboardConfig.class);
  }

  @Test
  public void findPromoLeaderboardByBrandTest() throws Exception {
    given(promoLeaderboardRepository.findByBrand(any()))
        .willReturn(Collections.singletonList(promoLeaderboardConfig));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/promo-leaderboard")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void findPromoLeaderboardByBrandWithExpireLbrTest() throws Exception {
    PromoLeaderboardConfig promoLeaderboardConfig1 = promoLeaderboardConfig;
    promoLeaderboardConfig1.setStatus(false);
    given(promoLeaderboardRepository.findByBrand(any()))
        .willReturn(Arrays.asList(promoLeaderboardConfig, promoLeaderboardConfig1));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/promo-leaderboard")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}
