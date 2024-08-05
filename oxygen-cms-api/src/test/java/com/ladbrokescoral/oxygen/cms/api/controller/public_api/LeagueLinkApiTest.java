package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.hamcrest.Matchers.hasSize;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.LeagueLink;
import com.ladbrokescoral.oxygen.cms.api.repository.impl.LeagueLinkRepository;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.LeagueLinkService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
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
      LeagueLinkApi.class,
      LeagueLink.class,
      LeagueLinkService.class,
      LeagueLinkRepository.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class LeagueLinkApiTest {

  @MockBean private LeagueLinkService leagueLinkService;

  @MockBean private AuthenticationService authenticationService;

  @MockBean private UserService userService;

  @Autowired private MockMvc mockMvc;

  private List<LeagueLink> leagueLinks;

  @Before
  public void init() throws IOException {
    final ObjectMapper jsonMapper = new ObjectMapper();
    leagueLinks =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/public_api/leagueLinks.json"),
            new TypeReference<List<LeagueLink>>() {});
  }

  @Test
  public void testToGetArcProfilesByBrand() throws Exception {
    given(leagueLinkService.getEnabledLeagueLinksByCouponId(anyString(), anyInt()))
        .willReturn(leagueLinks);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/league-links/123")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$", hasSize(1)));
  }
}
