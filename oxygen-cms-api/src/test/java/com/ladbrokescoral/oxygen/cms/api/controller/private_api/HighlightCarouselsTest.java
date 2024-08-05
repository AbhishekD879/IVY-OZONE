package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.HighlightCarouselArchiveRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SegmentArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.HighlightCarousel;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.repository.HighlightCarouselRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentedModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.Arrays;
import java.util.Optional;
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
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

// @RunWith(SpringRunner.class)
@WebMvcTest({
  HighlightCarousels.class,
  HighlightCarouselService.class,
  SegmentService.class,
  ModelMapper.class,
  SegmentedModuleSerive.class
})
@AutoConfigureMockMvc(addFilters = false)
@MockBean({SvgEntityService.class, EventHubService.class, BrandService.class})
@Import(ModelMapperConfig.class)
public class HighlightCarouselsTest extends AbstractControllerTest {

  private static final String HIGHLIGHT_CAROUSEL_URL = "/v1/api/highlight-carousel";

  @MockBean private HighlightCarouselRepository repository;
  @MockBean private SiteServeApiProvider siteServeApiProvider;
  @MockBean private SiteServerApi siteServerApi;

  @MockBean private HighlightCarouselArchiveRepository highlightCarouselArchiveRepository;
  @MockBean private SegmentRepository segmentRepository;
  @MockBean private SegmentedModuleRepository segmentedModuleRepository;
  @MockBean private SegmentArchivalRepository segmentArchivalRepository;
  @MockBean private CompetitionModuleService competitionModuleService;

  @Before
  public void init() {

    given(repository.findById(anyString())).willReturn(Optional.of(create()));
    given(repository.save(any(HighlightCarousel.class))).will(AdditionalAnswers.returnsFirstArg());

    given(siteServeApiProvider.api("bma")).willReturn(siteServerApi);
    given(siteServerApi.getEvent(any(), eq(true))).willReturn(Optional.of(new Event()));

    given(
            repository.findUniversalRecordsByBrandAndPageRef(
                "bma", PageType.valueOf("sport"), "0", SortableService.SORT_BY_SORT_ORDER_ASC))
        .willReturn(Arrays.asList(create()));
    given(repository.findUniversalRecordsByBrand("bma", SortableService.SORT_BY_SORT_ORDER_ASC))
        .willReturn(Arrays.asList(create()));
    HighlightCarousel highlightCarousel = create();
    highlightCarousel.setSegmentReferences(FooterMenusTest.getSegmentReference("segment1"));
    given(repository.findAllByBrandAndSegmentName("bma", Arrays.asList("segment1")))
        .willReturn(Arrays.asList(highlightCarousel));
  }

  @Test
  public void testCreateHighlightCarouselInplayNull() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(HIGHLIGHT_CAROUSEL_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.readFromFileAsBytes(
                        "controller/public_api/highlight-carousel-inplay-null.json")))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateHighlightCarouselInplayTrue() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(HIGHLIGHT_CAROUSEL_URL)
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    TestUtil.readFromFileAsBytes(
                        "controller/public_api/highlight-carousel-inplay-true.json")))
        .andExpect(MockMvcResultMatchers.jsonPath("$.inPlay").value(true))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadByBrandAndSegmentNameWithoutPageType() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    HIGHLIGHT_CAROUSEL_URL + "/brand/bma/segment/" + SegmentConstants.UNIVERSAL)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.length()").value(1));
  }

  @Test
  public void testReadByBrandAndSegmentNameWithoutPageTypeForNonUniversal() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(HIGHLIGHT_CAROUSEL_URL + "/brand/bma/segment/segment1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.length()").value(1));
  }

  @Test
  public void testReadByBrandAndSegmentName() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    HIGHLIGHT_CAROUSEL_URL
                        + "/brand/bma/segment/"
                        + SegmentConstants.UNIVERSAL
                        + "/sport/0")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.length()").value(1));
  }

  @Test
  public void testReadByBrandAndSegmentNameForNonUniversal() throws Exception {
    HighlightCarousel highlightCarousel = create();
    highlightCarousel.setUniversalSegment(false);
    highlightCarousel.setSegmentReferences(FooterMenusTest.getSegmentReference("segment1"));
    Mockito.when(
            repository.findAllByBrandAndSegmentNameAndPageRef(
                "bma", Arrays.asList("segment1"), PageType.valueOf("sport"), "0"))
        .thenReturn(Arrays.asList(highlightCarousel));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    HIGHLIGHT_CAROUSEL_URL + "/brand/bma/segment/segment1/sport/0")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(MockMvcResultMatchers.jsonPath("$.length()").value(1));
  }

  @Test
  public void successfulDeleteShouldReturn204() throws Exception {

    // given
    String idToBeRemoved = "100";

    // then
    mockMvc
        .perform(MockMvcRequestBuilders.delete(HIGHLIGHT_CAROUSEL_URL + "/" + idToBeRemoved))
        .andExpect(status().isNoContent());
  }

  @Test
  public void deleteShouldReturn404WhenEntityDoesntExist() throws Exception {
    // given
    String idToBeRemoved = "101";
    given(repository.findById(idToBeRemoved)).willReturn(Optional.empty());
    // then
    mockMvc
        .perform(MockMvcRequestBuilders.delete(HIGHLIGHT_CAROUSEL_URL + "/" + idToBeRemoved))
        .andExpect(status().isNotFound());
  }

  private static HighlightCarousel create() {
    HighlightCarousel dto = new HighlightCarousel();
    dto.setId("100");
    dto.setBrand("bma");
    dto.setSportId(16);
    dto.setTitle("test title1 ;:#@&-+()!?'$£");
    return dto;
  }
}
