package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.SignPosting;
import com.ladbrokescoral.oxygen.cms.api.service.SignPostingService;
import java.util.Arrays;
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
@WebMvcTest(value = {SignPostingService.class, SignPostingApi.class})
@AutoConfigureMockMvc(addFilters = false)
public class SignPostingApiTest extends AbstractControllerTest {

  private SignPosting signPosting;

  @MockBean SignPostingService service;

  @Before
  public void init() {
    signPosting = createSignPosting();
    given(service.findAllByBrand(anyString())).willReturn(Arrays.asList(signPosting));
  }

  @Test
  public void findByBrandTest() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/signposting")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void findByBrandEmptyResultsTest() throws Exception {

    SignPosting signPosting = new SignPosting();

    given(service.findAllByBrand(anyString())).willReturn(Arrays.asList());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/signposting")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private SignPosting createSignPosting() {
    SignPosting signPosting = new SignPosting();
    signPosting.setId("616e7a3c54409d7519879827");
    signPosting.setBrand("ladbrokes");
    return signPosting;
  }
}
