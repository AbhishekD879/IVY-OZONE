package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SegmentArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SurfaceBetArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.ActiveSurfaceBetDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentReference;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SurfaceBetMongoRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SurfaceBetRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SurfaceBetTitleRepository;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import com.ladbrokescoral.oxygen.cms.util.WithMockCustomUser;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.time.Duration;
import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.assertj.core.util.Lists;
import org.hamcrest.Matchers;
import org.junit.Before;
import org.junit.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.AdditionalAnswers;
import org.mockito.Mockito;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.web.util.NestedServletException;

@WebMvcTest({
  SurfaceBets.class,
  SurfaceBetService.class,
  SegmentService.class,
  ModelMapper.class,
  SportPagesOrderingService.class,
  SurfaceBetTitleService.class
})
@AutoConfigureMockMvc(addFilters = false)
@MockBean(BrandService.class)
@Import(ModelMapperConfig.class)
public class SurfaceBetsTest extends AbstractControllerTest {

  private static final int EXISTS_SELECTION_ID = 907016395;
  private static final String TEST_PAGE_ID = "test";
  private static final String TEST_SB_ID = "1";

  @MockBean private SurfaceBetRepository repository;
  @MockBean private SegmentArchivalRepository segmentArchivalRepository;

  @MockBean private SvgEntityService<SurfaceBet> svgEntityService;
  @MockBean private SiteServerApi siteServerApi;
  @MockBean private SiteServeApiProvider siteServeApiProvider;

  @MockBean private SurfaceBetArchivalRepository surfaceBetArchivalRepository;
  @MockBean private SegmentRepository segmentRepository;
  @MockBean private CompetitionModuleService moduleService;
  @MockBean private SurfaceBetMongoRepository surfaceBetMongoRepository;

  @MockBean private SurfaceBetTitleRepository surfaceBetTitleRepository;

  private SurfaceBet entity;

  @Before
  public void init() {

    entity = createValidSurfaceBet();

    given(repository.findById(anyString())).willReturn(Optional.of(entity));
    given(repository.save(any(SurfaceBet.class))).will(AdditionalAnswers.returnsFirstArg());

    given(siteServeApiProvider.api("bma")).willReturn(siteServerApi);
    given(siteServerApi.getEventToOutcomeForOutcome(anyList(), any(SimpleFilter.class), anyList()))
        .willReturn(Optional.of(new ArrayList<>()));
  }

  @Test
  @WithMockCustomUser
  public void testCreateSurfaceBet_OK() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @ParameterizedTest
  @WithMockCustomUser
  @CsvSource({
    "true, '0'",
    "false, '0'",
    "false, '1'",
  })
  void testUpdateActiveSB(boolean value, String refId) throws Exception {
    ActiveSurfaceBetDto activeSurfaceBetDto =
        new ActiveSurfaceBetDto("2324", false, value, true, true);
    SurfaceBet existingSB = createValidSurfaceBet();
    existingSB.setId("2324");
    existingSB.setDisabled(true);
    existingSB.setHighlightsTabOn(value);
    existingSB.setEdpOn(false);
    existingSB.setDisplayOnDesktop(true);

    Set<Relation> set = new HashSet<>();
    set.add(createRelation(refId));
    existingSB.setReferences(set);

    when(repository.findAllById(any())).thenReturn(Arrays.asList(existingSB));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/surface-bets")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(Arrays.asList(activeSurfaceBetDto))))
        .andExpect(status().is2xxSuccessful());
  }

  private static Relation createRelation(String refId) {
    Relation relation = new Relation();
    relation.setRelatedTo(RelationType.sport);
    relation.setRefId(refId);
    return relation;
  }

