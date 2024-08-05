package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Gamification;
import com.ladbrokescoral.oxygen.cms.api.repository.GamificationRepository;
import com.ladbrokescoral.oxygen.cms.api.service.GamificationPublicService;
import com.ladbrokescoral.oxygen.cms.api.service.GamificationService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({OneTwoFreeGamificationApi.class, GamificationPublicService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
class OneTwoFreeGamificationApiTest extends AbstractControllerTest {

  @MockBean private GamificationService gamificationService;
  @MockBean private GamificationRepository gamificationRepository;

  private List<Gamification> gamificationList;

  @BeforeEach
  public void setUp() throws Exception {
    Gamification entity =
        TestUtil.deserializeWithJackson(
            "controller/private_api/createGamification.json", Gamification.class);
    gamificationList = new ArrayList<>();
    gamificationList.add(entity);
  }

  @Test
  void findGamificationByBrand() throws Exception {
    given(gamificationRepository.findByBrand(anyString())).willReturn(gamificationList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/one-two-free/gamification")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }
}
