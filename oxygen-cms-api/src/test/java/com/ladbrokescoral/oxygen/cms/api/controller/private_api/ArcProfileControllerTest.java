package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.hamcrest.Matchers.hasSize;
import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.ArcProfileDataDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ArcProfile;
import com.ladbrokescoral.oxygen.cms.api.repository.ArcProfileRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ArcProfileService;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.BeanUtils;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      ArcProfileController.class,
      ArcProfile.class,
      ArcProfileService.class,
      ArcProfileRepository.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class ArcProfileControllerTest extends AbstractControllerTest {
  public static final String LADBROKES = "ladbrokes";
  private ArcProfile arcProfile = new ArcProfile();
  private ArcProfileDataDto arcProfileDataDto;
  private List<ArcProfile> arcProfiles;

  @MockBean ArcProfileService arcProfileService;

  @Before
  public void init() throws IOException {
    final ObjectMapper jsonMapper = new ObjectMapper();
    arcProfileDataDto =
        TestUtil.deserializeWithJackson(
            "controller/private_api/arcProfile.json", ArcProfileDataDto.class);
    arcProfiles =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/private_api/arcProfileDtos.json"),
            new TypeReference<List<ArcProfile>>() {});
    BeanUtils.copyProperties(arcProfileDataDto, arcProfile);
  }

  @Test
  public void testToCreateArcProfile() throws Exception {
    given(
            arcProfileService.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
                anyString(), anyInt(), anyInt()))
        .willReturn(null);
    given(arcProfileService.save(any(ArcProfile.class))).willReturn(arcProfile);
    given(arcProfileService.prepareModelBeforeSave(any())).willReturn(arcProfile);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/arc-profile")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(arcProfileDataDto)))
        .andExpect(status().isCreated());
  }

  @Test
  public void testToCreateArcProfileWithConflict() throws Exception {
    given(
            arcProfileService.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
                anyString(), anyInt(), anyInt()))
        .willReturn(arcProfile);
    given(arcProfileService.save(any(ArcProfile.class))).willReturn(arcProfile);
    given(arcProfileService.prepareModelBeforeSave(any())).willReturn(arcProfile);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/arc-profile")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(arcProfileDataDto)))
        .andExpect(status().isConflict());
  }

  @Test
  public void testToGetArcProfilesByBrand() throws Exception {
    List<ArcProfile> arcProfileList = new ArrayList<>();
    arcProfileList.add(arcProfile);
    given(arcProfileService.findByBrand(anyString())).willReturn(arcProfileList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/arc-profiles/brand/ladbrokes")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$", hasSize(1)));
  }

  @Test
  public void testToGetArcProfilesByBrandAndModelRiskLevelAndReasonCode() throws Exception {

    given(
            arcProfileService.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
                anyString(), anyInt(), anyInt()))
        .willReturn(arcProfile);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/arc-profile/ladbrokes/2/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.brand", is(LADBROKES)));
  }

  @Test
  public void testToGetArcProfilesByBrandAndModelRiskLevelAndReasonCodeNotFound() throws Exception {

    given(
            arcProfileService.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
                anyString(), anyInt(), anyInt()))
        .willReturn(null);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/arc-profile/ladbrokes/2/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testToDeleteArcProfilesByBrandAndModelRiskLevelAndReasonCode() throws Exception {
    given(
            arcProfileService.deleteArcProfileByBrandAndModelRiskLevelAndReasonCode(
                anyString(), anyInt(), anyInt()))
        .willReturn(1l);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/arc-profile/ladbrokes/2/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToDeleteArcProfilesByBrandAndModelRiskLevelAndReasonCodeNotFound()
      throws Exception {

    given(
            arcProfileService.deleteArcProfileByBrandAndModelRiskLevelAndReasonCode(
                anyString(), anyInt(), anyInt()))
        .willReturn(0l);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/arc-profile/ladbrokes/2/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testToDeleteById() throws Exception {
    given(arcProfileService.findOne(anyString())).willReturn(Optional.of(arcProfile));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/arc-profile/60d5b612b5a7cc45b8e4822f")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToReadById() throws Exception {
    given(arcProfileService.findOne(anyString())).willReturn(Optional.of(arcProfile));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/arc-profile/60d5b612b5a7cc45b8e4822f")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToReadAllArcProfiles() throws Exception {
    List<ArcProfile> arcProfileList = new ArrayList<>();
    arcProfileList.add(arcProfile);
    given(arcProfileService.findAll()).willReturn(arcProfileList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/arc-profiles")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateArcProfiles() throws Exception {
    given(
            arcProfileService.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
                anyString(), eq(2), eq(1)))
        .willReturn(arcProfiles.get(0));
    given(
            arcProfileService.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
                anyString(), eq(2), eq(2)))
        .willReturn(null);
    given(arcProfileService.findOne(anyString())).willReturn(Optional.of(arcProfiles.get(0)));
    given(arcProfileService.update(any(), any())).willReturn(arcProfiles.get(0));
    given(arcProfileService.save(any(ArcProfile.class))).willReturn(arcProfiles.get(1));
    given(arcProfileService.prepareModelBeforeSave(any())).willReturn(arcProfiles.get(1));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/arc-profiles/coral")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(arcProfiles)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateArcProfilesWithoutDocument() throws Exception {
    given(
            arcProfileService.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
                anyString(), anyInt(), anyInt()))
        .willReturn(null);
    given(arcProfileService.save(any(ArcProfile.class))).willReturn(arcProfile);
    given(arcProfileService.prepareModelBeforeSave(any())).willReturn(arcProfile);
    List<ArcProfileDataDto> profiles = new ArrayList();
    profiles.add(arcProfileDataDto);
    List<ArcProfile> arcProfileList = new ArrayList<>();
    arcProfileList.add(arcProfile);
    given(arcProfileService.findByBrand(anyString())).willReturn(arcProfileList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/arc-profiles/coral")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(profiles)))
        .andExpect(status().is2xxSuccessful());
  }
}
