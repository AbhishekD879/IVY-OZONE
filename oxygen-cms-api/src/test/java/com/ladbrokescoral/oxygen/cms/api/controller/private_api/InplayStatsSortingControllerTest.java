package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.InplayStatsSorting;
import com.ladbrokescoral.oxygen.cms.api.repository.InplayStatsSortingRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.InplayStatsSortingService;
import java.util.Arrays;
import java.util.Collections;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.mockito.Mockito;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.MockBeans;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

@WebMvcTest(value = {InplayStatsSortingController.class, InplayStatsSortingService.class})
@MockBeans(@MockBean(BrandService.class))
@AutoConfigureMockMvc(addFilters = false)
public class InplayStatsSortingControllerTest extends AbstractControllerTest {

  @MockBean private InplayStatsSortingRepository repository;

  private InplayStatsSorting inplayStatsSorting;

  @Before
  public void init() {
    inplayStatsSorting = buildInplayStatsSorting();
    given(this.repository.findById(Mockito.anyString()))
        .willReturn(Optional.of(inplayStatsSorting));
    given(this.repository.save(Mockito.any(InplayStatsSorting.class)))
        .willAnswer(AdditionalAnswers.returnsFirstArg());
    given(this.repository.findByBrand(Mockito.anyString()))
        .willReturn(Collections.singletonList(inplayStatsSorting));
    given(this.repository.findAll()).willReturn(Collections.singletonList(inplayStatsSorting));
  }

  @Test
  public void testSaveEntity() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/inplay-stats-sorting")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(inplayStatsSorting)))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  public void testReadById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/inplay-stats-sorting/1122")
                .accept(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  public void testReadByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/inplay-stats-sorting/brand/bma")
                .accept(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  public void testReadAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/inplay-stats-sorting")
                .accept(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  public void testUpdateEntity() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/inplay-stats-sorting/1122")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(inplayStatsSorting)))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  public void testDeleteEntity() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/inplay-stats-sorting/1122")
                .accept(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  public void testOrdering() throws Exception {
    OrderDto orderDto = OrderDto.builder().id("11").order(Arrays.asList("1", "2", "3")).build();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/inplay-stats-sorting/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(orderDto)))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  private InplayStatsSorting buildInplayStatsSorting() {
    InplayStatsSorting dto = new InplayStatsSorting();
    dto.setId("1122");
    dto.setBrand("bma");
    dto.setCategoryId(16);
    return dto;
  }
}
