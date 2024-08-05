package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSignposting;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesNewSignpostingRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewSignpostingService;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
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
@WebMvcTest(value = {FanzonesNewSignpostingService.class, FanzonesNewSignpostingApi.class})
@AutoConfigureMockMvc(addFilters = false)
public class FanzonesNewSignpostingApiTest extends AbstractControllerTest {

  private FanzoneNewSignposting fanzoneNewSignposting;

  @MockBean FanzonesNewSignpostingRepository fanzonesNewSignpostingRepository;

  @Before
  public void init() {
    fanzoneNewSignposting = createFanzoneNewSignposting();
    given(fanzonesNewSignpostingRepository.findAllByBrand(anyString()))
        .willReturn(Optional.of(fanzoneNewSignposting));
  }

  @Test
  public void testToReadFanzoneNewSignposting() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/fanzone-new-signposting")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private static FanzoneNewSignposting createFanzoneNewSignposting() {
    FanzoneNewSignposting entity = new FanzoneNewSignposting();
    entity.setId("123");
    entity.setBrand("ladbrokes");
    entity.setActive(true);
    entity.setNewSignPostingIcon("new");
    entity.setStartDate(Instant.now().plus(5, ChronoUnit.DAYS));
    entity.setEndDate(Instant.now().plus(6, ChronoUnit.DAYS));
    return entity;
  }
}
