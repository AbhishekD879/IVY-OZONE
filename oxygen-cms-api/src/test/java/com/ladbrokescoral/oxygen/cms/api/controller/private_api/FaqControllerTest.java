package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Faq;
import com.ladbrokescoral.oxygen.cms.api.repository.FaqRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FaqService;
import java.util.Arrays;
import java.util.Optional;
import java.util.UUID;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {
      FaqController.class,
      FaqService.class,
    })
@AutoConfigureMockMvc(addFilters = false)
public class FaqControllerTest extends AbstractControllerTest {
  @MockBean private FaqRepository repository;
  private Faq entity;

  @Before
  public void init() {
    entity = createFaq();
    given(repository.findById(any(String.class))).willReturn(Optional.of(entity));
    given(repository.save(any(Faq.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testCreateFaq() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/faq")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/faq/brand/coral")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/faq/1").contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.id", is("1")))
        .andExpect(jsonPath("$.brand", is("coral")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOneError() throws Exception {
    given(repository.findById(any(String.class))).willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/faq/3").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound())
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdateFaq() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/faq/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/faq/1").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testOrderFaq() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/faq/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOrderDto())))
        .andExpect(status().is2xxSuccessful());
  }

  private static Faq createFaq() {
    Faq faq = new Faq();
    faq.setId("1");
    faq.setBrand("coral");
    faq.setQuestion("How to play 5A-side");
    faq.setAnswer("Please refer rules and entry");
    return faq;
  }

  private OrderDto createOrderDto() {
    OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("1", "2", "3"))
            .id(UUID.randomUUID().toString())
            .build();
    return orderDto;
  }
}
