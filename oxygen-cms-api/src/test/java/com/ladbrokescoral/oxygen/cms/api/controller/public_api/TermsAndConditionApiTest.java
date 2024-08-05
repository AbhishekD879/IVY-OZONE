package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.TermsAndCondition;
import com.ladbrokescoral.oxygen.cms.api.repository.TermsAndConditionRepository;
import com.ladbrokescoral.oxygen.cms.api.service.TermsAndConditionService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.TermsAndConditionPublicService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.Arrays;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {
      TermsAndConditionApi.class,
      TermsAndConditionPublicService.class,
      TermsAndConditionService.class,
      ModelMapper.class
    })
@AutoConfigureMockMvc(addFilters = false)
@Import(ModelMapperConfig.class)
public class TermsAndConditionApiTest extends AbstractControllerTest {
  @MockBean private TermsAndConditionRepository repository;
  private TermsAndCondition entity;

  @Before
  public void init() {
    entity = new TermsAndCondition();
    entity.setId("1");
    entity.setBrand("bma");
    entity.setText("5A-side Showdown");
    entity.setTitle("Test");
    entity.setUrl("test");
    given(repository.findAllByBrandOrderBySortOrderAsc(anyString()))
        .willReturn(Arrays.asList(entity));
  }

  @Test
  public void testFindTermsAndConditionByBrand() throws Exception {
    given(repository.findOneByBrand(anyString())).willReturn(getTermsAndCondition());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/termsandcondition")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(status().is2xxSuccessful());
  }

  private Optional<TermsAndCondition> getTermsAndCondition() {
    TermsAndCondition termsAndCondition = new TermsAndCondition();
    termsAndCondition.setId("2");
    termsAndCondition.setText("5A side showdown");
    termsAndCondition.setBrand("bma");
    termsAndCondition.setTitle("Test");
    termsAndCondition.setUrl("test");
    return Optional.of(termsAndCondition);
  }
}
