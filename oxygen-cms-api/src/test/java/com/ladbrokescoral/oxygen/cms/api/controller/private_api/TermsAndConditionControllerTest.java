package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.TermsAndCondition;
import com.ladbrokescoral.oxygen.cms.api.repository.TermsAndConditionRepository;
import com.ladbrokescoral.oxygen.cms.api.service.TermsAndConditionService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.SpyBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {TermsAndConditionController.class, TermsAndConditionService.class, ModelMapper.class})
@AutoConfigureMockMvc(addFilters = false)
@Import(ModelMapperConfig.class)
public class TermsAndConditionControllerTest extends AbstractControllerTest {

  @SpyBean private TermsAndConditionService service;
  @MockBean private TermsAndConditionRepository repository;
  private TermsAndCondition entity;
  private String BRAND = "bma";

  @Before
  public void init() {
    entity = new TermsAndCondition();
    entity.setId("98789987");
    entity.setBrand(BRAND);
    entity.setText("5A-side Showdown");
    entity.setTitle("Test");
    entity.setUrl("test");

    doReturn(entity)
        .when(service)
        .update(any(TermsAndCondition.class), any(TermsAndCondition.class));
    doReturn(entity).when(service).save(any(TermsAndCondition.class));
    doReturn(Optional.of(entity)).when(service).findOne(any(String.class));
    doReturn(Optional.of(entity)).when(repository).findOneByBrand(BRAND);

    entity = createTermsAndCondition("1", true);
    given(repository.findById(any(String.class))).willReturn(Optional.of(entity));
    given(repository.save(any(TermsAndCondition.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testCreateTermsAndCondition() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/termsandcondition")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateTermsAndConditionError() throws Exception {
    TermsAndCondition dto = new TermsAndCondition(); // empty object
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/termsandcondition")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError())
        .andExpect(status().isBadRequest());
  }

  @Test
  public void testUpdateTermsAndCondition() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/termsandcondition/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOneByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/termsandcondition/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/termsandcondition/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private static TermsAndCondition createTermsAndCondition(String id, boolean value) {
    TermsAndCondition tAndc = new TermsAndCondition();
    tAndc.setId(id);
    tAndc.setBrand("coral");
    tAndc.setText("5A-side Showdown");
    tAndc.setTitle("Test");
    tAndc.setUrl("test");
    return tAndc;
  }
}