  @Test
  @WithMockCustomUser
  public void testUpdateActiveSBWhenEDP() throws Exception {
    ActiveSurfaceBetDto activeSurfaceBetDto =
        new ActiveSurfaceBetDto("2324", false, true, true, true);
    SurfaceBet existingSB = createValidSurfaceBet();
    existingSB.setId("2324");
    existingSB.setDisabled(true);
    existingSB.setHighlightsTabOn(true);
    existingSB.setEdpOn(false);
    existingSB.setDisplayOnDesktop(true);

    Relation relation = new Relation();
    relation.setRelatedTo(RelationType.edp);
    relation.setRefId("1");

    Set<Relation> set = new HashSet<>();
    set.add(relation);
    existingSB.setReferences(set);

    when(repository.findAllById(any())).thenReturn(Arrays.asList(existingSB));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/surface-bets")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(Arrays.asList(activeSurfaceBetDto))))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testCreateSurfaceBet_edp__OK() throws Exception {

    Set<Relation> refs = new HashSet<>();
    refs.add(
        Relation.builder().enabled(true).relatedTo(RelationType.edp).refId(TEST_PAGE_ID).build());
    entity.setReferences(refs);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testCreateSurfaceBet_eventHub__OK() throws Exception {

    Set<Relation> refs = new HashSet<>();
    refs.add(
        Relation.builder()
            .enabled(true)
            .relatedTo(RelationType.eventhub)
            .refId(TEST_PAGE_ID)
            .build());
    entity.setReferences(refs);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testCreateSurfaceBet_OKForUniversalSegmented() throws Exception {
    SurfaceBet surfaceBet = createSegmentedEntityWithExclusionList();
    surfaceBet.getReferences().clear();
    surfaceBet
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(surfaceBet)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testCreateSurfaceBet_OKForUniversalSegmentedWithPageRefId() throws Exception {
    SurfaceBet surfaceBet = createSegmentedEntityWithExclusionList();
    surfaceBet.getReferences().clear();
    surfaceBet
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("0")
                .id("0")
                .build());
    surfaceBet.getSegmentReferences().get(0).setPageRefId("0");
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(surfaceBet)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testCreateSurfaceBet_OKForUniversalSegmentedWithoutpage() throws Exception {
    SurfaceBet surfaceBet = createSegmentedEntityWithExclusionList();
    surfaceBet.getReferences().clear();
    surfaceBet
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("10")
                .id("0")
                .build());
    surfaceBet.getSegmentReferences().get(0).setPageRefId("0");
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(surfaceBet)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testCreateSurfaceBet_OKForNonUniversalSegmented() throws Exception {
    SurfaceBet surfaceBet = createSegmentedEntityWithInclussionList();
    surfaceBet.getReferences().clear();
    surfaceBet
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(surfaceBet)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testCreateSurfaceBet_OKForNonUniversalSegmentedWithPageRefId() throws Exception {
    SurfaceBet surfaceBet = createSegmentedEntityWithInclussionList();
    surfaceBet.getReferences().clear();
    surfaceBet
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("0")
                .id("0")
                .build());
    surfaceBet.getSegmentReferences().get(0).setPageRefId("0");
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(surfaceBet)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateSurfaceBet_SiteServe_Validation_Fail() throws Exception {

    given(siteServerApi.getEventToOutcomeForOutcome(anyList(), any(SimpleFilter.class), anyList()))
        .willReturn(Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateSurfaceBet_Validation_Fail() throws Exception {

    entity.setTitle("");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  @WithMockCustomUser
  public void testUpdateSurfaceBet() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(String.format("/v1/api/surface-bet/%s", TEST_SB_ID))
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testUpdateSurfaceBetWithArchiveId() throws Exception {
    entity.setArchivalId("1");
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(String.format("/v1/api/surface-bet/%s", TEST_SB_ID))
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testUpdateSurfaceBetWithSvgBgIdAndSvgBgImgPathAndContentHeader() throws Exception {
    entity.setSvgBgId("image2");
    entity.setSvgBgImgPath("/images/uploads/svg/test2.svg");
    entity.setContentHeader("test");
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(String.format("/v1/api/surface-bet/%s", TEST_SB_ID))
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testUpdateSurfaceBetWithoutSvgBgIdAndSvgBgImgPathAndContentHeader() throws Exception {
    entity.setSvgBgId(null);
    entity.setSvgBgImgPath(null);
    entity.setContentHeader(null);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(String.format("/v1/api/surface-bet/%s", TEST_SB_ID))
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateSurfaceBet_Validation_Fail() throws Exception {

    given(siteServerApi.getEventToOutcomeForOutcome(anyList(), any(SimpleFilter.class), anyList()))
        .willReturn(Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put(String.format("/v1/api/surface-bet/%s", TEST_SB_ID))
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  @WithMockCustomUser
  public void disableSurfaceBetsForPage_OK() throws Exception {

    assertThat(entity.getReferences()).allSatisfy(r -> assertTrue(r.isEnabled()));

    given(repository.findByBrand("bma")).willReturn(Arrays.asList(entity));

    mockMvc
        .perform(
            MockMvcRequestBuilders.post(
                    String.format(
                        "/v1/api/surface-bet/disable/%s/%s/%s",
                        "bma", RelationType.sport.toString(), TEST_PAGE_ID))
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());

    assertThat(entity.getReferences()).allSatisfy(r -> assertFalse(r.isEnabled()));
  }

  @Test
  public void disableSurfaceBetsForPage_NotFound_NoChange() throws Exception {

    assertThat(entity.getReferences()).allSatisfy(r -> assertTrue(r.isEnabled()));

    given(repository.findByBrand("bma")).willReturn(Lists.emptyList());

    mockMvc
        .perform(
            MockMvcRequestBuilders.post(
                    String.format(
                        "/v1/api/surface-bet/disable/%s/%s/%s",
                        "bma", RelationType.sport.toString(), TEST_PAGE_ID))
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());

    assertThat(entity.getReferences()).allSatisfy(r -> assertTrue(r.isEnabled()));
  }

  @Test
  public void enableSurfaceBetsForPage__NotFound_NoChange() throws Exception {

    entity.getReferences().clear();
    entity
        .getReferences()
        .add(
            Relation.builder()
                .refId(TEST_PAGE_ID)
                .relatedTo(RelationType.sport)
                .enabled(false)
                .build());

    assertThat(entity.getReferences()).allSatisfy(r -> assertFalse(r.isEnabled()));
    given(repository.findByBrand("bma")).willReturn(Lists.emptyList());

    mockMvc
        .perform(
            MockMvcRequestBuilders.post(
                    String.format(
                        "/v1/api/surface-bet/enable/%s/%s/%s",
                        "bma", RelationType.sport.toString(), TEST_PAGE_ID))
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());

    assertThat(entity.getReferences()).allSatisfy(r -> assertFalse(r.isEnabled()));
  }

  @Test
  @WithMockCustomUser
  public void enableSurfaceBetsForPage_OK() throws Exception {

    entity.getReferences().clear();
    entity
        .getReferences()
        .add(
            Relation.builder()
                .refId(TEST_PAGE_ID)
                .relatedTo(RelationType.sport)
                .enabled(false)
                .build());

    assertThat(entity.getReferences()).allSatisfy(r -> assertFalse(r.isEnabled()));

    given(repository.findByBrand("bma")).willReturn(Arrays.asList(entity));

    mockMvc
        .perform(
            MockMvcRequestBuilders.post(
                    String.format(
                        "/v1/api/surface-bet/enable/%s/%s/%s",
                        "bma", RelationType.sport.toString(), TEST_PAGE_ID))
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());

    assertThat(entity.getReferences()).allSatisfy(r -> assertTrue(r.isEnabled()));
  }

  @Test
  public void testUploadSvg_OK() throws Exception {

    given(
            svgEntityService.attachSvgImage(
                any(SurfaceBet.class), any(MockMultipartFile.class), anyString()))
        .willReturn(Optional.of(entity));

    final MockMultipartFile file =
        new MockMultipartFile("file", "android.svg", "image/png", "file".getBytes());
    mockMvc.perform(multipart("/v1/api/surface-bet/1/image").file(file)).andExpect(status().isOk());
  }

  @Test
  public void testIdUploadSvg_Validation_Fail() throws Exception {

    given(repository.findById(anyString())).willReturn(Optional.empty());

    given(
            svgEntityService.attachSvgImage(
                any(SurfaceBet.class), any(MockMultipartFile.class), anyString()))
        .willReturn(Optional.empty());

    final MockMultipartFile file =
        new MockMultipartFile("file", "android.svg", "image/png", "file".getBytes());

    mockMvc
        .perform(multipart("/v1/api/surface-bet/1/image").file(file))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveIdSvg_Validation_Fail() throws Exception {

    given(repository.findById(anyString())).willReturn(Optional.empty());

    mockMvc.perform(delete("/v1/api/surface-bet/1/image")).andExpect(status().is4xxClientError());
  }

  @Test(expected = NestedServletException.class)
  public void testRemoveImageSvg_Validation_Fail() throws Exception {

    given(svgEntityService.removeSvgImage(any(SurfaceBet.class))).willReturn(Optional.empty());

    mockMvc.perform(delete("/v1/api/surface-bet/1/image")).andExpect(status().is4xxClientError());
  }

  @Test
  public void readAll_OK() throws Exception {
    given(repository.findAll()).willReturn(Arrays.asList(entity));

    mockMvc.perform(get("/v1/api/surface-bet")).andExpect(status().is2xxSuccessful());
  }

  @Test
  public void readByBrand_OK() throws Exception {
    mockMvc
        .perform(get(String.format("/v1/api/surface-bet/brand/%s", "bma")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void readTitleByBrand_OK() throws Exception {
    given(this.surfaceBetTitleRepository.findByBrand("bma"))
        .willReturn(Arrays.asList(new SurfaceBetTitle()));
    mockMvc
        .perform(get(String.format("/v1/api/surface-bet/brand/%s/title", "bma")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void readByBrandAndSegmentForDefault() throws Exception {
    given(
            this.repository.findUniversalRecordsByBrand(
                "bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .willReturn(Arrays.asList(entity));
    mockMvc
        .perform(
            get(
                String.format(
                    "/v1/api/surface-bet/brand/%s/segment/%s", "bma", SegmentConstants.UNIVERSAL)))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.size()", Matchers.is(1)));
  }

  @Test
  public void readByBrandAndSegmentForNonDefault() throws Exception {
    given(
            repository.findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
                Mockito.matches("bma"), Mockito.anyList(), Mockito.anyList(), Mockito.any()))
        .willReturn(Arrays.asList(entity));
    given(repository.findAllByBrandAndSegmentName("bma", Arrays.asList("segment1")))
        .willReturn(Arrays.asList(createSegmentedEntity()));

    mockMvc
        .perform(get(String.format("/v1/api/surface-bet/brand/%s/segment/%s", "bma", "segment1")))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.size()", Matchers.is(2)));
  }

  @Test
  public void read_OK() throws Exception {
    mockMvc
        .perform(get(String.format("/v1/api/surface-bet/%s", "bma")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testOrder_OK() throws Exception {
    OrderDto object =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("0")
            .pageType("sport")
            .segmentName("segment1")
            .build();
    SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    surfaceBet1.setSegmentReferences(Arrays.asList(getSegmentReferences("segment1")));
    surfaceBet1
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2.setSegmentReferences(Arrays.asList(getSegmentReferences("segment1")));
    surfaceBet2
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");
    surfaceBet3.setSegmentReferences(Arrays.asList(getSegmentReferences("segment1")));
    surfaceBet3
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");
    surfaceBet4.setSegmentReferences(Arrays.asList(getSegmentReferences("segment1")));
    surfaceBet4
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    Mockito.when(repository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    Mockito.when(repository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    Mockito.when(repository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    Mockito.when(repository.findById("4")).thenReturn(Optional.of(surfaceBet4));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testOrder_OKForEnhanceSegments() throws Exception {
    OrderDto object =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("0")
            .pageType("sport")
            .segmentName("segment1")
            .build();
    SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    surfaceBet1.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1"))));
    surfaceBet1
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1"))));
    surfaceBet2
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");
    surfaceBet3.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1"))));
    surfaceBet3
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");
    surfaceBet4.setSegmentReferences(
        new ArrayList<>(
            Arrays.asList(getSegmentReferences("segment1"), getSegmentReferences("segment2"))));
    surfaceBet4
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .id("0")
                .refId("0")
                .build());
    surfaceBet4.getSegmentReferences().get(0).setPageRefId("0");
    surfaceBet4.getSegmentReferences().get(0).setId("0");

    Mockito.when(repository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    Mockito.when(repository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    Mockito.when(repository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    Mockito.when(repository.findById("4")).thenReturn(Optional.of(surfaceBet4));
    Mockito.when(repository.findByIdMatches(Arrays.asList("4", "1")))
        .thenReturn(new ArrayList<>(Arrays.asList(surfaceBet4, surfaceBet1)));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testOrder_OKForEnhanceSegmentsWithIdMatches() throws Exception {
    OrderDto object =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("0")
            .pageType("sport")
            .segmentName("segment1")
            .build();
    SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    // surfaceBet1.getSegmentReferences().get(0).setSortOrder(1.0);
    surfaceBet1
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    surfaceBet1.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1", "0"))));

    SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1", "0"))));
    surfaceBet2
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");
    surfaceBet3.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1", "0"))));
    surfaceBet3
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");
    surfaceBet4.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1", "0"))));
    surfaceBet4
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    Mockito.when(repository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    Mockito.when(repository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    Mockito.when(repository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    Mockito.when(repository.findById("4")).thenReturn(Optional.of(surfaceBet4));
    Mockito.when(repository.findByIdMatches(Arrays.asList("4", "1")))
        .thenReturn(new ArrayList<>(Arrays.asList(surfaceBet4, surfaceBet1)));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testOrder_OKWithoutSegmentReference() throws Exception {
    OrderDto object =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("0")
            .pageType("sport")
            .segmentName("segment1")
            .build();
    SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");

    SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");

    SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");

    SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");

    Mockito.when(repository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    Mockito.when(repository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    Mockito.when(repository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    Mockito.when(repository.findById("4")).thenReturn(Optional.of(surfaceBet4));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testOrder_OKWithSortOrder() throws Exception {
    OrderDto object =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("0")
            .pageType("sport")
            .segmentName("segment1")
            .build();
    SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    surfaceBet1.setSegmentReferences(Arrays.asList(getSegmentReferences("segment1")));
    surfaceBet1.getSegmentReferences().get(0).setSortOrder(1.0);
    surfaceBet1
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2.setSegmentReferences(Arrays.asList(getSegmentReferences("segment1")));
    surfaceBet2.getSegmentReferences().get(0).setSortOrder(2.0);
    surfaceBet2
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");
    surfaceBet3.setSegmentReferences(Arrays.asList(getSegmentReferences("segment1")));
    surfaceBet3.getSegmentReferences().get(0).setSortOrder(3.0);
    surfaceBet3
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");
    surfaceBet4.setSegmentReferences(Arrays.asList(getSegmentReferences("segment1")));
    surfaceBet4.getSegmentReferences().get(0).setSortOrder(4.0);
    surfaceBet4
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    Mockito.when(repository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    Mockito.when(repository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    Mockito.when(repository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    Mockito.when(repository.findById("4")).thenReturn(Optional.of(surfaceBet4));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testOrder_OKWithSortOrderSamePageIdForOne() throws Exception {
    OrderDto object =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("0")
            .pageType("sport")
            .segmentName("segment1")
            .build();
    SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    surfaceBet1.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1", "0"))));
    surfaceBet1.getSegmentReferences().get(0).setSortOrder(1.0);
    surfaceBet1
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1"))));
    surfaceBet2.getSegmentReferences().get(0).setSortOrder(2.0);
    surfaceBet2
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");
    surfaceBet3.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1"))));
    surfaceBet3.getSegmentReferences().get(0).setSortOrder(3.0);
    surfaceBet3
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");
    surfaceBet4.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1"))));
    surfaceBet4.getSegmentReferences().get(0).setSortOrder(4.0);
    surfaceBet4
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    Mockito.when(repository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    Mockito.when(repository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    Mockito.when(repository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    Mockito.when(repository.findById("4")).thenReturn(Optional.of(surfaceBet4));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testOrder_OKWithSortOrderSamePageIdForPreviousAndNext() throws Exception {
    OrderDto object =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("0")
            .pageType("sport")
            .segmentName("segment1")
            .build();
    SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    surfaceBet1.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1", "0"))));
    surfaceBet1.getSegmentReferences().get(0).setSortOrder(1.0);
    surfaceBet1
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1", "0"))));
    surfaceBet2.getSegmentReferences().get(0).setSortOrder(2.0);
    surfaceBet2
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");
    surfaceBet3.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1"))));
    surfaceBet3.getSegmentReferences().get(0).setSortOrder(3.0);

    SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");
    surfaceBet4.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1", "0"))));
    surfaceBet4.getSegmentReferences().get(0).setSortOrder(4.0);
    surfaceBet4
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    Mockito.when(repository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    Mockito.when(repository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    Mockito.when(repository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    Mockito.when(repository.findById("4")).thenReturn(Optional.of(surfaceBet4));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testOrder_OKWithSortOrderSamePageIdForNext() throws Exception {
    OrderDto object =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("4")
            .pageId("0")
            .pageType("sport")
            .segmentName("segment1")
            .build();
    SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("4");
    surfaceBet1.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1", "0"))));
    surfaceBet1.getSegmentReferences().get(0).setSortOrder(1.0);
    surfaceBet1
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1", "0"))));
    surfaceBet2.getSegmentReferences().get(0).setSortOrder(2.0);
    surfaceBet2
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");
    surfaceBet3.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1"))));
    surfaceBet3.getSegmentReferences().get(0).setSortOrder(3.0);

    SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");
    surfaceBet4.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1", "0"))));
    surfaceBet4.getSegmentReferences().get(0).setSortOrder(4.0);
    surfaceBet4
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    Mockito.when(repository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    Mockito.when(repository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    Mockito.when(repository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    Mockito.when(repository.findById("4")).thenReturn(Optional.of(surfaceBet4));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testOrder_Failed() throws Exception {
    OrderDto object =
        OrderDto.builder()
            .id("1")
            .pageId("16")
            .order(Collections.singletonList("-1"))
            // .id(UUID.randomUUID().toString())
            .build();

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testOrderWithoutList_Failed() throws Exception {
    OrderDto object =
        OrderDto.builder()
            .id("1")
            .pageId("16")
            // .order(Collections.singletonList("-1"))
            .id(UUID.randomUUID().toString())
            .build();

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void readByBrandForPageId_OK() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                String.format("/v1/api/surface-bet/brand/%s/%s/%s", "bma", "sport", "16")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteWithImage_OK() throws Exception {
    this.mockMvc
        .perform(delete(String.format("/v1/api/surface-bet/%s", TEST_PAGE_ID)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteListWithImage_OK() throws Exception {
    List<String> idList = Arrays.asList("id1", "id2", "id3");
    this.mockMvc
        .perform(delete("/v1/api/surface-bet/{idList}", idList))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteSBTitleByBrand_OK() throws Exception {
    SurfaceBetTitle mockTitle = Mockito.mock(SurfaceBetTitle.class);
    given(surfaceBetTitleRepository.findByBrandAndId(Mockito.anyString(), Mockito.anyString()))
        .willReturn(mockTitle);
    this.mockMvc
        .perform(delete("/v1/api/surface-bet/brand/bma/id/abc123"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteSBTitleByBrand_ClientError() throws Exception {
    this.mockMvc
        .perform(delete("/v1/api/surface-bet/brand/bma/id/abc123"))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void removeImage_OK() throws Exception {

    given(svgEntityService.removeSvgImage(any(SurfaceBet.class))).willReturn(Optional.of(entity));

    this.mockMvc
        .perform(delete(String.format("/v1/api/surface-bet/%s/image", TEST_PAGE_ID)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void readByBrandForSegmentAndPageId_OK() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                String.format(
                    "/v1/api/surface-bet/brand/%s/segment/%s/%s/%s",
                    "bma", "universal", "sport", "16")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void readByBrandForSegmentNonUniversalAndPageId_OK() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                String.format(
                    "/v1/api/surface-bet/brand/%s/segment/%s/%s/%s",
                    "bma", "segment1", "sport", "16")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void readByBrandForSegmentUniversalAndPageId_OK() throws Exception {
    SurfaceBet surfaceBet1 = createSegmentedEntityWithInclussionList();
    List<SurfaceBet> surfaceBets = new ArrayList<>();
    surfaceBets.add(surfaceBet1);
    Mockito.when(
            repository.findAllByBrandAndSegmentNameAndPageRef(
                "bma", Arrays.asList("segment1"), RelationType.valueOf("sport"), "16"))
        .thenReturn(surfaceBets);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                String.format(
                    "/v1/api/surface-bet/brand/%s/segment/%s/%s/%s",
                    "bma", "segment1", "sport", "16")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void readByBrandForDefaultSegmentUniversalAndPageId_OK() throws Exception {
    SurfaceBet surfaceBet1 = createSegmentedEntityWithInclussionList();
    surfaceBet1.setId("1");
    surfaceBet1.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences(SegmentConstants.UNIVERSAL))));
    surfaceBet1.getSegmentReferences().get(0).setSortOrder(1.0);

    SurfaceBet surfaceBet2 = createSegmentedEntityWithInclussionList();
    surfaceBet2.setSegmentReferences(
        FooterMenusTest.getSegmentReference(SegmentConstants.UNIVERSAL));
    surfaceBet2.getSegmentReferences().get(0).setSortOrder(0.0);
    surfaceBet2.getSegmentReferences().addAll(FooterMenusTest.getSegmentReference("segment1"));

    SurfaceBet surfaceBet3 = createSegmentedEntityWithInclussionList();
    surfaceBet3.setSegmentReferences(null);

    SurfaceBet surfaceBet5 = createSegmentedEntityWithInclussionList();
    surfaceBet5.setSegmentReferences(FooterMenusTest.getSegmentReference("segment1"));

    SurfaceBet surfaceBet4 = createSegmentedEntityWithInclussionList();
    surfaceBet4.setId("4");
    surfaceBet4.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences(SegmentConstants.UNIVERSAL))));
    surfaceBet4.getSegmentReferences().get(0).setSortOrder(-1.0);

    List<SurfaceBet> surfaceBets = new ArrayList<>();
    surfaceBets.add(surfaceBet1);
    surfaceBets.add(surfaceBet2);
    surfaceBets.add(surfaceBet3);
    surfaceBets.add(surfaceBet4);
    surfaceBets.add(surfaceBet5);
    Mockito.when(
            repository.findUniversalRecordsByBrandAndPageRef(
                "bma", RelationType.valueOf("sport"), "16"))
        .thenReturn(surfaceBets);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                String.format(
                    "/v1/api/surface-bet/brand/%s/segment/%s/%s/%s",
                    "bma", SegmentConstants.UNIVERSAL, "sport", "16")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void readByBrandForSegmentUniversalAndPageIdWithSegmentReferences_OK() throws Exception {
    SurfaceBet surfaceBet1 = createSegmentedEntityWithInclussionList();
    surfaceBet1.setId("1");
    List<SurfaceBet> surfaceBets = new ArrayList<>();
    surfaceBets.add(surfaceBet1);
    Mockito.when(
            repository.findAllByBrandAndSegmentNameAndPageRef(
                "bma", Arrays.asList("segment1"), RelationType.valueOf("sport"), "16"))
        .thenReturn(surfaceBets);
    SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2.setCreatedAt(Instant.now());
    surfaceBet2.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1"))));
    surfaceBet2
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("2");
    surfaceBet3.setCreatedAt(Instant.now());
    surfaceBet3.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("Universal"))));
    surfaceBet3
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    Mockito.when(
            repository.findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
                "bma",
                Arrays.asList("segment1"),
                Arrays.asList("1"),
                RelationType.valueOf("sport"),
                "16"))
        .thenReturn(new ArrayList<>(Arrays.asList(surfaceBet2, surfaceBet3)));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                String.format(
                    "/v1/api/surface-bet/brand/%s/segment/%s/%s/%s",
                    "bma", "segment1", "sport", "16")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void readByBrandForSegmentUniversalAndPageId_0_WithSegmentReferences_OK()
      throws Exception {
    SurfaceBet surfaceBet1 = createSegmentedEntityWithInclussionList();
    surfaceBet1.setId("1");
    surfaceBet1
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("0")
                .id("1_test")
                .build());
    List<SegmentReference> refrences = new ArrayList<>();
    refrences.add(
        SegmentReference.builder()
            .segmentName("segment1")
            .sortOrder(1.0)
            .pageRefId("1_test")
            .build());
    surfaceBet1.setSegmentReferences(refrences);
    SurfaceBet surfaceBetPage0 = createSegmentedEntityWithInclussionList();
    surfaceBetPage0.setId("1_sport_0");
    List<SegmentReference> refrences1 = new ArrayList<>();
    refrences1.add(
        SegmentReference.builder()
            .segmentName("segment2")
            .sortOrder(1.0)
            .pageRefId("3_test")
            .build());
    surfaceBetPage0.setSegmentReferences(refrences1);
    surfaceBetPage0
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("0")
                .id("2_test")
                .build());

    SurfaceBet surfaceBetPage10 = createSegmentedEntityWithInclussionList();
    surfaceBetPage10.setId("1_sport_1S0");
    List<SegmentReference> refrences2 = new ArrayList<>();
    refrences1.add(
        SegmentReference.builder()
            .segmentName("segment1")
            .sortOrder(1.0)
            .pageRefId("3_test")
            .build());
    surfaceBetPage10.setSegmentReferences(refrences1);
    surfaceBetPage10
        .getReferences()
        .add(
            Relation.builder()
                .enabled(true)
                .relatedTo(RelationType.sport)
                .refId("0")
                .id("2_test")
                .build());

    SurfaceBet surfaceBetPage1 = createSegmentedEntityWithInclussionList();
    surfaceBetPage1.setId("1_sport_1");
    surfaceBetPage1
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.eventhub).refId("0").build());
    SurfaceBet surfaceBetPage3 = createSegmentedEntityWithInclussionList();
    surfaceBetPage3.setId("1_sport_4");
    surfaceBetPage3.setReferences(null);
    List<SurfaceBet> surfaceBets = new ArrayList<>();
    surfaceBets.add(surfaceBet1);
    surfaceBets.add(surfaceBetPage0);
    surfaceBets.add(surfaceBetPage1);
    surfaceBets.add(surfaceBetPage3);
    surfaceBets.add(surfaceBetPage10);

    Mockito.when(
            repository.findAllByBrandAndSegmentNameAndPageRef(
                "bma", Arrays.asList("segment1"), RelationType.valueOf("sport"), "0"))
        .thenReturn(surfaceBets);
    SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2.setCreatedAt(Instant.now());
    surfaceBet2.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("segment1"))));
    surfaceBet2
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("2");
    surfaceBet3.setCreatedAt(Instant.now());
    surfaceBet3.setSegmentReferences(
        new ArrayList<>(Arrays.asList(getSegmentReferences("Universal"))));
    surfaceBet3
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("0").build());

    Mockito.when(
            repository.findByBrandAndApplyUniversalSegmentsAndNotInExclusionListOrInInclusiveList(
                "bma",
                Arrays.asList("segment1"),
                Arrays.asList("1"),
                RelationType.valueOf("sport"),
                "0"))
        .thenReturn(new ArrayList<>(Arrays.asList(surfaceBet2, surfaceBet3)));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                String.format(
                    "/v1/api/surface-bet/brand/%s/segment/%s/%s/%s",
                    "bma", "segment1", "sport", "0")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void hasActiveBetsOnPage_OK() throws Exception {
    SurfaceBet surfaceBet = createSegmentedEntity();
    Mockito.when(repository.findByBrand("bma")).thenReturn(Arrays.asList(surfaceBet));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                String.format(
                    "/v1/api/surface-bet/has-active-bets/%s/%s/%s", "bma", "sport", "16")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void fetchSurfaceBetsBYSegmentNameAndRef_OK() throws Exception {
    SurfaceBet surfaceBet = createSegmentedEntity();
    Mockito.when(repository.findByBrand("bma")).thenReturn(Arrays.asList(surfaceBet));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                String.format(
                    "/v1/api/surface-bet/has-active-bets/%s/%s/%s", "bma", "sport", "16")))
        .andExpect(status().is2xxSuccessful());
  }

  private static SurfaceBet createValidSurfaceBet() {
    SurfaceBet result = new SurfaceBet();
    result.setDisplayFrom(Instant.now());
    result.setDisplayTo(Instant.now().plus(Duration.ofDays(5)));
    result.setEdpOn(true);
    result.setHighlightsTabOn(true);
    result.setPrice(
        new Price()
            .setPriceDec(BigDecimal.valueOf(1.27))
            .setPriceDen(27)
            .setPriceNum(10)
            .setPriceType("LP"));
    result.setSelectionId(BigInteger.valueOf(EXISTS_SELECTION_ID));
    Set<Relation> refs = new HashSet<>();
    refs.add(
        Relation.builder().enabled(true).relatedTo(RelationType.sport).refId(TEST_PAGE_ID).build());
    result.setReferences(refs);
    result.setBrand("bma");
    result.setTitle("test ;:#@&-+()!?'$£");
    result.setContent("content ;:#@&-+()!?'$£");
    result.setSvgBgId("image1");
    result.setSvgBgImgPath("/images/uploads/svg/test1.svg");
    result.setContentHeader("test");
    return result;
  }

  private static SurfaceBet createSegmentedEntity() {
    SurfaceBet surfaceBet = createValidSurfaceBet();
    surfaceBet.setSegmentReferences(Arrays.asList(getSegmentReferences("segment1")));
    return surfaceBet;
  }

  private static SurfaceBet createSegmentedEntityWithExclusionList() {
    SurfaceBet surfaceBet = createValidSurfaceBet();
    surfaceBet.setSegmentReferences(Arrays.asList(getSegmentReferences("segment3")));
    surfaceBet.setExclusionList(Arrays.asList("segment1", "setgment2"));
    return surfaceBet;
  }

  private static SurfaceBet createSegmentedEntityWithInclussionList() {
    SurfaceBet surfaceBet = createValidSurfaceBet();
    surfaceBet.setUniversalSegment(false);
    surfaceBet.setSegmentReferences(Arrays.asList(getSegmentReferences("segment1")));
    surfaceBet.setInclusionList(Arrays.asList("segment1", "setgment2"));
    return surfaceBet;
  }

  private static SegmentReference getSegmentReferences(String segmentName) {
    return SegmentReference.builder().segmentName(segmentName).sortOrder(1.0).build();
  }

  private static SegmentReference getSegmentReferences(String segmentName, String pageRefId) {
    return SegmentReference.builder()
        .segmentName(segmentName)
        .pageRefId(pageRefId)
        .id(pageRefId)
        .sortOrder(1.0)
        .build();
  }

  @Test
  public void readByBrandForSegmentUniversalAndPageType() throws Exception {
    SurfaceBet surfaceBet1 = createSegmentedEntityWithInclussionList();
    List<SurfaceBet> surfaceBets = new ArrayList<>();
    surfaceBets.add(surfaceBet1);
    Mockito.when(
            repository.findAllByBrandAndSegmentNameAndPageRef(
                "bma", Arrays.asList("segment1"), RelationType.valueOf("sport"), "16"))
        .thenReturn(surfaceBets);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                String.format(
                    "/v1/api/surface-bet/brand/%s/segment/%s/%s/%s",
                    "bma", "segment1", "eventhub", "16")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testCreateSurfaceBet_Selection_ID_validation() throws Exception {

    SurfaceBet surfaceBets = createValidSurfaceBet();
    surfaceBets.setId("1234567889");
    surfaceBets.setUniversalSegment(false);
    surfaceBets.setInclusionList(Collections.emptyList());
    Mockito.when(repository.findBySelectionIdAndBrand(anyString(), any(), any(Instant.class)))
        .thenReturn(Arrays.asList(surfaceBets));
    given(siteServerApi.getEventToOutcomeForOutcome(anyList(), any(SimpleFilter.class), anyList()))
        .willReturn(Optional.of(new ArrayList<>()));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testOrder_OK1() throws Exception {
    OrderDto object =
        OrderDto.builder()
            .order(Arrays.asList("4", "1", "2", "3"))
            .id("1")
            .pageId("16")
            .pageType("sport")
            .segmentName("segment1")
            .build();
    SurfaceBet surfaceBet1 = createValidSurfaceBet();
    surfaceBet1.setId("1");
    surfaceBet1.setSegmentReferences(Arrays.asList(getSegmentReferences("segment1")));
    surfaceBet1
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("16").build());

    SurfaceBet surfaceBet2 = createValidSurfaceBet();
    surfaceBet2.setId("2");
    surfaceBet2.setSegmentReferences(Arrays.asList(getSegmentReferences("segment1")));
    surfaceBet2
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("16").build());

    SurfaceBet surfaceBet3 = createValidSurfaceBet();
    surfaceBet3.setId("3");
    surfaceBet3.setSegmentReferences(Arrays.asList(getSegmentReferences("segment1")));
    surfaceBet3
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("16").build());

    SurfaceBet surfaceBet4 = createValidSurfaceBet();
    surfaceBet4.setId("4");
    surfaceBet4.setSegmentReferences(Arrays.asList(getSegmentReferences("segment1")));
    surfaceBet4
        .getReferences()
        .add(Relation.builder().enabled(true).relatedTo(RelationType.sport).refId("16").build());

    Mockito.when(surfaceBetMongoRepository.findById("1")).thenReturn(Optional.of(surfaceBet1));
    Mockito.when(surfaceBetMongoRepository.findById("2")).thenReturn(Optional.of(surfaceBet2));
    Mockito.when(surfaceBetMongoRepository.findById("3")).thenReturn(Optional.of(surfaceBet3));
    Mockito.when(surfaceBetMongoRepository.findById("4")).thenReturn(Optional.of(surfaceBet4));
    List<SurfaceBet> surfaceBets =
        Stream.of(surfaceBet4, surfaceBet1, surfaceBet2, surfaceBet3).collect(Collectors.toList());
    Mockito.when(surfaceBetMongoRepository.findByIdMatches(Arrays.asList("4", "1", "2", "3")))
        .thenReturn(surfaceBets);

    Mockito.when(surfaceBetMongoRepository.saveAll(surfaceBets)).thenReturn(surfaceBets);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/surface-bet/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }
}
