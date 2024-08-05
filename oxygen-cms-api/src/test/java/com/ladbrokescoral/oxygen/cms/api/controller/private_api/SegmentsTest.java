package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SegmentArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentPurgeService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.assertj.core.util.Arrays;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {Segments.class, SegmentService.class, SegmentPurgeService.class})
@AutoConfigureMockMvc(addFilters = false)
@Import(ModelMapperConfig.class)
public class SegmentsTest extends AbstractControllerTest {

  @Mock private SegmentService service;
  @Mock private ModelMapper mapper;
  @MockBean private SegmentRepository segmentRepository;
  @MockBean private SegmentArchivalRepository segmentArchivalRepository;
  @MockBean private SegmentPurgeService purgeService;
  private Segment segment;

  public void init() throws Exception {

    this.segment = createSegment("segment1");
    this.segment.setId("1");
    given(segmentRepository.findByBrand("bma")).willReturn(getSegments());
    given(segmentRepository.save(any(Segment.class))).willReturn(this.segment);
    given(segmentRepository.findById("1")).willReturn(Optional.of(segment));
  }

  @Test
  public void testReadAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/segments/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.size()", is(5)))
        .andExpect(jsonPath("$[0].name", is(SegmentConstants.UNIVERSAL)));
  }

  @Test
  public void testCreateSegment() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/segments")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createSegment("segment1"))))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.id", is("1")))
        .andExpect(jsonPath("$.segmentName", is("segment1")));
  }

  @Test
  public void testUpdateSegment() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/segments/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(createSegment("segment1"))))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.id", is("1")))
        .andExpect(jsonPath("$.segmentName", is("segment1")));
  }

  @Test
  public void testDeleteSegments() throws Exception {

    when(segmentRepository.findAllByIdIn(anyList())).thenReturn(getSegments("1,2,3"));
    Mockito.doNothing().when(purgeService).deleteSegmentsInModules(any(List.class), any());
    Mockito.doNothing().when(segmentRepository).deleteByIdIn(any(List.class));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/segments/1,2,3/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteSegmentsWithUniversalSegment() throws Exception {

    when(segmentRepository.findAllByIdIn(anyList())).thenReturn(getSegments());
    Mockito.doNothing().when(purgeService).deleteSegmentsInModules(any(List.class), any());
    Mockito.doNothing().when(segmentRepository).deleteByIdIn(any(List.class));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/segments/1,2,3/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private Segment createSegment(String segmentName) {
    return Segment.builder().segmentName(segmentName).brand("bma").build();
  }

  private List<Segment> getSegments() {
    List<Segment> segList = new ArrayList<>();
    segList.add(createSegment("s1"));
    segList.add(createSegment("s2"));
    segList.add(createSegment("s3"));
    segList.add(createSegment("s4"));
    segList.add(createSegment("Universal"));

    return segList;
  }

  private List<Segment> getSegments(String segments) {
    List<Segment> segList = new ArrayList<>();

    Arrays.asList(segments.split(",")).forEach(seg -> segList.add(createSegment(seg.toString())));

    return segList;
  }
}
