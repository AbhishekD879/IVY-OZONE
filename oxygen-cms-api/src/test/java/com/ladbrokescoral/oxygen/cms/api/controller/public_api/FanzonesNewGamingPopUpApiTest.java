package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewGamingPopUp;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesNewGamingPopUpRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewGamingPopUpService;
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
@WebMvcTest(value = {FanzonesNewGamingPopUpService.class, FanzonesNewGamingPopUpApi.class})
@AutoConfigureMockMvc(addFilters = false)
public class FanzonesNewGamingPopUpApiTest extends AbstractControllerTest {

  private FanzoneNewGamingPopUp fanzoneNewGamingPopUp;

  @MockBean FanzonesNewGamingPopUpRepository fanzonesNewGamingPopUpRepository;

  @Before
  public void init() {
    fanzoneNewGamingPopUp = createFanzoneNewGamingPopUp();
    given(fanzonesNewGamingPopUpRepository.findAllByBrand(anyString()))
        .willReturn(Optional.of(fanzoneNewGamingPopUp));
  }

  @Test
  public void testToReadFanzoneNewGamingPopUp() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/fanzone-new-gaming-pop-up")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private FanzoneNewGamingPopUp createFanzoneNewGamingPopUp() {
    FanzoneNewGamingPopUp entity = new FanzoneNewGamingPopUp();
    entity.setBrand("ladbrokes");
    entity.setTitle("Fanzone New Gaming Pop Up");
    entity.setDescription("Fanzone New gaming pop up description here");
    entity.setCloseCTA("close");
    entity.setPlayCTA("play");
    return entity;
  }
}
