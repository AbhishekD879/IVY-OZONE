package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SegmentArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportQuickLinkArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.AliasModuleNamesDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentedModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportQuickLinkRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SystemConfigurationRepository;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import com.ladbrokescoral.oxygen.cms.util.WithMockCustomUser;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.mockito.Mockito;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.util.CollectionUtils;

@WebMvcTest({
  SportQuickLinks.class,
  SportQuickLinkService.class,
  SegmentService.class,
  ModelMapper.class,
  SegmentedModuleSerive.class,
  AutomaticUpdateService.class
})
@AutoConfigureMockMvc(addFilters = false)
@MockBean({EventHubService.class, BrandService.class})
@Import(ModelMapperConfig.class)
public class SportQuickLinksTest extends AbstractControllerTest {
  @MockBean private SportQuickLinkRepository repository;
  @MockBean private SegmentArchivalRepository segmentArchivalRepository;

  @MockBean private SvgEntityService<SportQuickLink> svgEntityService;

  @MockBean private SportQuickLinkArchivalRepository sportQuickLinkArchivalRepository;
  @MockBean private SegmentRepository segmentRepository;
  @MockBean private SegmentedModuleRepository segmentedModuleRepository;
  @MockBean private SystemConfigurationRepository systemConfigurationRepository;

  @MockBean private RGYModuleService rgyModuleService;

  @MockBean private RGYConfigUploadService rgyConfigUploadService;

  private SportQuickLink entity;

  private RGYModuleEntity rgyModuleEntity;

