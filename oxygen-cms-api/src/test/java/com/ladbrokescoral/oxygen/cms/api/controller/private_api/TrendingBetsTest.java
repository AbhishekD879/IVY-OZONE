package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.TrendingBetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.TrendingBet;
import com.ladbrokescoral.oxygen.cms.api.repository.TrendingBetRepository;
import com.ladbrokescoral.oxygen.cms.api.service.TrendingBetService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
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

@WebMvcTest(value = {TrendingBets.class, TrendingBetService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class TrendingBetsTest extends AbstractControllerTest {

  @MockBean private TrendingBetRepository repository;

  private TrendingBet entity;
  private TrendingBetDto dto;
  ModelMapper mapper = new ModelMapper();

  @Before
  public void setUp() throws Exception {
    dto = createTrendingBetDto("62cd9ce3fa2d927e6d9c18ad");
    entity = mapper.map(dto, TrendingBet.class);
    when(repository.save(any())).thenReturn(entity);
    when(repository.findById(any())).thenReturn(Optional.of(entity));
  }

  @Test
  public void testCreateTrendingBet() throws Exception {
    when(repository.findTrendingBetByBrandAndType(anyString(), anyString()))
        .thenReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/trending-bet")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateTrendingBetWhenTypeNotContains() throws Exception {
    dto = createTrendingBetDto("62cd9ce3fa2d927e6d9c18ad");
    dto.setType("type");
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/trending-bet")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateTrendingBetWhenEntityExists() throws Exception {
    when(repository.findTrendingBetByBrandAndType(anyString(), anyString()))
        .thenReturn(Optional.of(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/trending-bet")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdateTrendingBetWhenIdExists() throws Exception {
    String id = "62cd9ce3fa2d927e6d9c18ad";
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/trending-bet/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateTrendingBetWhenIdNotExists() throws Exception {
    String id = "118000004558668682";
    when(repository.findById(id)).thenReturn(Optional.empty());
    dto.setId(id);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/trending-bet/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testDeleteById() throws Exception {
    String id = "62cd9ce3fa2d927e6d9c18ad";
    when(repository.findById(any())).thenReturn(Optional.of(entity), Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/trending-bet/" + id)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetByBrand() throws Exception {
    when(repository.findTrendingBetByBrandAndType(anyString(), anyString()))
        .thenReturn(Optional.of(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/trending-bet/brand/bma")
                .param("type", "bet-slip")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void testGetByBrandWhenEmpty() throws Exception {
    when(repository.findTrendingBetByBrandAndType(anyString(), anyString()))
        .thenReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/trending-bet/bet-receipt/brand/bma")
                .param("type", "bet-slip")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  private static TrendingBetDto createTrendingBetDto(String id) {
    TrendingBetDto dto = new TrendingBetDto();
    dto.setId(id);
    dto.setType("bet-slip");
    dto.setBrand("bma");
    dto.setActive(true);
    dto.setDisplayForAllUsers(true);
    dto.setMostBackedIn("24Hr");
    dto.setEventStartsIn("2Hr");
    dto.setIsTimeInHours(false);
    dto.setBetRefreshInterval(20);
    return dto;
  }
}
