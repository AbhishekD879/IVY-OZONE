package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.junit.Assert.assertNotNull;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.TeamKit;
import com.ladbrokescoral.oxygen.cms.api.mapping.TeamMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.TeamKitRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.SvgImageParser;
import com.ladbrokescoral.oxygen.cms.api.service.TeamKitService;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({TeamKits.class, TeamKitService.class})
@AutoConfigureMockMvc(addFilters = false)
@MockBean(SvgImageParser.class)
public class TeamKitsTest extends AbstractControllerTest {

  @MockBean private ImageService imageService;
  @MockBean private TeamKitRepository repository;

  private TeamKit entity;

  @Before
  public void init() {

    entity = createTeamKit();

    given(repository.findById(anyString())).willReturn(Optional.of(entity));
    given(repository.save(any(TeamKit.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void getTeamKits() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/team-kit/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void testCreateTeamKit() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/team-kit")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().isCreated());
  }

  @Test
  public void testCreateTeamKit_BadRequest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/team-kit")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes("wrong dto")))
        .andExpect(status().isBadRequest());
  }

  @Test
  public void testCreateTeamKitWithImage() throws Exception {

    final MockMultipartFile file =
        new MockMultipartFile("file", "android.svg", "image/png", "file".getBytes());

    final Filename fileName = new Filename();
    fileName.setPath("path");
    fileName.setOriginalname("originalname");

    given(imageService.upload(anyString(), any(), anyString(), anyString(), isNull()))
        .willReturn(Optional.of(fileName));

    this.mockMvc
        .perform(
            multipart("/v1/api/team-kit/brand/bma/teamName/image")
                .file(file)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().isOk());
  }

  @Test
  public void testUpdateTeamKit() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/team-kit/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().isOk());
  }

  @Test
  public void testUpdateTeamKit_BadRequest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/team-kit/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes("wrong dto")))
        .andExpect(status().isBadRequest());
  }

  @Test
  public void testGetTeamKits() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/team-kit").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/team-kit/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void testGetById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/team-kit/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void testGetByIdError() throws Exception {
    given(repository.findById(anyString())).willReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/team-kit/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testDelete() throws Exception {

    entity.setId("100");

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/team-kit/100")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNoContent());
  }

  @Test
  public void testMapperDeclaration() {
    TeamMapper teamMapper = TeamMapper.getInstance();
    assertNotNull(teamMapper);
  }

  private static TeamKit createTeamKit() {
    TeamKit dto = new TeamKit();
    dto.setBrand("bma");
    dto.setTeamName("teamName");
    dto.setPath("testPathToImage");
    return dto;
  }
}
