package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.BPMDto;
import com.ladbrokescoral.oxygen.cms.api.dto.BetPackFilterDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackFilter;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackEnablerFilterRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackEnablerFilterService;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceService;
import java.io.IOException;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Spy;
import org.springframework.beans.BeanUtils;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      BetPackMarketPlaceFilterController.class,
      BetPackFilter.class,
      BetPackEnablerFilterService.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class BetPackMarketPlaceFilterControllerTest extends AbstractControllerTest {
  public static final String CORAL = "coral";
  private BetPackFilter betPackFilterEntity = new BetPackFilter();
  private BetPackFilterDto betPackFilterDto;
  private BetPackFilter betPackFilter;
  private BetPackEntity betPackEntity;

  @MockBean BetPackEnablerFilterService betPackEnablerFilterService;
  @MockBean BetPackMarketPlaceService betPackMarketPlaceService;
  @MockBean BetPackEnablerFilterRepository betPackEnablerFilterRepository;
  @Spy BPMDto bpmDto;

  @Before
  public void init() throws IOException {
    final ObjectMapper jsonMapper = new ObjectMapper();
    betPackFilterDto =
        TestUtil.deserializeWithJackson(
            "controller/private_api/betpack-enabler/BetpackFilter.json", BetPackFilterDto.class);
    jsonMapper.enable(DeserializationFeature.ACCEPT_EMPTY_STRING_AS_NULL_OBJECT);
    betPackFilter =
        TestUtil.deserializeWithJackson(
            "controller/private_api/betpack-enabler/BetpackFilter.json", BetPackFilter.class);
    betPackEntity =
        TestUtil.deserializeWithJackson(
            "controller/private_api/betpack-enabler/Betpack.json", BetPackEntity.class);

    BeanUtils.copyProperties(betPackFilterDto, betPackFilterEntity);
  }

  @Test
  public void testCreateBetPackFilter() throws Exception {
    given(betPackEnablerFilterService.prepareModelBeforeSave(any()))
        .willReturn(betPackFilterEntity);
    given(
            betPackEnablerFilterService.checkActiveFilterLimit(
                anyString(), any(BetPackFilterDto.class)))
        .willReturn(betPackFilterEntity);
    given(betPackEnablerFilterService.save(any(BetPackFilter.class)))
        .willReturn(betPackFilterEntity);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bet-pack/filter")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackFilterDto)))
        .andExpect(status().isCreated());
  }

  @Test
  public void testGetAllBetPackFilters() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/bet-pack/filters")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetBetPackFilterByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/bet-pack/filters/brand/coral")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testOrder() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bet-pack/filter/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOrderDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetBetPackFilterById() throws Exception {
    given(betPackEnablerFilterService.findOne(anyString()))
        .willReturn(Optional.of(betPackFilterEntity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/bet-pack/filter/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateBetPackFilterNameFalse() throws Exception {
    List<BetPackEntity> betPackEntityList = new ArrayList<>();
    betPackEntity.setFilterList(Arrays.asList("abc"));
    betPackEntityList.add(betPackEntity);
    BPMDto bpm = new BPMDto();
    bpm.setFilterAssociated(true);
    given(betPackEnablerFilterService.getFilterStatus(anyString(), any(), any())).willReturn(bpm);
    given(betPackEnablerFilterService.findOne(anyString()))
        .willReturn(Optional.of(betPackFilterEntity));
    given(
            betPackEnablerFilterService.checkActiveFilterLimit(
                anyString(), any(BetPackFilterDto.class)))
        .willReturn(betPackFilterEntity);
    given(betPackEnablerFilterService.prepareModelBeforeSave(any()))
        .willReturn(betPackFilterEntity);
    given(betPackMarketPlaceService.findAllBetPackEntities()).willReturn(betPackEntityList);
    given(betPackEnablerFilterService.update(any(), any())).willReturn(betPackFilterEntity);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/bet-pack/filter/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackFilter)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateFilterAssociationTrue() throws Exception {
    List<BetPackEntity> betPackEntityList = new ArrayList<>();
    BPMDto bpm = new BPMDto();
    bpm.setFilterAssociated(true);
    given(betPackEnablerFilterService.getFilterStatus(anyString(), any(), any())).willReturn(bpm);
    betPackEntity.setFilterList(Arrays.asList("abc"));
    betPackEntityList.add(betPackEntity);
    given(betPackEnablerFilterService.findOne(anyString()))
        .willReturn(Optional.of(betPackFilterEntity));
    given(
            betPackEnablerFilterService.checkActiveFilterLimit(
                anyString(), any(BetPackFilterDto.class)))
        .willReturn(betPackFilterEntity);
    given(betPackEnablerFilterService.prepareModelBeforeSave(any()))
        .willReturn(betPackFilterEntity);
    given(betPackMarketPlaceService.findAllBetPackEntities()).willReturn(betPackEntityList);
    given(betPackEnablerFilterService.update(any(), any())).willReturn(betPackFilterEntity);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/bet-pack/filter/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackFilter)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateBetPackFilterMatchFilterName() throws Exception {
    List<BetPackEntity> betPackEntityList = new ArrayList<>();
    betPackEntityList.add(betPackEntity);

    BPMDto bpm = new BPMDto();
    given(betPackEnablerFilterService.getFilterStatus(anyString(), any(), any())).willReturn(bpm);
    given(betPackEnablerFilterService.findOne(anyString()))
        .willReturn(Optional.of(betPackFilterEntity));
    given(betPackEnablerFilterService.prepareModelBeforeSave(any()))
        .willReturn(betPackFilterEntity);
    given(betPackEnablerFilterService.checkActiveFilterLimit(anyString(), any()))
        .willReturn(betPackFilterEntity);
    given(betPackMarketPlaceService.findAllBetPackEntities()).willReturn(betPackEntityList);
    given(betPackEnablerFilterService.update(any(), any())).willReturn(betPackFilterEntity);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/bet-pack/filter/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackFilter)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteByFilterNameFalse() throws Exception {
    List<BetPackEntity> betPackEntityList = Arrays.asList(betPackEntity);
    given(betPackMarketPlaceService.findAllBetPackEntities()).willReturn(betPackEntityList);

    given(betPackEnablerFilterService.getFilterStatus(anyString(), any(), any()))
        .willReturn(new BPMDto());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-pack/filter/today")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteByFilterNameIsFilterAssociated() throws Exception {
    BPMDto bpm = new BPMDto();
    // when(bpmDto.isFilterAssociated()).thenReturn(true);
    // betPackEnablerFilterService= mock(BetPackEnablerFilterService.class,CALLS_REAL_METHODS);
    bpm.setFilterAssociated(true);
    // betPackEnablerFilterService.getFilterStatus("today",bpm, Arrays.asList(betPackEntity));
    given(betPackEnablerFilterService.getFilterStatus(anyString(), any(), any())).willReturn(bpm);
    List<BetPackEntity> betPackEntityList = Arrays.asList(betPackEntity);
    given(betPackMarketPlaceService.findAllBetPackEntities()).willReturn(betPackEntityList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-pack/filter/today")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteByFilterNameEqIgnoreCase_EndDateAfter() throws Exception {
    given(betPackEnablerFilterService.getFilterStatus(anyString(), any(), any()))
        .willReturn(new BPMDto());
    Instant now = Instant.now().plus(30, ChronoUnit.DAYS);
    betPackEntity.setBetPackEndDate(now);
    List<BetPackEntity> betPackEntityList = Arrays.asList(betPackEntity);
    given(betPackMarketPlaceService.findAllBetPackEntities()).willReturn(betPackEntityList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-pack/filter/Today")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteByFilterNameNonEqIgnoreCase_EndDateBefore() throws Exception {
    Instant now = Instant.now().minus(30, ChronoUnit.DAYS);
    betPackEntity.setBetPackEndDate(now);
    List<BetPackEntity> betPackEntityList = Arrays.asList(betPackEntity);
    given(betPackEnablerFilterService.getFilterStatus(anyString(), any(), any()))
        .willReturn(new BPMDto());
    given(betPackMarketPlaceService.findAllBetPackEntities()).willReturn(betPackEntityList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-pack/filter/Cricket")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteByFilterNameWithEmptyList() throws Exception {
    List<BetPackEntity> betPackEntityList = new ArrayList<>();
    given(betPackEnablerFilterService.getFilterStatus(anyString(), any(), any()))
        .willReturn(new BPMDto());
    given(betPackMarketPlaceService.findAllBetPackEntities()).willReturn(betPackEntityList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-pack/filter/6299d8fd4fccfd73f6d8d456")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteByFilterNameDeleteStatusZero() throws Exception {
    List<BetPackEntity> betPackEntityList = new ArrayList<>();
    given(betPackEnablerFilterService.getFilterStatus(anyString(), any(), any()))
        .willReturn(new BPMDto());
    given(betPackMarketPlaceService.findAllBetPackEntities()).willReturn(betPackEntityList);
    given(betPackEnablerFilterService.deleteByFilterName(anyString())).willReturn(0L);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-pack/filter/6299d8fd4fccfd73f6d8d456")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteByFilterNameDeleteStatusOne() throws Exception {
    List<BetPackEntity> betPackEntityList = new ArrayList<>();
    given(betPackEnablerFilterService.getFilterStatus(anyString(), any(), any()))
        .willReturn(new BPMDto());
    given(betPackMarketPlaceService.findAllBetPackEntities()).willReturn(betPackEntityList);
    given(betPackEnablerFilterService.deleteByFilterName(anyString())).willReturn(1L);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-pack/filter/6299d8fd4fccfd73f6d8d456")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
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
