package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSeason;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesNewSeasonRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewSeasonService;
import java.util.Optional;
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
@WebMvcTest(value = {FanzonesNewSeasonService.class, FanzonesNewSeasonApiController.class})
@AutoConfigureMockMvc(addFilters = false)
public class FanzonesNewSeasonApiTest extends AbstractControllerTest {

  private FanzoneNewSeason fanzoneNewSeason;

  @MockBean FanzonesNewSeasonRepository fanzonesNewSeasonRepository;

  @Before
  public void init() {
    fanzoneNewSeason = createFanzoneNewSeason();
    given(fanzonesNewSeasonRepository.findAllByBrand(anyString()))
        .willReturn(Optional.of(fanzoneNewSeason));
  }

  @Test
  public void testToReadFanzoneNewSeason() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/fanzone-new-season")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private static FanzoneNewSeason createFanzoneNewSeason() {
    FanzoneNewSeason entity = new FanzoneNewSeason();
    entity.setId("123");
    entity.setBrand("ladbrokes");
    entity.setFzNewSeasonHeading("Fanzone New Season");
    entity.setFzNewSeasonTitle("Fanzone New Season Pop Up Title");
    entity.setFzNewSeasonDescription("Fanzone New Season Pop Up Descriptionn");
    entity.setFzNewSeasonBgImageDesktop("Fanzone_Syc2");
    entity.setFzNewSeasonBgImageMobile("Fanzone_Syc2");
    entity.setFzNewSeasonBadgeMobile("Fanzone_Syc2");
    entity.setFzNewSeasonBadgeDesktop("Fanzone_Syc2");
    entity.setFzNewSeasonLightningMobile("Fanzone_Syc2");
    entity.setFzNewSeasonLightningDesktop("Fanzone_Syc2");
    return entity;
  }
}
