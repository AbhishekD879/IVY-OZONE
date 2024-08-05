package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.hamcrest.Matchers.hasSize;
import static org.hamcrest.Matchers.is;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.ArcProfileDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ArcProfile;
import com.ladbrokescoral.oxygen.cms.api.repository.ArcProfileRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ArcProfileService;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ArcProfilePublicService;
import java.io.IOException;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      ArcProfileApi.class,
      ArcProfile.class,
      ArcProfileDto.class,
      ArcProfilePublicService.class,
      ArcProfileRepository.class,
      ArcProfileService.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class ArcProfileApiTest {

  private List<ArcProfileDto> arcProfiles;

  @MockBean private ArcProfilePublicService arcProfilePublicService;

  @MockBean private ArcProfileService arcProfileService;

  @MockBean private AuthenticationService authenticationService;

  @MockBean private UserService userService;

  @Autowired private MockMvc mockMvc;

  @Before
  public void init() throws IOException {
    final ObjectMapper jsonMapper = new ObjectMapper();
    jsonMapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);
    jsonMapper.registerModule(new JavaTimeModule());
    arcProfiles =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/public_api/arcProfilesDto.json"),
            new TypeReference<List<ArcProfileDto>>() {});
  }

  @Test
  public void testToGetArcProfilesByBrand() throws Exception {
    given(arcProfilePublicService.findByBrand(anyString())).willReturn(arcProfiles);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/arc-profile")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$", hasSize(1)));
  }

  @Test
  public void testToGetArcProfilesByBrandAndModelRiskLevelAndReasonCode() throws Exception {
    given(
            arcProfilePublicService.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
                anyString(), anyInt(), anyInt()))
        .willReturn(arcProfiles.get(0));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/arc-profile/2/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.brand", is("coral")));
  }

  @Test
  public void testToGetArcProfilesByBrandNotFound() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/arc-profile")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testToGetArcProfilesByBrandAndModelRiskLevelAndReasonCodeNotFound() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/ladbrokes/arc-profile/2/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testToGetArcProfilesById() throws Exception {
    given(arcProfilePublicService.findById(anyString())).willReturn(arcProfiles.get(0));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/arc-profile/60dee0ef2d035979bf67eac0")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.brand", is("coral")));
  }
}
