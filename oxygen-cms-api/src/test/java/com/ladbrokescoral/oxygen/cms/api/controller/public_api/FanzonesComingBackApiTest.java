package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneComingBack;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesComingBackRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesSycRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesComingBackService;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(value = {FanzonesComingBackService.class, FanzonesComingBackApiController.class})
@AutoConfigureMockMvc(addFilters = false)
public class FanzonesComingBackApiTest extends AbstractControllerTest {

  private FanzoneComingBack fanzoneComingBack;

  @MockBean FanzonesComingBackRepository fanzonesComingBackRepository;

  @Autowired FanzonesComingBackService fanzonesComingBackService;
  @MockBean FanzonesSycRepository fanzonesSycRepository;

  @Before
  public void init() {
    fanzonesComingBackService =
        new FanzonesComingBackService(fanzonesComingBackRepository, fanzonesSycRepository);
    fanzoneComingBack = createFanzoneComingBack();
    given(fanzonesComingBackRepository.findAllByBrand(anyString()))
        .willReturn(Optional.of(fanzoneComingBack));
  }

  @Test
  public void testToReadFanzoneComingBack() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/fanzone-coming-back")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private static FanzoneComingBack createFanzoneComingBack() {
    FanzoneComingBack entity = new FanzoneComingBack();
    entity.setId("123");
    entity.setBrand("ladbrokes");
    entity.setFzComingBackHeading("Fanzone Coming Back");
    entity.setFzComingBackDescription("Fanzone Coming Back Pop Up Description");
    entity.setFzComingBackTitle("Fanzone Coming Back Pop Up Title");
    entity.setFzComingBackOKCTA("OK CTA");
    entity.setFzComingBackDisplayFromDays("No of days before season starts");
    entity.setFzComingBackBadgeUrlDesktop("Fanzone_Syc2");
    entity.setFzComingBackBadgeUrlMobile("Fanzone_Syc2");
    entity.setFzComingBackPopupDisplay(true);
    return entity;
  }
}
