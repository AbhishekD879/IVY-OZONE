package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Overlay;
import com.ladbrokescoral.oxygen.cms.api.repository.OverlayRepository;
import com.ladbrokescoral.oxygen.cms.api.service.OverlayService;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.SpyBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {
      OverlayController.class,
      OverlayService.class,
    })
@AutoConfigureMockMvc(addFilters = false)
public class OverLayControllerTest extends AbstractControllerTest {
  @MockBean private OverlayRepository repository;
  @SpyBean private OverlayService service;
  private Overlay entity;

  @Before
  public void init() {
    entity = new Overlay();
    entity.setId("98789987");
    entity.setBrand("bma");
    doReturn(entity).when(service).update(any(Overlay.class), any(Overlay.class));
    doReturn(entity).when(service).save(any(Overlay.class));
    doReturn(Optional.of(entity)).when(repository).findOneByBrand("bma");
    entity = createOverlay("1", true);
    given(repository.findById(any(String.class))).willReturn(Optional.of(entity));
    given(repository.save(any(Overlay.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testReadAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/overlay").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/overlay/1").contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.id", is("1")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOneError() throws Exception {
    given(repository.findById(any(String.class))).willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/overlay/3").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound())
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdateContest() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/overlay/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrand() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/overlay/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadAllByBrandWithEmptyOverlay() throws Exception {
    doReturn(Optional.ofNullable(null)).when(repository).findOneByBrand("bma");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/overlay/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  private Overlay createOverlay(String id, boolean b) {
    Overlay overlayInfo = new Overlay();
    overlayInfo.setBrand("bma");
    overlayInfo.setId(id);
    overlayInfo.setHeaderTitle("welcome overlay");
    return overlayInfo;
  }
}
