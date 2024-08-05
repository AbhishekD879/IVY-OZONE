package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Faq;
import com.ladbrokescoral.oxygen.cms.api.repository.FaqRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FaqService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FaqPublicService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.Arrays;
import java.util.Collections;
import java.util.Optional;
import org.hamcrest.Matchers;
import org.junit.Before;
import org.junit.Test;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {FaqApi.class, FaqPublicService.class, FaqService.class, ModelMapper.class})
@AutoConfigureMockMvc(addFilters = false)
@Import(ModelMapperConfig.class)
public class FaqApiTest extends AbstractControllerTest {
  @MockBean private FaqRepository repository;
  private Faq entity;

  @Before
  public void init() {
    entity = new Faq();
    entity.setId("1");
    entity.setQuestion("How to play 5A-side");
    entity.setAnswer("Please Refer our Entry Rules");
    entity.setBrand("bma");
    given(repository.findAllByBrandOrderBySortOrderAsc(anyString()))
        .willReturn(Arrays.asList(entity));
  }

  @Test
  public void testByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/faq").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testByBrandForEmpty() throws Exception {
    given(repository.findAllByBrandOrderBySortOrderAsc(anyString()))
        .willReturn(Collections.emptyList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/faq").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(status().isNoContent());
  }

  @Test
  public void testFindByIdForException() throws Exception {
    given(repository.findById(anyString())).willReturn(Optional.empty());
    this.mockMvc
        .perform(MockMvcRequestBuilders.get("/cms/api/faq/1"))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testFindById() throws Exception {
    given(repository.findById("2")).willReturn(getContest());
    this.mockMvc
        .perform(MockMvcRequestBuilders.get("/cms/api/faq/2"))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.id", Matchers.is("2")))
        .andExpect(jsonPath("$.brand", Matchers.is("bma")));
  }

  private Optional<Faq> getContest() {
    Faq faq = new Faq();
    faq.setId("2");
    entity.setQuestion("How to play 5A-side");
    entity.setAnswer("Please Refer our Entry Rules");
    faq.setBrand("bma");
    return Optional.of(faq);
  }
}
