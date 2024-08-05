package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesOptinEmailRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesSycRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesOptinEmailService;
import java.util.*;
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
@WebMvcTest(value = {FanzonesOptinEmailService.class, FanzoneOptinEmailApi.class})
@AutoConfigureMockMvc(addFilters = false)
public class FanzoneOptinEmailApiTest extends AbstractControllerTest {

  private FanzoneOptinEmail fanzoneOptinEmail;

  @MockBean FanzonesOptinEmailRepository fanzonesOptinEmailRepository;

  @Autowired FanzonesOptinEmailService fanzonesOptinEmailService;
  @MockBean FanzonesSycRepository fanzonesSycRepository;

  @Before
  public void init() {
    fanzonesOptinEmailService =
        new FanzonesOptinEmailService(fanzonesOptinEmailRepository, fanzonesSycRepository);
    fanzoneOptinEmail = createFanzoneOptinEmail();
    given(fanzonesOptinEmailRepository.findFanzoneOptinEmailByBrand(anyString()))
        .willReturn(Optional.of(fanzoneOptinEmail));
  }

  @Test
  public void testToReadFanzoneOptinEmail() throws Exception {
    given(fanzonesOptinEmailRepository.findFanzoneOptinEmailByBrand(anyString()))
        .willReturn(Optional.of(fanzoneOptinEmail));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/fanzones/fanzone-optin-email")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private static FanzoneOptinEmail createFanzoneOptinEmail() {
    FanzoneOptinEmail entity = new FanzoneOptinEmail();
    entity.setId("616e7a3c54409d7519879827");
    entity.setBrand("ladbrokes");
    entity.setFanzoneEmailPopupDescription("Abc");
    entity.setFanzoneEmailPopupDontShowThisAgain("abc");
    entity.setFanzoneEmailPopupOptIn("abc");
    entity.setFanzoneEmailPopupRemindMeLater("abc");
    entity.setFanzoneEmailPopupTitle("abc");
    return entity;
  }
}
