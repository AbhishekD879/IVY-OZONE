package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportModuleArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplayConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.RpgConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.repository.SportModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.DeleteEntityService;
import com.ladbrokescoral.oxygen.cms.api.service.HomeInplaySportService;
import com.ladbrokescoral.oxygen.cms.api.service.SportModuleService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.mockito.InjectMocks;
import org.mockito.Mockito;
import org.mockito.Spy;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({SportModules.class, SportModuleService.class})
@AutoConfigureMockMvc(addFilters = false)
@Import(ModelMapperConfig.class)
public class SportModuleTest extends AbstractControllerTest {

  @MockBean private SportModuleRepository repository;
  @MockBean private BrandService brandService;
  @MockBean private DeleteEntityService deleteEntityService;
  @MockBean private HomeInplaySportService homeInplaySportService;
  @InjectMocks private SportModuleService sportModuleService;
  @Spy private ModelMapper modelMapper;
  @MockBean private SportModuleArchivalRepository sportModuleArchivalRepository;

  private SportModule entity = new SportModule();

  private static SportModule createValidObject() {
    SportModule entity = new SportModule();
    entity.setId("100");
    entity.setBrand("bma");
    entity.setTitle("test title1");
    entity.setDisabled(false);
    entity.setSortOrder(1.0);
    entity.setSportId(4);
    entity.setModuleType(SportModuleType.QUICK_LINK);
    entity.setPublishedDevices(new ArrayList<>());
    HomeInplayConfig configuration = new HomeInplayConfig();
    entity.setInplayConfig(configuration);
    return entity;
  }

  @Before
  public void init() {

    entity = createValidObject();

    given(repository.findById(anyString())).willReturn(Optional.of(entity));
    given(repository.save(any(SportModule.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testCreateSportModuleError() throws Exception {
    SportModule dto = new SportModule();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-module")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateSportModulePublishedDevicesError() throws Exception {

    entity.setTitle("title");
    entity.setBrand("bma");
    entity.setModuleType(SportModuleType.FEATURED);
    entity.setPublishedDevices(null);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-module")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateSportModule() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-module")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateSportModuleRpgConfig() throws Exception {

    RpgConfig config = new RpgConfig();
    config.setGamesAmount(1);
    config.setTitle("RPG 1");
    config.setSeeMoreLink("https://www.google.com");

    entity.setInplayConfig(null);
    entity.setRpgConfig(config);
    entity.setPageId("0");
    entity.setModuleType(SportModuleType.RECENTLY_PLAYED_GAMES);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-module")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateSportModule() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/sport-module/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-module")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-module/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-module/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOneError() throws Exception {

    given(repository.findById(anyString())).willReturn(Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-module/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testDelete() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/sport-module/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());

    Mockito.verify(deleteEntityService, Mockito.times(1))
        .delete("4", "bma", PageType.sport, SportModuleType.QUICK_LINK);
  }

  @Test
  public void testOrder() throws Exception {
    OrderDto object =
        OrderDto.builder()
            .order(Arrays.asList(UUID.randomUUID().toString()))
            .id(UUID.randomUUID().toString())
            .build();
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-module/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateSportModuleBrandSecondscreen() throws Exception {

    entity.setSportId(16);
    entity.setBrand("secondscreen");
    entity.setModuleType(SportModuleType.RECENTLY_PLAYED_GAMES);
    entity.setTitle("test title1");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-module")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testInvalidTitle() throws Exception {

    entity.setTitle("test title1 $");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-module")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testPostModuleNullType() throws Exception {

    entity.setModuleType(null);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-module")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testPutModuleNullType() throws Exception {

    entity.setModuleType(null);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/sport-module/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testInvalidTitleAndSymbol() throws Exception {

    entity.setTitle("test title1 & test");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-module")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testReadOne_InplayModle_page_0() throws Exception {
    given(repository.findById("121212121212")).willReturn(createInplaySportModule("0"));

    when(homeInplaySportService.findByBrandAndSegmentName("bma", SegmentConstants.UNIVERSAL))
        .thenReturn(HomeInplaySportsTest.findUniversalRecords());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-module/121212121212")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOne_InplayModle_page_2() throws Exception {

    given(repository.findById("121212121212")).willReturn(createInplaySportModule("2"));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-module/121212121212")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  public static List<SportModule> createINplayModules() {
    List<SportModule> modules = new ArrayList<>();
    modules.add(createInplaySportModule("0").get());
    modules.add(createInplaySportModule("2").get());
    modules.add(createInplaySportModule("3").get());
    return modules;
  }

  public static Optional<SportModule> createInplaySportModule(String pageId) {
    SportModule entity = new SportModule();
    entity.setId("121212121212");
    entity.setBrand("bma");
    entity.setTitle("test title1");
    entity.setDisabled(false);
    entity.setSortOrder(1.0);
    entity.setSportId(0);
    entity.setPageId(pageId);
    entity.setModuleType(SportModuleType.INPLAY);
    entity.setPublishedDevices(new ArrayList<>());
    HomeInplayConfig configuration = new HomeInplayConfig();
    configuration.setMaxEventCount(2);
    entity.setInplayConfig(configuration);
    configuration.setHomeInplaySports(HomeInplaySportsTest.findAllEntites());
    return Optional.of(entity);
  }
}
