package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.repository.VirtualSportRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.VirtualSportTrackRepository;
import com.ladbrokescoral.oxygen.cms.api.service.SvgEntityService;
import com.ladbrokescoral.oxygen.cms.api.service.VirtualSportService;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.beans.BeanUtils;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({VirtualSports.class, VirtualSportService.class})
@AutoConfigureMockMvc(addFilters = false)
public class VirtualSportsTest extends AbstractControllerTest {

  @MockBean private VirtualSportRepository repository;
  @MockBean private VirtualSportTrackRepository trackRepository;

  @MockBean private SvgEntityService<VirtualSport> svgEntityService;

  private VirtualSport entity;

  @Before
  public void init() throws Exception {

    entity =
        TestUtil.deserializeWithJackson(
            "controller/private_api/virtual-sports/virtual-sport.json", VirtualSport.class);

    given(repository.findById(anyString())).willReturn(Optional.of(entity));
    given(repository.save(any(VirtualSport.class))).will(AdditionalAnswers.returnsFirstArg());

    given(svgEntityService.attachSvgImage(any(), any(), any())).willReturn(Optional.of(entity));
    given(svgEntityService.removeSvgImage(any())).willReturn(Optional.of(entity));
  }

  @Test
  public void create() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/virtual-sport")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().isCreated());
  }

  @Test
  public void readFullVirtualSport() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/virtual-sport")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void readById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/virtual-sport/5e7e1c1ac9e77c0001ec5736")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void readVirtualSportByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/virtual-sport/brand/ladbrokes")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void readAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/virtual-sport")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void update() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/virtual-sport/5e7e1c1ac9e77c0001ec5736")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().isOk());
  }

  @Test
  public void updateWithTitleChange() throws Exception {

    // Mock 2 related sport tracks
    List<Filename> silks = Arrays.asList(new Filename(), new Filename());

    Map<String, List<Filename>> eventSilks = new HashMap<>();
    eventSilks.put("event", silks);

    List<VirtualSportTrack> virtualSportTracks = new ArrayList<>();
    VirtualSportTrack virtualSportTrack = new VirtualSportTrack();
    virtualSportTrack.setRunnerImages(silks);
    virtualSportTracks.add(virtualSportTrack);

    virtualSportTrack = new VirtualSportTrack();
    virtualSportTrack.setEventRunnerImages(eventSilks);
    virtualSportTracks.add(virtualSportTrack);

    virtualSportTrack = new VirtualSportTrack();
    virtualSportTracks.add(virtualSportTrack);
    when(trackRepository.findBySportIdOrderBySortOrderAsc(anyString()))
        .thenReturn(virtualSportTracks);

    VirtualSport entityUpdated = new VirtualSport();
    BeanUtils.copyProperties(entity, entityUpdated);

    // FIXME: not sure what we are testing here
    entityUpdated.setTitle("NewTitle");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/virtual-sport/5e7e1c1ac9e77c0001ec5736")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entityUpdated)))
        .andExpect(status().isOk());

    verify(trackRepository, times(2)).save(any(VirtualSportTrack.class));
  }

  @Test
  public void delete() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/virtual-sport/5e7e1c1ac9e77c0001ec5736")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNoContent());
  }

  @Test
  public void attachIcon() throws Exception {
    MockMultipartFile file =
        new MockMultipartFile("file", "android.svg", "image/svg", "file".getBytes());
    mockMvc
        .perform(multipart("/v1/api/virtual-sport/5e7e1c1ac9e77c0001ec5736/icon").file(file))
        .andExpect(status().isOk());
  }

  @Test
  public void deleteIcon() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/virtual-sport/5e7e1c1ac9e77c0001ec5736/icon")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void order() throws Exception {
    OrderDto order =
        OrderDto.builder()
            .order(Collections.singletonList("5e7e1c1ac9e77c0001ec5736"))
            .id("5e7e1c1ac9e77c0001ec5736")
            .build();

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/virtual-sport/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(order)))
        .andExpect(status().isOk());
  }
}
