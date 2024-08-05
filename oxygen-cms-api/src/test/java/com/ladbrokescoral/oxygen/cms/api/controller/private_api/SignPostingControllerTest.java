package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.SignPosting;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.repository.SignPostingRepository;
import com.ladbrokescoral.oxygen.cms.api.service.SignPostingService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.AdditionalAnswers;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.annotation.CreatedBy;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      SignPostingController.class,
      SignPostingRepository.class,
      SignPostingService.class,
      SignPosting.class,
      UserService.class,
      User.class,
      CreatedBy.class,
      Util.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class SignPostingControllerTest extends AbstractControllerTest {
  @MockBean private SignPosting signPosting;
  @MockBean private SignPostingRepository signPostingRepository;
  @Autowired private SignPostingService signPostingService;

  @Before
  public void init() {
    given(signPostingRepository.save(any(SignPosting.class)))
        .will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void readAllTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/signposting")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void readTest() throws Exception {
    SignPosting signPosting = new SignPosting();
    signPosting.setId("616e7a3c54409d7519879827");
    signPosting.setBrand("ladbrokes");
    given(signPostingService.findOne(anyString())).willReturn(Optional.of(signPosting));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/signposting/732648732")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void readByBrandTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/signposting/brand/ladbrokes")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createTest() throws Exception {

    SignPosting signPosting = new SignPosting();
    signPosting.setId("616e7a3c54409d7519879827");
    signPosting.setBrand("ladbrokes");
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/signposting")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(signPosting)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateTest() throws Exception {

    SignPosting signPosting = new SignPosting();
    signPosting.setId("616e7a3c54409d7519879827");
    signPosting.setBrand("ladbrokes");
    given(signPostingService.findOne(anyString())).willReturn(Optional.of(signPosting));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/signposting/123")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(signPosting)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteTest() throws Exception {

    SignPosting signPosting = new SignPosting();
    signPosting.setId("616e7a3c54409d7519879827");
    signPosting.setBrand("ladbrokes");
    given(signPostingService.findOne(anyString())).willReturn(Optional.of(signPosting));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/signposting/123")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}
