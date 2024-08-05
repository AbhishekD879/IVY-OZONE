package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.hamcrest.Matchers.is;
import static org.mockito.ArgumentMatchers.any;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.ModuleRibbonTabArchiveRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SegmentArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.ModuleRibbonTabArchive;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ModuleRibbonTab;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import com.ladbrokescoral.oxygen.cms.api.repository.ModuleRibbonTabRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ModuleRibbonTabService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentedModuleSerive;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import com.ladbrokescoral.oxygen.cms.util.WithMockCustomUser;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.mockito.Mockito;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({
  ModuleRibbonTabs.class,
  ModuleRibbonTabService.class,
  SegmentService.class,
})
@AutoConfigureMockMvc(addFilters = false)
@Import(ModelMapperConfig.class)
@ContextConfiguration
public class ModuleRibbonTabsTest extends AbstractControllerTest {

  @MockBean ModuleRibbonTabRepository repository;
  private ModuleRibbonTab entity;
  @MockBean ModuleRibbonTabArchiveRepository moduleRibbonTabArchiveRepository;
  @MockBean private SegmentRepository segmentRepository;
  @MockBean private SegmentedModuleSerive segmentedModuleSerive;
  @MockBean private SegmentArchivalRepository segmentArchivalRepository;

  @Before
  public void init() {

    entity = create();

    given(repository.save(any(ModuleRibbonTab.class))).will(AdditionalAnswers.returnsFirstArg());

    entity = createModuleRibbonTab("1", false, "universal");
    given(repository.findById(any(String.class))).willReturn(Optional.of(entity));
    given(repository.findUniversalRecordsByBrand("bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .willReturn(getModuleRibbonTabList());

    given(repository.findAllByBrandAndSegmentName("bma", Arrays.asList("segment1")))
        .willReturn(getModuleRibbonTabListForUniversalFalse());

    given(
            repository.findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
                "bma",
                Arrays.asList("segment1"),
                Arrays.asList("1", "2"),
                SortableService.SORT_BY_SORT_ORDER_ASC))
        .willReturn(getModuleRibbonTabList());

    given(repository.findByBrand("bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .willReturn(getModuleRibbonTabList());

    given(repository.save(any(ModuleRibbonTab.class))).will(AdditionalAnswers.returnsFirstArg());

    given(moduleRibbonTabArchiveRepository.save(any(ModuleRibbonTabArchive.class)))
        .will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testUpdateMarket() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/module-ribbon-tab/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/module-ribbon-tab/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.id", is("1")))
        .andExpect(jsonPath("$.brand", is("bma")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOneError() throws Exception {
    given(repository.findById(any(String.class))).willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/module-ribbon-tab/3")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound())
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testReadAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/module-ribbon-tab")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrand() throws Exception {
    given(
            repository.findUniversalRecordAndInclusiveNotNullAndBrand(
                "bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .willReturn(getModuleRibbonTabList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/module-ribbon-tab/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.size()", is(1)));
  }

  @Test
  public void testReadAllByBrandAndSegmentForUniversalSegment() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/module-ribbon-tab/brand/bma/segment/universal")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.size()", is(1)))
        .andExpect(jsonPath("$[0].universalSegment", is(true)));
  }

  @Test
  public void testReadAllByBrandAndSegmentForNonUniversalSegment() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/module-ribbon-tab/brand/bma/segment/segment1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.size()", is(3)))
        .andExpect(jsonPath("$[0].universalSegment", is(false)));
  }

  @Test
  public void testDeleteOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/module-ribbon-tab/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteOneNotFind() throws Exception {
    ModuleRibbonTab moduleRibbonTab = createModuleRibbonTab("2", false, "universal");
    Mockito.when(repository.findById("2"))
        .thenReturn(Optional.of(moduleRibbonTab), Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/module-ribbon-tab/2")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateModuleRibbonTab() throws Exception {
    entity = createModuleRibbonTab("2", false, "universal");
    given(repository.save(any(ModuleRibbonTab.class))).willReturn(entity);
    given(repository.findByBrand(anyString())).willReturn(getModuleRibbonTabList());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/module-ribbon-tab")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().isCreated());
  }

  @Test
  public void testUpdateModuleRibbonTab() throws Exception {
    entity = createModuleRibbonTab("2", false, "segment1");
    given(repository.findById("2")).willReturn(Optional.of(entity));
    given(repository.findByBrand(anyString())).willReturn(getModuleRibbonTabList());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/module-ribbon-tab/2")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateWithsSameId() throws Exception {
    given(repository.findById("1")).willReturn(Optional.of(entity));
    given(repository.findByBrand(anyString())).willReturn(getModuleRibbonTabList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/module-ribbon-tab/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testOrderMenu() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/module-ribbon-tab/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOrderDto())))
        .andExpect(status().is2xxSuccessful());
  }

  public static ModuleRibbonTab createModuleRibbonTab(
      String id, boolean value, String segmentName) {
    ModuleRibbonTab ModuleRibbonTab = new ModuleRibbonTab();
    ModuleRibbonTab.setTargetUri("ModuleRibbonTab");
    ModuleRibbonTab.setTitle("ModuleRibbonTab test");
    ModuleRibbonTab.setSegmentReferences(getSegmentReference(segmentName));
    ModuleRibbonTab.setSortOrder(5 + Math.random());
    ModuleRibbonTab.setId(id);
    ModuleRibbonTab.setUniversalSegment(value);
    ModuleRibbonTab.setShowTabOn("onTab");
    ModuleRibbonTab.setInternalId("1");
    ModuleRibbonTab.setBrand("bma");
    ModuleRibbonTab.setHubIndex(16);
    ModuleRibbonTab.setTitle("test title1");
    ModuleRibbonTab.setUrl("http://test.com");
    Calendar instance = Calendar.getInstance();
    instance.set(Calendar.YEAR, 2200);
    ModuleRibbonTab.setDisplayTo(instance.toInstant());
    ModuleRibbonTab.setDisplayFrom(Instant.now());
    ModuleRibbonTab.setDirectiveName("eventhub");

    return ModuleRibbonTab;
  }

  private static List<SegmentReference> getSegmentReference(String segmentName) {
    List<SegmentReference> segmentReferences = new ArrayList<>();
    segmentReferences.add(getSegmentReference(segmentName, "10", 1));
    segmentReferences.add(getSegmentReference(segmentName, "10", 2));
    return segmentReferences;
  }

  private static SegmentReference getSegmentReference(
      String segmentName, String pageRefId, double sortOrder) {
    return SegmentReference.builder()
        .segmentName(segmentName)
        .id("1")
        .sortOrder(sortOrder)
        .pageRefId(pageRefId)
        .build();
  }

  private OrderDto createOrderDto() {
    OrderDto orderDto =
        OrderDto.builder()
            .order(Arrays.asList("1", "2", "3"))
            .segmentName("segment1")
            .id(UUID.randomUUID().toString())
            .build();
    return orderDto;
  }

  private static List<ModuleRibbonTab> getModuleRibbonTabList() {
    List<ModuleRibbonTab> ModuleRibbonTabList = new ArrayList<>();
    ModuleRibbonTabList.add(createModuleRibbonTab("1", true, "universal"));
    return ModuleRibbonTabList;
  }

  private List<ModuleRibbonTab> getModuleRibbonTabListForUniversalFalse() {
    List<ModuleRibbonTab> moduleRibbonTabs = new ArrayList<>();
    moduleRibbonTabs.add(createModuleRibbonTab("1", false, "segment1"));
    moduleRibbonTabs.add(createModuleRibbonTab("2", false, "segment1"));
    return moduleRibbonTabs;
  }

  @Test
  public void testCreateNullHubIndex() throws Exception {

    entity.setHubIndex(null);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/module-ribbon-tab")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateInvalidDateRange() throws Exception {

    Calendar instance = Calendar.getInstance();
    instance.set(Calendar.YEAR, 2200);
    entity.setDisplayFrom(instance.toInstant());
    entity.setDisplayTo(instance.toInstant());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/module-ribbon-tab")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  public ModuleRibbonTab create() {
    ModuleRibbonTab entity = new ModuleRibbonTab();
    entity.setShowTabOn("onTab");
    entity.setInternalId("1");
    entity.setBrand("bma");
    entity.setHubIndex(16);
    entity.setTitle("test title1");
    entity.setUrl("http://test.com");
    Calendar instance = Calendar.getInstance();
    instance.set(Calendar.YEAR, 2200);
    entity.setDisplayTo(instance.toInstant());
    entity.setDisplayFrom(Instant.now());
    entity.setDirectiveName("eventhub");
    return entity;
  }
}
