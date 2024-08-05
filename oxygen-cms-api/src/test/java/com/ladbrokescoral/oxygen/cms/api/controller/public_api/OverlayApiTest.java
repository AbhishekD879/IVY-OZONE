package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Overlay;
import com.ladbrokescoral.oxygen.cms.api.repository.OverlayRepository;
import com.ladbrokescoral.oxygen.cms.api.service.OverlayService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OverlayPublicService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.Arrays;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {OverlayApi.class, OverlayPublicService.class, OverlayService.class})
@AutoConfigureMockMvc(addFilters = false)
@Import(ModelMapperConfig.class)
public class OverlayApiTest extends AbstractControllerTest {
  @MockBean private OverlayRepository repository;
  private Overlay entity;

  @Before
  public void init() {
    entity = new Overlay();
    entity.setId("1");
    entity.setHeaderTitle("welcome Tutorial");
    given(repository.findByBrand(anyString())).willReturn(Arrays.asList(entity));
    doReturn(Optional.of(entity)).when(repository).findOneByBrand("bma");
  }

  @Test
  public void testByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/overlay")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.id", is("1")))
        .andExpect(jsonPath("$.headerTitle", is("welcome Tutorial")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testByBrandWithEmpty() throws Exception {
    doReturn(Optional.ofNullable(null)).when(repository).findOneByBrand("bma");
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/overlay")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}
