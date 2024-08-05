package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.StructurePublicService;
import java.util.Collections;
import java.util.Optional;
import org.junit.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({SystemConfigurationApi.class})
@AutoConfigureMockMvc(addFilters = false)
public class SystemConfigurationApiTest extends AbstractControllerTest {

  @MockBean StructurePublicService structurePublicService;

  @Test
  public void testFindEnabled() throws Exception {
    given(structurePublicService.find("bma")).willReturn(Optional.of(Collections.emptyMap()));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/system-configuration")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testFailedToFind() throws Exception {
    given(structurePublicService.find("bma")).willReturn(Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/system-configuration")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testFailedToFindConfigByName() throws Exception {
    given(structurePublicService.findElement("bma", "SomeConfig")).willReturn(Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/system-configurations/SomeConfig")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testFindConfigByName() throws Exception {
    given(structurePublicService.findElement("bma", "SomeConfig"))
        .willReturn(Optional.of(Collections.emptyMap()));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/bma/system-configurations/SomeConfig")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}
