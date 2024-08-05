package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.PopularAccaWidgetDataDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PopularAccaWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.repository.PopularAccaWidgetDataRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.PopularAccaWidgetRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.Random;
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

@WebMvcTest(
    value = {
      PopularAccaWidgetController.class,
      PopularAccaWidgetService.class,
      PopularAccaWidgetDataService.class,
      SportModuleService.class
    })
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
@MockBean(BrandService.class)
public class PopularAccaWidgetControllerTest extends AbstractControllerTest {

  @MockBean PopularAccaWidgetRepository popularAccaWidgetRepository;
  @MockBean PopularAccaWidgetDataRepository popularAccaWidgetDataRepository;

  @MockBean SportModuleRepository sportModuleRepository;

  @MockBean SportCategoryService sportCategoryService;

  PopularAccaWidgetDto popularAccaWidgetDto;
  ModelMapper mapper = new ModelMapper();

  @MockBean private DeleteEntityService deleteEntityService;
  @MockBean private HomeInplaySportService homeInplaySportService;
  @MockBean private SportModuleArchivalRepository sportModuleArchivalRepository;

  @Before
  @Override
  public void init() {

    popularAccaWidgetDto = createDto();
    PopularAccaWidget entity = mapper.map(popularAccaWidgetDto, PopularAccaWidget.class);
    entity.setId("12121212121");
    entity.setCreatedBy("system");
    entity.setUpdatedAt(Instant.now());
    when(popularAccaWidgetRepository.save(any())).thenReturn(entity);
    when(popularAccaWidgetRepository.findById("12121212121")).thenReturn(Optional.of(entity));
    when(sportModuleRepository.findAllByBrandAndModuleTypeOrderBySortOrderAsc(
            "bma", SportModuleType.POPULAR_ACCA))
        .thenReturn(createSportModule());
  }

  private List<SportModule> createSportModule() {
    List<SportModule> modules = new ArrayList<>();
    modules.add(sportModule(0, SportModuleType.POPULAR_ACCA));
    SportModule module = sportModule(16, SportModuleType.POPULAR_ACCA);
    module.setDisabled(false);
    modules.add(module);
    return modules;
  }

  private SportModule sportModule(Integer sportId, SportModuleType moduleType) {
    SportModule module = new SportModule();
    module.setSportId(sportId);
    module.setPageId(String.valueOf(sportId));
    module.setModuleType(moduleType);
    module.setId(String.valueOf(sportId) + new Random().nextInt());
    module.setPageType(PageType.sport);
    return module;
  }
  // create

  @Test
  public void create() throws Exception {
    when(popularAccaWidgetRepository.existsByBrand(Mockito.anyString())).thenReturn(false);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/popular-acca-widget")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(popularAccaWidgetDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createDuplicateRecord() throws Exception {
    when(popularAccaWidgetRepository.existsByBrand(Mockito.anyString())).thenReturn(true);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/popular-acca-widget")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(popularAccaWidgetDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void createWithEmptyValues() throws Exception {
    popularAccaWidgetDto = new PopularAccaWidgetDto();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/popular-acca-widget")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(popularAccaWidgetDto)))
        .andExpect(status().is4xxClientError());
  }

  // update
  @Test
  public void update() throws Exception {

    when(popularAccaWidgetRepository.existsByBrand(Mockito.anyString())).thenReturn(true);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/popular-acca-widget/12121212121")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(popularAccaWidgetDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateRecordWithEmptyId() throws Exception {
    when(popularAccaWidgetRepository.existsByBrand(Mockito.anyString())).thenReturn(true);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/popular-acca-widget")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(popularAccaWidgetDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void updateWithEmptyValues() throws Exception {
    popularAccaWidgetDto = new PopularAccaWidgetDto();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/popular-acca-widget/12121212121")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(popularAccaWidgetDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testReadByBrand() throws Exception {
    PopularAccaWidget entity = mapper.map(createDto(), PopularAccaWidget.class);
    List<PopularAccaWidget> list = new ArrayList<>();
    list.add(entity);
    when(popularAccaWidgetRepository.findByBrand(Mockito.anyString())).thenReturn(list);
    PopularAccaWidgetData entityData = mapper.map(createData(), PopularAccaWidgetData.class);
    List<PopularAccaWidgetData> listData = new ArrayList<>();
    listData.add(entityData);
    when(popularAccaWidgetDataRepository.findActiveAndFutureRecordsByBrandOrderBySortOrderAsc(
            Mockito.anyString(), any(), any()))
        .thenReturn(listData);
    when(sportCategoryService.findOneByCategoryId(any(), any()))
        .thenReturn(Optional.ofNullable(new SportCategory()));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/popular-acca-widget/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadByBrand_NotFound() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/popular-acca-widget/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private PopularAccaWidgetDto createDto() {
    PopularAccaWidgetDto dto = new PopularAccaWidgetDto();
    dto.setTitle("POPULAR_ACCA");
    dto.setBrand("bma");
    return dto;
  }

  private PopularAccaWidgetDataDto createData() {

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
