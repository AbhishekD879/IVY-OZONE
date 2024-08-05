package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.mockito.Matchers.any;
import static org.mockito.Matchers.anyString;
import static org.mockito.Matchers.eq;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Category;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.repository.VirtualSportTrackRepository;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.api.service.VirtualSportService;
import com.ladbrokescoral.oxygen.cms.api.service.VirtualSportTrackService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.util.Arrays;
import java.util.Collections;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.SpyBean;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(value = {Users.class, AuthenticationService.class, VirtualSportTracks.class})
@AutoConfigureMockMvc(addFilters = false)
public class VirtualSportTracksTest {

  @MockBean private UserService userServiceMock;
  @MockBean private SiteServeApiProvider siteServeApiProvider;
  @Autowired private MockMvc mockMvc;
  @MockBean private VirtualSportTrackRepository repository;
  @MockBean private ImageService imageServiceMock;
  @MockBean private VirtualSportService sportService;
  @SpyBean private VirtualSportTrackService service;
  @Mock private SiteServerApi siteServerApi;

  private VirtualSportTrack virtualSportTrack;

  @Before
  public void setUp() throws Exception {
    virtualSportTrack =
        TestUtil.deserializeWithJackson(
            "controller/private_api/virtual-sports/virtual-sport-track.json",
            VirtualSportTrack.class);

    doReturn(Optional.of(new Filename()))
        .when(imageServiceMock)
        .upload(any(), any(), any(), any(), any());
    doReturn(Optional.empty()).when(userServiceMock).findOne(anyString());
    doReturn(virtualSportTrack).when(repository).save(any(VirtualSportTrack.class));
    doReturn(Optional.of(virtualSportTrack)).when(repository).findById("5e7d4a3f983019527c82330b");
    doReturn(Collections.singletonList(virtualSportTrack))
        .when(repository)
        .findByBrand(eq("ladbrokes"), any());
    doReturn(Collections.singletonList(virtualSportTrack)).when(repository).findAll();
    doReturn(Collections.singletonList(virtualSportTrack))
        .when(repository)
        .findBySportIdOrderBySortOrderAsc("5e7e1c1ac9e77c0001ec5736");

    when(sportService.findOne("5e7e1c1ac9e77c0001ec5736"))
        .thenReturn(
            Optional.of(
                new VirtualSport() {
                  {
                    setTitle("virtual-football");
                  }
                }));

    Category category = new Category();
    category.setId(123);
    category.setName("virtual football");

    when(siteServerApi.getClasses(any(), any())).thenReturn(Optional.of(Arrays.asList(category)));
    when(siteServeApiProvider.api(any())).thenReturn(siteServerApi);
  }

  @Test
  public void create() throws Exception {
    when(sportService.findOne("5e7e1c1ac9e77c0001ec5736")).thenReturn(Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/virtual-sport-track")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(virtualSportTrack)))
        .andExpect(status().isBadRequest());
  }

  @Test
  public void validationFails() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/virtual-sport-track")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(virtualSportTrack)))
        .andExpect(status().isCreated());
  }

  @Test
  public void readFullVirtualSportTrack() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/virtual-sport-track")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void readById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/virtual-sport-track/5e7d4a3f983019527c82330b")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void readVirtualSportTrackBySportId() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get(
                    "/v1/api/virtual-sport-track/sport-id/5e7e1c1ac9e77c0001ec5736")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void readAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/virtual-sport-track")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void update() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/virtual-sport-track/5e7d4a3f983019527c82330b")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(virtualSportTrack)))
        .andExpect(status().isOk());
  }

  @Test
  public void delete() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/virtual-sport-track/5e7d4a3f983019527c82330b")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNoContent());
  }

  @Test
  public void uploadImage() throws Exception {
    MockMultipartFile file =
        new MockMultipartFile("file", "1.png", "image/png", "sample".getBytes());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.multipart(
                    "/v1/api/virtual-sport-track/5e7d4a3f983019527c82330b/image-upload")
                .file(file)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());

    verify(this.service, times(1)).attachImage("5e7d4a3f983019527c82330b", file, null);
  }

  @Test
  public void removeImage() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post(
                    "/v1/api/virtual-sport-track/5e7d4a3f983019527c82330b/image-remove")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"type\":\"SINGLE_FOR_TRACK\",\"filename\":\"1.png\"}"))
        .andExpect(status().isOk());

    verify(this.service, times(1)).removeImageForVirtualSportTrack(any(), any());
  }

  @Test
  public void order() throws Exception {
    OrderDto order =
        OrderDto.builder()
            .order(Collections.singletonList("5e7d4a3f983019527c82330b"))
            .id("5e7d4a3f983019527c82330b")
            .build();

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/virtual-sport-track/ordering")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(order)))
        .andExpect(status().isOk());
  }
}
