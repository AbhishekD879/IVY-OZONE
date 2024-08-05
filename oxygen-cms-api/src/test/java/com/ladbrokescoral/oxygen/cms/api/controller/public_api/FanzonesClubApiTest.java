package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesClubRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesClubService;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(value = {FanzonesClubService.class, FanzonesClubApi.class})
@AutoConfigureMockMvc(addFilters = false)
public class FanzonesClubApiTest extends AbstractControllerTest {

  private FanzoneClub fanzoneClub;

  @MockBean FanzonesClubRepository fanzonesClubRepository;

  @Before
  public void init() {
    fanzoneClub = createFanzoneClub();
    given(fanzonesClubRepository.findAllFanzonesByBrand(anyString()))
        .willReturn(Optional.of(Arrays.asList(fanzoneClub)));
  }

  @Test
  public void testToReadAllFanzones() throws Exception {
    given(fanzonesClubRepository.findAllFanzonesByBrand(anyString()))
        .willReturn(Optional.of(Arrays.asList(fanzoneClub)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/fanzone-club")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private static FanzoneClub createFanzoneClub() {
    FanzoneClub entity = new FanzoneClub();
    entity.setId("123");
    entity.setBrand("ladbrokes");
    entity.setActive(true);
    entity.setBannerLink("www.asset.com");
    entity.setTitle("club");
    entity.setDescription("welcome to clubs");
    entity.setValidityPeriodStart(Instant.now().plus(5, ChronoUnit.DAYS));
    entity.setValidityPeriodEnd(Instant.now().plus(6, ChronoUnit.DAYS));
    return entity;
  }
}
