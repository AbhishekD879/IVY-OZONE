package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.ModuleRibbonTabArchiveRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetDataDto;
import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.repository.BybWidgetDataRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.BybWidgetRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.ModuleRibbonTabRepository;
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
      BybWidgetController.class,
      BybWidgetService.class,
      BybWidgetDataService.class,
      SportModuleService.class,
      ModuleRibbonTabService.class
    })
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
@MockBean(BrandService.class)
public class BybWidgetsTest extends AbstractControllerTest {

  @MockBean BybWidgetRepository bybWidgetRepository;
  @MockBean BybWidgetDataRepository bybWidgetDataRepository;

  @MockBean SportModuleRepository sportModuleRepository;

  @MockBean ModuleRibbonTabRepository moduleRibbonTabRepository;
  BybWidgetDto bybWidgetDto;
  ModelMapper mapper = new ModelMapper();

  @MockBean private BrandService brandService;
  @MockBean private DeleteEntityService deleteEntityService;
  @MockBean private HomeInplaySportService homeInplaySportService;

  @MockBean private SportModuleArchivalRepository sportModuleArchivalRepository;

  @MockBean ModuleRibbonTabArchiveRepository moduleRibbonTabArchivalRepository;
  @MockBean SegmentService segmentService;

  @Before
  public void init() {

    bybWidgetDto = createDto();
    BybWidget entity = mapper.map(bybWidgetDto, BybWidget.class);
    entity.setId("12121212121");
    entity.setCreatedBy("system");
    entity.setUpdatedAt(Instant.now());
    when(bybWidgetRepository.save(any())).thenReturn(entity);
    when(bybWidgetRepository.findById("12121212121")).thenReturn(Optional.of(entity));
    when(sportModuleRepository.findAllByBrandAndModuleTypeOrderBySortOrderAsc(
            "bma", SportModuleType.BYB_WIDGET))
        .thenReturn(createSportModule());

    when(moduleRibbonTabRepository.existsByBrandAndDirectiveNameAndBybVisbleTrue(
            "bma", "BuildYourBet"))
        .thenReturn(true);
  }

  private List<SportModule> createSportModule() {
    List<SportModule> modules = new ArrayList<>();
    modules.add(sportModule(0, SportModuleType.BYB_WIDGET));
    SportModule module = sportModule(16, SportModuleType.BYB_WIDGET);
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
    when(bybWidgetRepository.existsByBrand(Mockito.anyString())).thenReturn(false);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/byb-widget")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(bybWidgetDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createDuplicateRecord() throws Exception {
    when(bybWidgetRepository.existsByBrand(Mockito.anyString())).thenReturn(true);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/byb-widget")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(bybWidgetDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void createWithEmptyValues() throws Exception {
    bybWidgetDto = new BybWidgetDto();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/byb-widget")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(bybWidgetDto)))
        .andExpect(status().is4xxClientError());
  }

  // update
  @Test
  public void update() throws Exception {

    when(bybWidgetRepository.existsByBrand(Mockito.anyString())).thenReturn(true);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/byb-widget/12121212121")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(bybWidgetDto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateRecordWithEmptyId() throws Exception {
    when(bybWidgetRepository.existsByBrand(Mockito.anyString())).thenReturn(true);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/byb-widget/")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(bybWidgetDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void updateWithEmptyValues() throws Exception {
    bybWidgetDto = new BybWidgetDto();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/byb-widget/12121212121")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(bybWidgetDto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testReadByBrand() throws Exception {
    BybWidget entity = mapper.map(createDto(), BybWidget.class);
    List<BybWidget> list = new ArrayList<>();
    list.add(entity);
    when(bybWidgetRepository.findByBrand(Mockito.anyString())).thenReturn(list);
    BybWidgetData entityData = mapper.map(createData(), BybWidgetData.class);
    List<BybWidgetData> listData = new ArrayList<>();
    listData.add(entityData);
    when(bybWidgetDataRepository.findActiveAndFutureRecordsByBrandOrderBySortOrderAsc(
            Mockito.anyString(), any(), any()))
        .thenReturn(listData);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/byb-widget/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadByBrand_NotFound() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/byb-widget/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private BybWidgetDto createDto() {
    BybWidgetDto dto = new BybWidgetDto();
    dto.setTitle("BYB_WIDGET");
    dto.setShowAll(true);
    dto.setMarketCardVisibleSelections(10);
    dto.setBrand("bma");
    return dto;
  }

  private BybWidgetDataDto createData() {

    BybWidgetDataDto dto = new BybWidgetDataDto();
    dto.setTitle("data");
    dto.setDisplayFrom(Instant.now());
    dto.setDisplayTo(Instant.now());
    dto.setEventId("123");
    dto.setMarketId("123");
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