  @Before
  public void init() {

    entity = createSportQuicklink();
    SportQuickLink sportQuickLink = createSportQuicklink();
    sportQuickLink.setId("1");
    rgyModuleEntity = createRgyModuleEntity();
    given(repository.findById(anyString())).willReturn(Optional.of(sportQuickLink));
    given(repository.save(any(SportQuickLink.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testCreateSportQuickLinkError() throws Exception {

    entity.setTitle("");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateSportQuickLinkInvalidEventHub() throws Exception {

    entity.setPageType(PageType.eventhub);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateSportQuickLink() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateSportQuickLinkForDisabled() throws Exception {
    SportQuickLink quickLink = createSportQuicklink();
    quickLink.setPageId("0");
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(quickLink)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testCreateSportQuickLinkForSegmentInclussion() throws Exception {
    SportQuickLink quickLink = createSportQuicklink();
    quickLink.setPageId("0");
    quickLink.setDisabled(false);
    quickLink.setUniversalSegment(false);
    quickLink.setInclusionList(Arrays.asList("segment1", "segment2"));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(quickLink)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateSportQuickLink() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/sport-quick-link/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateSportLinkAndRgyModule() throws Exception {

    SportQuickLink existing = createSportQuicklink();
    existing.setTitle("hello");

    SportQuickLink updated = createSportQuicklink();
    updated.setTitle("supreme");

    given(this.repository.findById(anyString())).willReturn(Optional.of(existing));
    given(this.rgyModuleService.readByBrand(anyString()))
        .willReturn(Collections.singletonList(rgyModuleEntity));
    given(this.rgyModuleService.save(any(RGYModuleEntity.class)))
        .willAnswer(AdditionalAnswers.returnsFirstArg());
    given(this.rgyConfigUploadService.uploadToS3(anyString())).willReturn(Collections.emptyList());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/sport-quick-link/11")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updated)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-quick-link/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrandAndSport() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-quick-link/brand/bma/sport/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrandAndEventHub() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-quick-link/brand/bma/eventhub/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrandAndUnknown() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-quick-link/brand/bma/unknown/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isBadRequest());
  }

  @Test
  public void testReadOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-quick-link/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOneError() throws Exception {

    given(repository.findById(anyString())).willReturn(Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-quick-link/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testDelete() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/sport-quick-link/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteNotFound() throws Exception {
    SportQuickLink sportQuickLink = createSportQuicklink();
    // mock twice
    given(repository.findById(anyString()))
        .willReturn(Optional.of(sportQuickLink), Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/sport-quick-link/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testOrderForUniversal() throws Exception {
    OrderDto object =
        OrderDto.builder()
            .order(Collections.singletonList("-1"))
            .segmentName(SegmentConstants.UNIVERSAL)
            .id(UUID.randomUUID().toString())
            .build();

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testOrderForSegment() throws Exception {
    OrderDto object =
        OrderDto.builder()
            .order(Collections.singletonList("-1"))
            .segmentName("segment-one")
            .id(UUID.randomUUID().toString())
            .build();
    User user = new User();
    user.setId("userId");
    Authentication authentication = mock(Authentication.class);
    SecurityContext securityContext = mock(SecurityContext.class);
    when(securityContext.getAuthentication()).thenReturn(authentication);
    SecurityContextHolder.setContext(securityContext);
    when(SecurityContextHolder.getContext().getAuthentication().getPrincipal()).thenReturn(user);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(object)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateSportQuickLinkBrandSecondscreen() throws Exception {

    entity.setBrand("secondscreen");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testInvalidTitle() throws Exception {

    entity.setBrand("test");
    entity.setTitle("test title1 %");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testInvalidURL() throws Exception {

    entity.setDestination("invalid");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testPutInvalidURL() throws Exception {

    entity.setDestination("invalid");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/sport-quick-link/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testInvalidEndDate() throws Exception {

    Calendar instance = Calendar.getInstance();
    instance.set(Calendar.YEAR, 1990);
    entity.setValidityPeriodEnd(instance.toInstant());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCorrectEndDate() throws Exception {

    Calendar instance = Calendar.getInstance();
    instance.set(Calendar.YEAR, 2990);
    entity.setValidityPeriodEnd(instance.toInstant());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testInvalidDateRange() throws Exception {

    Calendar instance = Calendar.getInstance();
    instance.set(Calendar.YEAR, 2990);
    entity.setValidityPeriodEnd(instance.toInstant());
    instance.set(Calendar.YEAR, 2991);
    entity.setValidityPeriodStart(instance.toInstant());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testInvalidTitleAndSymbol() throws Exception {

    entity.setTitle(null);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUploadSvg() throws Exception {

    when(svgEntityService.attachSvgImage(
            any(SportQuickLink.class), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(entity));

    final MockMultipartFile file =
        new MockMultipartFile("file", "android.svg", "image/png", "file".getBytes());
    mockMvc
        .perform(multipart("/v1/api/sport-quick-link/1/image").file(file))
        .andExpect(status().isOk());
  }

  @Test
  public void testInvalidIdUploadSvg() throws Exception {

    Optional<SportQuickLink> optional = Optional.empty();
    given(repository.findById(anyString())).willReturn(optional);

    when(svgEntityService.attachSvgImage(
            any(SportQuickLink.class), any(MockMultipartFile.class), anyString()))
        .thenReturn(optional);

    final MockMultipartFile file =
        new MockMultipartFile("file", "android.svg", "image/png", "file".getBytes());
    mockMvc
        .perform(multipart("/v1/api/sport-quick-link/1/image").file(file))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveInvalidIdSvg() throws Exception {

    given(repository.findById(anyString())).willReturn(Optional.empty());

    mockMvc
        .perform(delete("/v1/api/sport-quick-link/1/image"))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveInvalidImageSvg() throws Exception {

    when(svgEntityService.removeSvgImage(any(SportQuickLink.class))).thenReturn(Optional.empty());

    mockMvc
        .perform(delete("/v1/api/sport-quick-link/1/image"))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveSvg() throws Exception {

    when(svgEntityService.removeSvgImage(any(SportQuickLink.class)))
        .thenReturn(Optional.of(entity));
    mockMvc
        .perform(delete("/v1/api/sport-quick-link/1/image"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrandAndSegment() throws Exception {
    Mockito.when(
            repository.findUniversalRecordsByBrand("bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(Arrays.asList(createSportQuicklink(), createSportQuicklink()));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-quick-link/brand/bma/segment/Universal")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrandAndUniversalSegment() throws Exception {
    SportQuickLink quickLink = createSportQuicklink();
    quickLink.setUniversalSegment(true);
    Mockito.when(
            repository.findUniversalRecordsByBrand("bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(Arrays.asList(quickLink));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-quick-link/brand/bma/segment/Universal")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrandAndSegment1() throws Exception {
    SportQuickLink quickLink = createSportQuicklink();
    quickLink.setSegmentReferences(FooterMenusTest.getSegmentReference("segment1"));
    Mockito.when(repository.findAllByBrandAndSegmentName("bma", Arrays.asList("segment1")))
        .thenReturn(Arrays.asList(quickLink));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/sport-quick-link/brand/bma/segment/segment1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrandAndSegmentAndSport() throws Exception {
    SportQuickLink quickLink = createSportQuicklink();
    quickLink.setSegmentReferences(FooterMenusTest.getSegmentReference("segment1"));
    Mockito.when(
            repository.findUniversalRecordsByBrandAndPageRef(
                "bma", PageType.valueOf("sport"), "1", SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(Arrays.asList(quickLink));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    "/v1/api/sport-quick-link/brand/bma/segment/universal/sport/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrandAndNonUniversalSegmentAndSport() throws Exception {
    SportQuickLink quickLink = createSportQuicklink();
    quickLink.setSegmentReferences(FooterMenusTest.getSegmentReference("segment1"));
    Mockito.when(
            repository.findAllByBrandAndSegmentNameAndPageRef(
                "bma", Arrays.asList("segment1"), PageType.valueOf("sport"), "1"))
        .thenReturn(Arrays.asList(quickLink));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    "/v1/api/sport-quick-link/brand/bma/segment/segment1/sport/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private SportQuickLink createSportQuicklink() {
    SportQuickLink entity = new SportQuickLink();
    entity.setId("11");
    entity.setBrand("bma");
    entity.setSportId(16);
    entity.setTitle("test title1 ; : # @ & - + * ( ) ! ? ' $");
    entity.setDestination("http://test.com");
    return entity;
  }

  @Test
  public void testCreateSportQuickLinkuniversalRecordLessThanMaxConfig() throws Exception {

    when(systemConfigurationRepository.findOneByBrandAndName("bma", "Sport Quick Links"))
        .thenReturn(createSystemConfig());

    when(segmentRepository.findByBrand("bma")).thenReturn(getSegments());

    when(repository.findAllActiveAndvalidityPeriodStartIsAfterAndvalidityPeriodEndIsBefore(
            any(), any(), any()))
        .thenReturn(getSportQuickLinkList(1, 0, 0));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.convertObjectToJsonBytes(
                        createSegmentedSportQuicklink(new ArrayList<>(), new ArrayList<>()))))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateSportQuickLinkUniversalRecordGreaterThanConfig() throws Exception {

    when(systemConfigurationRepository.findOneByBrandAndName("bma", "Sport Quick Links"))
        .thenReturn(createSystemConfig());
    when(segmentRepository.findByBrand("bma")).thenReturn(getSegments());
    when(repository.findAllActiveAndvalidityPeriodStartIsAfterAndvalidityPeriodEndIsBefore(
            any(), any(), any()))
        .thenReturn(getSportQuickLinkList(3, 0, 0));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.convertObjectToJsonBytes(
                        createSegmentedSportQuicklink(new ArrayList<>(), new ArrayList<>()))))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateSportQuickLinkUniversalRecordGreaterThanConfigAndUniversalSegmentExsists()
      throws Exception {

    when(systemConfigurationRepository.findOneByBrandAndName("bma", "Sport Quick Links"))
        .thenReturn(createSystemConfig());
    when(segmentRepository.findByBrand("bma")).thenReturn(getSegmentsWithUniversal());
    when(repository.findAllActiveAndvalidityPeriodStartIsAfterAndvalidityPeriodEndIsBefore(
            any(), any(), any()))
        .thenReturn(getSportQuickLinkList(3, 0, 0));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.convertObjectToJsonBytes(
                        createSegmentedSportQuicklink(new ArrayList<>(), new ArrayList<>()))))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateSportQuickLinkUniversalRecordWithConfignull() throws Exception {

    when(systemConfigurationRepository.findOneByBrandAndName("bma", "Sport Quick Links"))
        .thenReturn(Optional.empty());
    when(segmentRepository.findByBrand("bma")).thenReturn(getSegments());
    when(repository.findAllActiveAndvalidityPeriodStartIsAfterAndvalidityPeriodEndIsBefore(
            any(), any(), any()))
        .thenReturn(getSportQuickLinkList(3, 0, 0));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.convertObjectToJsonBytes(
                        createSegmentedSportQuicklink(new ArrayList<>(), new ArrayList<>()))))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testCreateSportQuickLinkSegmentedInclusiveRecordLessThanMaxConfig() throws Exception {

    when(systemConfigurationRepository.findOneByBrandAndName("bma", "Sport Quick Links"))
        .thenReturn(createSystemConfig());

    when(segmentRepository.findByBrand("bma")).thenReturn(getSegments());

    when(repository.findAllActiveAndvalidityPeriodStartIsAfterAndvalidityPeriodEndIsBefore(
            any(), any(), any()))
        .thenReturn(getSportQuickLinkList(1, 1, 0));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.convertObjectToJsonBytes(
                        createSegmentedSportQuicklink(
                            new ArrayList<>(), Arrays.asList("s1".split(","))))))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testCreateSportQuickLinkSegmentedInclusiveRecordwithnewRecord() throws Exception {

    when(systemConfigurationRepository.findOneByBrandAndName("bma", "Sport Quick Links"))
        .thenReturn(createSystemConfig());

    when(segmentRepository.findByBrand("bma")).thenReturn(getSegments());

    when(repository.findAllActiveAndvalidityPeriodStartIsAfterAndvalidityPeriodEndIsBefore(
            any(), any(), any()))
        .thenReturn(getSportQuickLinkList(1, 1, 0));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.convertObjectToJsonBytes(
                        createSegmentedSportQuicklink(
                            new ArrayList<>(), Arrays.asList("s5".split(","))))))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  @WithMockCustomUser
  public void testCreateSportQuickLinkSegmentedInclusiveRecordwithnewRecordwithGrtMaxConfig()
      throws Exception {

    when(systemConfigurationRepository.findOneByBrandAndName("bma", "Sport Quick Links"))
        .thenReturn(createSystemConfig());

    when(segmentRepository.findByBrand("bma")).thenReturn(getSegments());

    when(repository.findAllActiveAndvalidityPeriodStartIsAfterAndvalidityPeriodEndIsBefore(
            any(), any(), any()))
        .thenReturn(getSportQuickLinkList(3, 1, 0));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.convertObjectToJsonBytes(
                        createSegmentedSportQuicklink(
                            new ArrayList<>(), Arrays.asList("s5".split(","))))))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateSportQuickLinkSegmentedInclusiveRecordgreaterThanMaxConfig()
      throws Exception {

    when(systemConfigurationRepository.findOneByBrandAndName("bma", "Sport Quick Links"))
        .thenReturn(createSystemConfig());

    when(segmentRepository.findByBrand("bma")).thenReturn(getSegments());

    when(repository.findAllActiveAndvalidityPeriodStartIsAfterAndvalidityPeriodEndIsBefore(
            any(), any(), any()))
        .thenReturn(getSportQuickLinkList(1, 2, 0));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.convertObjectToJsonBytes(
                        createSegmentedSportQuicklink(
                            new ArrayList<>(), Arrays.asList("s1".split(","))))))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateSportQuickLinkuniversalRecordAndExclusionLessThanMaxConfig()
      throws Exception {

    when(systemConfigurationRepository.findOneByBrandAndName("bma", "Sport Quick Links"))
        .thenReturn(createSystemConfig());

    when(segmentRepository.findByBrand("bma")).thenReturn(getSegments());

    when(repository.findAllActiveAndvalidityPeriodStartIsAfterAndvalidityPeriodEndIsBefore(
            any(), any(), any()))
        .thenReturn(getSportQuickLinkList(2, 0, 1));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.convertObjectToJsonBytes(
                        createSegmentedSportQuicklink(
                            Arrays.asList("s2".split(",")), new ArrayList<>()))))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateSportQuickLinkuniversalRecordAndExclusionGreaterThanMaxConfig()
      throws Exception {

    when(systemConfigurationRepository.findOneByBrandAndName("bma", "Sport Quick Links"))
        .thenReturn(createSystemConfig());

    when(segmentRepository.findByBrand("bma")).thenReturn(getSegments());

    when(repository.findAllActiveAndvalidityPeriodStartIsAfterAndvalidityPeriodEndIsBefore(
            any(), any(), any()))
        .thenReturn(getSportQuickLinkList(3, 0, 1));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.convertObjectToJsonBytes(
                        createSegmentedSportQuicklink(
                            Arrays.asList("s2".split(",")), new ArrayList<>()))))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateSportQuickLinkuniversalRecordWithExclusionLessThanMaxConfig()
      throws Exception {

    when(systemConfigurationRepository.findOneByBrandAndName("bma", "Sport Quick Links"))
        .thenReturn(createSystemConfig());

    when(segmentRepository.findByBrand("bma")).thenReturn(getSegments());

    when(repository.findAllActiveAndvalidityPeriodStartIsAfterAndvalidityPeriodEndIsBefore(
            any(), any(), any()))
        .thenReturn(getSportQuickLinkList(1, 1, 1));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.convertObjectToJsonBytes(
                        createSegmentedSportQuicklink(
                            Arrays.asList("s2".split(",")), new ArrayList<>()))))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateSportQuickLinkuniversalRecordWithExclusiongreaterThanMaxConfig()
      throws Exception {

    when(systemConfigurationRepository.findOneByBrandAndName("bma", "Sport Quick Links"))
        .thenReturn(createSystemConfig());

    when(segmentRepository.findByBrand("bma")).thenReturn(getSegments());

    when(repository.findAllActiveAndvalidityPeriodStartIsAfterAndvalidityPeriodEndIsBefore(
            any(), any(), any()))
        .thenReturn(getSportQuickLinkList(1, 2, 1));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.convertObjectToJsonBytes(
                        createSegmentedSportQuicklink(
                            Arrays.asList("s2".split(",")), new ArrayList<>()))))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void
      testCreateSportQuickLinkuniversalRecordWithExclusionAndInclusionEqualMaxAndToatallessThannMaxConfig()
          throws Exception {

    when(systemConfigurationRepository.findOneByBrandAndName("bma", "Sport Quick Links"))
        .thenReturn(createSystemConfig());

    when(segmentRepository.findByBrand("bma")).thenReturn(getSegments());

    when(repository.findAllActiveAndvalidityPeriodStartIsAfterAndvalidityPeriodEndIsBefore(
            any(), any(), any()))
        .thenReturn(getSportQuickLinkList(0, 3, 1));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/sport-quick-link")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.convertObjectToJsonBytes(
                        createSegmentedSportQuicklink(
                            Arrays.asList("s1".split(",")), new ArrayList<>()))))
        .andExpect(status().is2xxSuccessful());
  }

  private List<SportQuickLink> getSportQuickLinkList(
      int numberofUniversal, int inclusiveList, int exclusivelist) {
    List<SportQuickLink> liksList = new ArrayList<>();
    while (numberofUniversal > 0) {
      liksList.add(createSegmentedSportQuicklink(new ArrayList<>(), new ArrayList<>()));
      numberofUniversal--;
    }

    while (inclusiveList > 0) {
      liksList.add(
          createSegmentedSportQuicklink(new ArrayList<>(), Arrays.asList("s1".split(","))));
      inclusiveList--;
    }

    while (exclusivelist > 0) {
      liksList.add(
          createSegmentedSportQuicklink(Arrays.asList("s1".split(",")), new ArrayList<>()));
      exclusivelist--;
    }
    return liksList;
  }

  private SportQuickLink createSegmentedSportQuicklink(
      List<String> exeList, List<String> incluList) {
    SportQuickLink entity = new SportQuickLink();
    entity.setBrand("bma");
    entity.setSportId(16);
    entity.setTitle("test title1 ; : # @ & - + * ( ) ! ? ' $");
    entity.setDestination("http://test.com");
    entity.setUniversalSegment(true);
    entity.setPageId("0");
    entity.setDisabled(false);
    if (CollectionUtils.isEmpty(incluList)) {
      entity.setExclusionList(exeList);

    } else {
      entity.setInclusionList(incluList);
      entity.setUniversalSegment(false);
    }
    return entity;
  }

  private List<Segment> getSegments() {
    List<Segment> segments = new ArrayList<>();
    segments.add(Segment.builder().brand("bma").segmentName("s1").build());
    segments.add(Segment.builder().brand("bma").segmentName("s2").build());
    segments.add(Segment.builder().brand("bma").segmentName("s3").build());

    return segments;
  }

  private List<Segment> getSegmentsWithUniversal() {
    List<Segment> segments = new ArrayList<>();
    segments.add(Segment.builder().brand("bma").segmentName("s1").build());
    segments.add(Segment.builder().brand("bma").segmentName("s2").build());
    segments.add(Segment.builder().brand("bma").segmentName("s3").build());
    segments.add(Segment.builder().brand("bma").segmentName("Universal").build());

    return segments;
  }

  private Optional<SystemConfiguration> createSystemConfig() {
    SystemConfiguration config = new SystemConfiguration();
    List<SystemConfigProperty> properties = new ArrayList<>();
    SystemConfigProperty property = new SystemConfigProperty();
    property.setName("maxAmount");
    property.setStructureValue("3");
    properties.add(property);
    ;
    config.setProperties(properties);
    return Optional.of(config);
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
