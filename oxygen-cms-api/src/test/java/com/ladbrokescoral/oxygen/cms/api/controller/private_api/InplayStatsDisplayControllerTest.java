package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.InplayStatsDisplay;
import com.ladbrokescoral.oxygen.cms.api.repository.InplayStatsDisplayRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.InplayStatsDisplayService;
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

@WebMvcTest(value = {InplayStatsDisplayController.class, InplayStatsDisplayService.class})
@AutoConfigureMockMvc(addFilters = false)
@MockBeans({@MockBean(BrandService.class)})
public class InplayStatsDisplayControllerTest extends AbstractControllerTest {

  @MockBean private InplayStatsDisplayRepository repository;

  private InplayStatsDisplay inplayStatsDisplay;

  @Before
  public void init() {
    inplayStatsDisplay = buildInplayStatsDisplay();
    given(this.repository.findById(Mockito.anyString()))
        .willReturn(Optional.of(inplayStatsDisplay));
    given(this.repository.save(Mockito.any(InplayStatsDisplay.class)))
        .willAnswer(AdditionalAnswers.returnsFirstArg());
    given(this.repository.findByBrand(Mockito.anyString()))
        .willReturn(Collections.singletonList(inplayStatsDisplay));
    given(this.repository.findAll()).willReturn(Collections.singletonList(inplayStatsDisplay));
  }

  @Test
  public void testSaveEntity() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/inplay-stats-display")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(inplayStatsDisplay)))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  public void testReadById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/inplay-stats-display/1122")
                .accept(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  public void testReadByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/inplay-stats-display/brand/bma")
                .accept(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  public void testReadAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/inplay-stats-display")
                .accept(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  public void testUpdateEntity() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/inplay-stats-display/1122")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(inplayStatsDisplay)))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  public void testDeleteEntity() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/inplay-stats-display/1122")
                .accept(MediaType.APPLICATION_JSON))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  @Test
  public void testOrdering() throws Exception {
    OrderDto orderDto = OrderDto.builder().id("11").order(Arrays.asList("1", "2", "3")).build();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/inplay-stats-display/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(orderDto)))
        .andExpect(MockMvcResultMatchers.status().is2xxSuccessful());
  }

  private InplayStatsDisplay buildInplayStatsDisplay() {
    InplayStatsDisplay dto = new InplayStatsDisplay();
    dto.setId("1122");
    dto.setBrand("bma");
    dto.setCategoryId(16);
    return dto;
  }
}
