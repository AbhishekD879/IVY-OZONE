package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetDataDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeMarketDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybWidgetData;
import com.ladbrokescoral.oxygen.cms.api.repository.BybWidgetDataRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.BybWidgetDataService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Instant;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

@WebMvcTest(value = {BybWidgetDataController.class, BybWidgetDataService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
@MockBean(BrandService.class)
public class BybWidgetDataTest extends AbstractControllerTest {

  @MockBean BybWidgetDataRepository bybWidgetDataRepository;
  @MockBean SiteServeService siteServeService;

  BybWidgetDataDto bybWidgetDataDto;
  ModelMapper mapper = new ModelMapper();

  @Before
  public void init() {
    bybWidgetDataDto = createDto();
    BybWidgetData entity = mapper.map(bybWidgetDataDto, BybWidgetData.class);
    entity.setId("12121212121");
    entity.setCreatedBy("system");
    entity.setUpdatedAt(Instant.now());
    when(bybWidgetDataRepository.save(any())).thenReturn(entity);
    when(bybWidgetDataRepository.findById("12121212121")).thenReturn(Optional.of(entity));
    when(siteServeService.getMarketById("bma", "1234567"))
        .thenReturn(Optional.of(createSiteServeMarketDto("1234567", "da", "123")));
  }

  private SiteServeMarketDto createSiteServeMarketDto(
      String marketId, String name, String eventId) {

    SiteServeMarketDto dto = new SiteServeMarketDto();
    dto.setId(marketId);
    dto.setName(name);
    dto.setEventId(eventId);
    return dto;
  }
  // create

  @Test
  public void create() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/byb-widget-data")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(bybWidgetDataDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createInvalidMarketIdRecord() throws Exception {
    BybWidgetDataDto createDto = createDto();
    createDto.setMarketId("123");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/byb-widget-data")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void createWithEmptyValues() throws Exception {
    bybWidgetDataDto = new BybWidgetDataDto();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/byb-widget-data")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(bybWidgetDataDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void createWithExsistingMarket() throws Exception {
    BybWidgetData entity = mapper.map(bybWidgetDataDto, BybWidgetData.class);
    entity.setId("12331");
    when(bybWidgetDataRepository.findByMarketId(any())).thenReturn(Optional.of(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/byb-widget-data")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(bybWidgetDataDto)))
        .andExpect(status().is4xxClientError());
  }

  // update
  @Test
  public void update() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/byb-widget-data/12121212121")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(bybWidgetDataDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateSameEntityWithExsistingMarket() throws Exception {
    BybWidgetData entity = mapper.map(bybWidgetDataDto, BybWidgetData.class);
    entity.setId("12121212121");
    when(bybWidgetDataRepository.findByMarketId(any())).thenReturn(Optional.of(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/byb-widget-data/12121212121")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(bybWidgetDataDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateWithExsistingMarket() throws Exception {
    BybWidgetData entity = mapper.map(bybWidgetDataDto, BybWidgetData.class);
    entity.setId("123");
    when(bybWidgetDataRepository.findByMarketId(any())).thenReturn(Optional.of(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/byb-widget-data/12121212121")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(bybWidgetDataDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void updateInValidMarketId() throws Exception {
    BybWidgetDataDto updateDto = createDto();
    updateDto.setMarketId("123");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/byb-widget-data/12121212121")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void updateRecordWithEmptyId() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/byb-widget-data/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(bybWidgetDataDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void updateWithEmptyValues() throws Exception {
    bybWidgetDataDto = new BybWidgetDataDto();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/byb-widget-data/12121212121")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(bybWidgetDataDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testReadByBrand() throws Exception {

    BybWidgetData entityData = mapper.map(createDto(), BybWidgetData.class);
    List<BybWidgetData> listData = new ArrayList<>();
    listData.add(entityData);
    when(bybWidgetDataRepository.findByBrand(Mockito.anyString())).thenReturn(listData);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/byb-widget-data/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.length()").value(1));
  }

  @Test
  public void testReadActiveRecordsByBrand() throws Exception {

    BybWidgetData entityData = mapper.map(createDto(), BybWidgetData.class);
    List<BybWidgetData> listData = new ArrayList<>();
    listData.add(entityData);
    when(bybWidgetDataRepository.findActiveAndFutureRecordsByBrandOrderBySortOrderAsc(
            Mockito.anyString(), any(), any()))
        .thenReturn(listData);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/byb-widget-data/brand/bma/status")
                .param("active", String.valueOf(true))
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.length()").value(1));
  }

  @Test
  public void testReadActiveRecordsByBrand_NotFound() throws Exception {
    when(bybWidgetDataRepository.findActiveAndFutureRecordsByBrandOrderBySortOrderAsc(
            Mockito.anyString(), any(), any()))
        .thenReturn(new ArrayList<>());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/byb-widget-data/brand/bma/status")
                .param("active", String.valueOf(true))
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.length()").value(0));
  }

  @Test
  public void testReadExpireRecordsByBrand() throws Exception {

    BybWidgetData entityData = mapper.map(createDto(), BybWidgetData.class);
    List<BybWidgetData> listData = new ArrayList<>();
    listData.add(entityData);
    when(bybWidgetDataRepository.findExpiredRecordsByBrandOrderBySortOrderAsc(
            Mockito.anyString(), any(), any()))
        .thenReturn(listData);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/byb-widget-data/brand/bma/status")
                .param("active", String.valueOf(false))
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.length()").value(1));
    ;
  }

  @Test
  public void testReadByBrand_NotFound() throws Exception {
    when(bybWidgetDataRepository.findByBrand(Mockito.anyString(), any()))
        .thenReturn(new ArrayList<>());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/byb-widget-data/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.length()").value(0));
  }

  @Test
  public void testOrderMenu() throws Exception {
    BybWidgetData entity = mapper.map(bybWidgetDataDto, BybWidgetData.class);
    entity.setId("1212121");
    when(bybWidgetDataRepository.findById("1")).thenReturn(Optional.of(entity));
    when(bybWidgetDataRepository.findById("2")).thenReturn(Optional.of(entity));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/byb-widget-data/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOrderDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testdelete() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/byb-widget-data/12121212121")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private OrderDto createOrderDto() {
    OrderDto orderDto =
        OrderDto.builder().order(Arrays.asList("1", "2")).segmentName("segment1").id("2").build();
    return orderDto;
  }

  private BybWidgetDataDto createDto() {

    BybWidgetDataDto dto = new BybWidgetDataDto();
    dto.setTitle("data");
    dto.setDisplayFrom(Instant.now());
    dto.setDisplayTo(Instant.now());
    dto.setEventId("123");
    dto.setMarketId("1234567");
    dto.setBrand("bma");
    dto.setLocations(createLocations());

    return dto;
  }

  private List<String> createLocations() {
    List<String> locs = new ArrayList<>();
    locs.add("home");
    locs.add("football");
    return locs;
  }
}
