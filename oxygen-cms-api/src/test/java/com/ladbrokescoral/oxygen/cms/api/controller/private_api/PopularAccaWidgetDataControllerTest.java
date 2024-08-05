package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PopularAccaWidgetDataDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventValidationResultDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PopularAccaType;
import com.ladbrokescoral.oxygen.cms.api.entity.PopularAccaWidgetData;
import com.ladbrokescoral.oxygen.cms.api.repository.PopularAccaWidgetDataRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.PopularAccaWidgetDataService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
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

@WebMvcTest(value = {PopularAccaWidgetDataController.class, PopularAccaWidgetDataService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
@MockBean(BrandService.class)
public class PopularAccaWidgetDataControllerTest extends AbstractControllerTest {

  @MockBean PopularAccaWidgetDataRepository popularAccaWidgetDataRepository;

  @MockBean SiteServeService siteServeService;

  PopularAccaWidgetDataDto popularAccaWidgetDataDto;
  ModelMapper mapper = new ModelMapper();

  @Before
  @Override
  public void init() {
    popularAccaWidgetDataDto = createDto();
    PopularAccaWidgetData entity =
        mapper.map(popularAccaWidgetDataDto, PopularAccaWidgetData.class);
    entity.setId("12121212121");
    entity.setCreatedBy("system");
    entity.setUpdatedAt(Instant.now());
    when(popularAccaWidgetDataRepository.save(any())).thenReturn(entity);
    when(popularAccaWidgetDataRepository.findById("12121212121")).thenReturn(Optional.of(entity));
  }

  @Test
  public void testRead() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/popular-acca-widget-data/12121212121")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  // create
  @Test
  public void create() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/popular-acca-widget-data")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(popularAccaWidgetDataDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createWithTypeIds() throws Exception {
    PopularAccaWidgetDataDto dto = createDto();
    dto.setAccaIdsType(PopularAccaType.TYPEID.getValue());
    dto.setListOfIds(Arrays.asList("1"));
    when(siteServeService.validateEventsByTypeId(any(), any(), anyBoolean()))
        .thenReturn(new SiteServeEventValidationResultDto());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/popular-acca-widget-data")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createWithEventIds() throws Exception {
    PopularAccaWidgetDataDto dto = createDto();
    dto.setAccaIdsType(PopularAccaType.EVENT.getValue());
    dto.setListOfIds(Arrays.asList("1"));
    SiteServeEventValidationResultDto resultDto = new SiteServeEventValidationResultDto();
    resultDto.setInvalid(Arrays.asList("1"));
    when(siteServeService.validateAndGetEventsById(any(), any(), anyBoolean()))
        .thenReturn(resultDto);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/popular-acca-widget-data")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void createWithOutcomeIds() throws Exception {
    PopularAccaWidgetDataDto dto = createDto();
    dto.setAccaIdsType(PopularAccaType.SELECTION.getValue());
    dto.setListOfIds(Arrays.asList("1"));
    when(siteServeService.validateEventsByOutcomeId(any(), any()))
        .thenReturn(new SiteServeEventValidationResultDto());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/popular-acca-widget-data")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createWithEmptyOutcomeIds() throws Exception {
    PopularAccaWidgetDataDto dto = createDto();
    dto.setAccaIdsType(PopularAccaType.SELECTION.getValue());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/popular-acca-widget-data")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void createWithEmptyValues() throws Exception {
    popularAccaWidgetDataDto = new PopularAccaWidgetDataDto();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/popular-acca-widget-data")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(popularAccaWidgetDataDto)))
        .andExpect(status().is4xxClientError());
  }

  // update
  @Test
  public void update() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/popular-acca-widget-data/12121212121")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(popularAccaWidgetDataDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateRecordWithEmptyId() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/popular-acca-widget-data/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(popularAccaWidgetDataDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void updateWithEmptyValues() throws Exception {
    popularAccaWidgetDataDto = new PopularAccaWidgetDataDto();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/popular-acca-widget-data/12121212121")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(popularAccaWidgetDataDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testReadByBrand() throws Exception {

    PopularAccaWidgetData entityData = mapper.map(createDto(), PopularAccaWidgetData.class);
    List<PopularAccaWidgetData> listData = new ArrayList<>();
    listData.add(entityData);
    when(popularAccaWidgetDataRepository.findByBrand(Mockito.anyString())).thenReturn(listData);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/popular-acca-widget-data/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.length()").value(1));
  }

  @Test
  public void testReadActiveRecordsByBrand() throws Exception {

    PopularAccaWidgetData entityData = mapper.map(createDto(), PopularAccaWidgetData.class);
    List<PopularAccaWidgetData> listData = new ArrayList<>();
    listData.add(entityData);
    when(popularAccaWidgetDataRepository.findActiveAndFutureRecordsByBrandOrderBySortOrderAsc(
            Mockito.anyString(), any(), any()))
        .thenReturn(listData);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/popular-acca-widget-data/brand/bma/status")
                .param("active", String.valueOf(true))
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.length()").value(1));
  }

  @Test
  public void testReadActiveRecordsByBrand_NotFound() throws Exception {
    when(popularAccaWidgetDataRepository.findActiveAndFutureRecordsByBrandOrderBySortOrderAsc(
            Mockito.anyString(), any(), any()))
        .thenReturn(new ArrayList<>());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/popular-acca-widget-data/brand/bma/status")
                .param("active", String.valueOf(true))
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.length()").value(0));
  }

  @Test
  public void testReadExpireRecordsByBrand() throws Exception {

    PopularAccaWidgetData entityData = mapper.map(createDto(), PopularAccaWidgetData.class);
    List<PopularAccaWidgetData> listData = new ArrayList<>();
    listData.add(entityData);
    when(popularAccaWidgetDataRepository.findExpiredRecordsByBrandOrderBySortOrderAsc(
            Mockito.anyString(), any(), any()))
        .thenReturn(listData);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/popular-acca-widget-data/brand/bma/status")
                .param("active", String.valueOf(false))
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.length()").value(1));
  }

  @Test
  public void testReadByBrand_NotFound() throws Exception {
    when(popularAccaWidgetDataRepository.findByBrand(Mockito.anyString(), any()))
        .thenReturn(new ArrayList<>());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/popular-acca-widget-data/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.length()").value(0));
  }

  @Test
  public void testOrderMenu() throws Exception {
    PopularAccaWidgetData entity =
        mapper.map(popularAccaWidgetDataDto, PopularAccaWidgetData.class);
    entity.setId("1212121");
    when(popularAccaWidgetDataRepository.findById("1")).thenReturn(Optional.of(entity));
    when(popularAccaWidgetDataRepository.findById("2")).thenReturn(Optional.of(entity));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/popular-acca-widget-data/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOrderDto())))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testdelete() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/popular-acca-widget-data/12121212121")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private OrderDto createOrderDto() {
    return OrderDto.builder()
        .order(Arrays.asList("1", "2"))
        .segmentName("segment1")
        .id("2")
        .build();
  }

  private PopularAccaWidgetDataDto createDto() {

    PopularAccaWidgetDataDto dto = new PopularAccaWidgetDataDto();
    dto.setTitle("data");
    dto.setDisplayFrom(Instant.now());
    dto.setDisplayTo(Instant.now());
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
