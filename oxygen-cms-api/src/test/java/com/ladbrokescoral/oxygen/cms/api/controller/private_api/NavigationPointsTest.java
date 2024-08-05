package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.NavigationPointArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SegmentArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.NavigationPointArchive;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.AliasModuleNamesDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYModuleEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import com.ladbrokescoral.oxygen.cms.api.repository.NavigationPointRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import com.ladbrokescoral.oxygen.cms.util.WithMockCustomUser;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {NavigationPoints.class, NavigationPointService.class, SegmentService.class})
@AutoConfigureMockMvc(addFilters = false)
@MockBean({
  BrandService.class,
  ImageEntityService.class,
  SvgEntityService.class,
  ImageConfig.ImagePath.class,
  SegmentedModuleSerive.class,
  AutomaticUpdateService.class
})
@Import(ModelMapperConfig.class)
public class NavigationPointsTest extends AbstractControllerTest {

  @MockBean private SegmentArchivalRepository segmentArchivalRepository;

  @MockBean private NavigationPointRepository repository;
  @MockBean private NavigationPointArchivalRepository NavigationPointArchivalRepository;
  @MockBean private SegmentRepository segmentRepository;

  @MockBean private RGYModuleService rgyModuleService;

  @MockBean private RGYConfigUploadService rgyConfigUploadService;

  private NavigationPoint entity;

  private RGYModuleEntity rgyModuleEntity;

  @Before
  public void init() {
    entity = createNavigationPoint("1", false, "universal");
    rgyModuleEntity = createRgyModuleEntity();
    given(repository.findById(any(String.class))).willReturn(Optional.of(entity));
    given(repository.findUniversalRecordsByBrand("bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .willReturn(getNavigationPointList());

    given(repository.findAllByBrandAndSegmentName("bma", Arrays.asList("segment1")))
        .willReturn(getNavigationPointListForUniversalFalse());

    given(
            repository.findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
                "bma",
                Arrays.asList("segment1"),
                Arrays.asList("1", "2"),
                SortableService.SORT_BY_SORT_ORDER_ASC))
        .willReturn(getNavigationPointList());

    given(repository.findByBrand("bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .willReturn(getNavigationPointList());

    given(repository.save(any(NavigationPoint.class))).will(AdditionalAnswers.returnsFirstArg());

    given(NavigationPointArchivalRepository.save(any(NavigationPointArchive.class)))
        .will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testCreateMarket() throws Exception {
    entity.setId(null);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/navigation-points")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateInvalidSegmentName() throws Exception {
    NavigationPoint entity = createNavigationPoint("123", false, "CSP_Test-1$");
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/navigation-points")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreatevalidSegmentName() throws Exception {
    NavigationPoint entity = createNavigationPoint("123", false, "CSP_Test-1");
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/navigation-points")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateMarket() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/navigation-points/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/navigation-points/1")
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
            MockMvcRequestBuilders.get("/v1/api/navigation-points/3")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound())
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testReadAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/navigation-points")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrand() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/navigation-points/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.size()", is(1)));
  }

  @Test
  public void testReadAllByBrandAndSegmentForUniversalSegment() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/navigation-points/brand/bma/segment/universal")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.size()", is(1)))
        .andExpect(jsonPath("$[0].universalSegment", is(true)));
  }

  @Test
  public void testReadAllByBrandAndSegmentForNonUniversalSegment() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/navigation-points/brand/bma/segment/segment1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.size()", is(3)))
        .andExpect(jsonPath("$[0].universalSegment", is(false)));
  }

  @Test
  public void testDeleteOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/navigation-points/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateNavigationPoint() throws Exception {
    entity = createNavigationPoint("2", false, "universal");
    given(repository.save(any(NavigationPoint.class))).willReturn(entity);
    given(repository.findByBrand(anyString())).willReturn(getNavigationPointList());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/navigation-points")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().isCreated());
  }

  @Test
  public void testUpdateNavigationPoint() throws Exception {
    entity = createNavigationPoint("2", false, "segment1");
    given(repository.findById("2")).willReturn(Optional.of(entity));
    given(repository.findByBrand(anyString())).willReturn(getNavigationPointList());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/navigation-points/2")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateNavigationPointWithAliasModuleName() throws Exception {
    NavigationPoint existing = createNavigationPoint("11", false, "universal");
    existing.setTitle("hello");
    NavigationPoint updated = createNavigationPoint("11", false, "universal");
    updated.setTitle("supreme");

    given(this.repository.findById(anyString())).willReturn(Optional.of(existing));
    given(this.rgyModuleService.readByBrand(anyString()))
        .willReturn(Collections.singletonList(rgyModuleEntity));
    given(this.rgyConfigUploadService.uploadToS3(anyString())).willReturn(Collections.emptyList());
    given(this.repository.save(any(NavigationPoint.class)))
        .willAnswer(AdditionalAnswers.returnsFirstArg());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/navigation-points/11")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updated)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateWithsSameId() throws Exception {
    given(repository.findById("1")).willReturn(Optional.of(entity));
    given(repository.findByBrand(anyString())).willReturn(getNavigationPointList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/navigation-points/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testOrderMenu() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/navigation-points/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createOrderDto())))
        .andExpect(status().is2xxSuccessful());
  }

  private static NavigationPoint createNavigationPoint(
      String id, boolean value, String segmentName) {
    NavigationPoint navigationPoint = new NavigationPoint();
    navigationPoint.setBrand("bma");
    navigationPoint.setTargetUri("my-navigation");
    navigationPoint.setTitle("navigation points test");
    navigationPoint.setDescription("This is navigation points test file");
    navigationPoint.setValidityPeriodStart(Instant.now());
    navigationPoint.setValidityPeriodEnd(Instant.now().plus(10, ChronoUnit.DAYS));
    navigationPoint.setSegmentReferences(getSegmentReference(segmentName));
    navigationPoint.setInclusionList(new ArrayList<>(Arrays.asList(segmentName)));
    navigationPoint.setId(id);
    navigationPoint.setUniversalSegment(value);
    navigationPoint.setCtaAlignment("center alignment");
    navigationPoint.setShortDescription("test");
    navigationPoint.setThemes("test");

    return navigationPoint;
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

  private static List<NavigationPoint> getNavigationPointList() {
    List<NavigationPoint> NavigationPointList = new ArrayList<>();
    NavigationPointList.add(createNavigationPoint("1", true, "universal"));
    return NavigationPointList;
  }

  private List<NavigationPoint> getNavigationPointListForUniversalFalse() {
    List<NavigationPoint> NavigationPoints = new ArrayList<>();
    NavigationPoints.add(createNavigationPoint("1", false, "segment1"));
    NavigationPoints.add(createNavigationPoint("2", false, "segment1"));
    return NavigationPoints;
  }

  private RGYModuleEntity createRgyModuleEntity() {
    RGYModuleEntity rgyModuleEntity = new RGYModuleEntity();
    rgyModuleEntity.setAliasModules(Collections.singletonList(aliasModuleNamesDto("11", "hello")));
    rgyModuleEntity.setBrand("bma");
    return rgyModuleEntity;
  }

  private AliasModuleNamesDto aliasModuleNamesDto(String id, String title) {
    AliasModuleNamesDto aliasModuleNamesDto = new AliasModuleNamesDto();
    aliasModuleNamesDto.setId(id);
    aliasModuleNamesDto.setTitle(title);
    return aliasModuleNamesDto;
  }
}
