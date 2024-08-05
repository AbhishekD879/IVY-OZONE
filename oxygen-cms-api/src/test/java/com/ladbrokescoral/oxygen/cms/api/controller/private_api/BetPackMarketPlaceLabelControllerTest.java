package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.dto.BetPackLabelDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackLabel;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackEnablerLabelRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceLabelService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.mockito.Mockito;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {
      BetPackMarketPlaceLabelController.class,
      BetPackMarketPlaceLabelService.class,
    })
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class BetPackMarketPlaceLabelControllerTest extends AbstractControllerTest {
  public static final String CORAL = "coral";
  private BetPackLabel betPackLabelEntity = new BetPackLabel();
  private List<BetPackLabel> betPackLabelEntityList = new ArrayList<>();
  private BetPackLabelDto betPackLabelDto;
  private BetPackLabel betPackLabel;
  @MockBean private BetPackEnablerLabelRepository betPackEnablerLabelRepository;
  // @MockBean private CrudService<BetPackLabel> crudService;

  private MockMultipartFile backgroundImage;
  private MockMultipartFile backgroundImageUpdated;

  @MockBean private ImageService imageService;

  // @MockBean BetPackMarketPlaceLabelService betPackMarketPlaceLabelService;
  private final String path = "/images/uploads/betPackLabel";

  @Before
  public void init() throws IOException {
    betPackLabelDto =
        TestUtil.deserializeWithJackson(
            "controller/private_api/betpack-enabler/BetpackLabel.json", BetPackLabelDto.class);
    betPackLabel =
        TestUtil.deserializeWithJackson(
            "controller/private_api/betpack-enabler/BetpackLabel.json", BetPackLabel.class);

    backgroundImage =
        new MockMultipartFile("backgroundImage", "test2.png", "image/png", "file".getBytes());
    backgroundImageUpdated =
        new MockMultipartFile(
            "backgroundImageUpdated", "test4.png", "image/png", "file".getBytes());

    given(betPackEnablerLabelRepository.save(any(BetPackLabel.class)))
        .will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void testCreateLabel() throws Exception {
    betPackLabelDto.setAllFilterPillMessageActive(true);
    given(betPackEnablerLabelRepository.findById(any()))
        .willReturn((Optional.of(betPackLabelEntity)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bet-pack/label")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackLabelDto)))
        .andExpect(status().isCreated());
  }

  @Test
  public void testCreateLabelFilterMessageNull() throws Exception {
    betPackLabelDto.setAllFilterPillMessage(null);
    given(betPackEnablerLabelRepository.findById(any()))
        .willReturn((Optional.of(betPackLabelEntity)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bet-pack/label")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackLabelDto)))
        .andExpect(status().isCreated());
  }

  @Test
  public void testCreateLabelFalseAllFilterPillMessageActive() throws Exception {
    betPackLabelDto.setAllFilterPillMessageActive(false);
    given(betPackEnablerLabelRepository.findById(any()))
        .willReturn((Optional.of(betPackLabelEntity)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bet-pack/label")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackLabelDto)))
        .andExpect(status().isCreated());
  }

  @Test
  public void testCreateLabelWithException() throws Exception {
    betPackLabelDto.setAllFilterPillMessageActive(true);
    betPackLabelDto.setAllFilterPillMessage(null);
    given(betPackEnablerLabelRepository.findById(any()))
        .willReturn((Optional.of(betPackLabelEntity)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/bet-pack/label")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackLabelDto)))
        .andExpect(status().isBadRequest());
  }

  @Test
  public void testGetAllBetPackLabels() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/bet-pack/labels")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetBetPackLabelsByBrand() throws Exception {
    betPackLabelEntityList.add(betPackLabel);
    given(betPackEnablerLabelRepository.findByBrand(anyString()))
        .willReturn(betPackLabelEntityList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/bet-pack/label/brand/bma")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackLabel)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetBetPackLabelsByBrandNotFound() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/bet-pack/label/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetBetPackLabelById() throws Exception {
    given(betPackEnablerLabelRepository.findById(anyString()))
        .willReturn(Optional.of(betPackLabelEntity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/bet-pack/label/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateBetPackLabel() throws Exception {
    given(betPackEnablerLabelRepository.findById(anyString()))
        .willReturn(Optional.of(betPackLabelEntity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/bet-pack/label/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(betPackLabel)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteById() throws Exception {
    given(betPackEnablerLabelRepository.findById(anyString()))
        .willReturn(Optional.of(betPackLabel));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-pack/label/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteByIdEmptyData() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-pack/label/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void handleFileUploadTest() throws Exception {
    given(betPackEnablerLabelRepository.findById(any())).willReturn((Optional.of(betPackLabel)));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(Optional.of(getFilename("test2.png", "banner.png")));
    mockMvc
        .perform(
            multipart("/v1/api/bet-pack/label/uploadImage/1")
                .file("file", backgroundImage.getBytes())
                .param("bannerId", "1"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void handleFileUploadBackGroundImageNullTest() throws Exception {
    betPackLabel.setBackgroundImage(null);
    given(betPackEnablerLabelRepository.findById(any())).willReturn((Optional.of(betPackLabel)));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(Optional.of(getFilename("test2.png", "banner.png")));
    mockMvc
        .perform(
            multipart("/v1/api/bet-pack/label/uploadImage/1")
                .file("file", backgroundImage.getBytes())
                .param("bannerId", "1"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void handleFileUploadTestThrowException() throws Exception {
    given(betPackEnablerLabelRepository.findById(any())).willReturn((Optional.of(betPackLabel)));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);

    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(Optional.empty());
    mockMvc
        .perform(
            multipart("/v1/api/bet-pack/label/uploadImage/1")
                .file("file", backgroundImage.getBytes())
                .param("bannerId", "1"))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void handleFileUploadTestRemoveImageFalse() throws Exception {
    given(betPackEnablerLabelRepository.findById(any())).willReturn((Optional.of(betPackLabel)));
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(Optional.of(getFilename("test2.png", "banner.png")));
    mockMvc
        .perform(
            multipart("/v1/api/bet-pack/label/uploadImage/1")
                .file("file", backgroundImage.getBytes())
                .param("bannerId", "1"))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void handleFileUploadTestWithoutImage() throws Exception {
    given(betPackEnablerLabelRepository.findById(any())).willReturn((Optional.of(betPackLabel)));
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(Optional.of(getFilename("test5.png", "abc.png")));
    mockMvc
        .perform(
            multipart("/v1/api/bet-pack/label/uploadImage/1")
                .file("file", null)
                .param("bannerId", "1"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void handleFileUploadWithoutImageTest() throws Exception {
    mockMvc
        .perform(
            multipart("/v1/api/bet-pack/label/uploadImage/1")
                .file("file", backgroundImage.getBytes())
                .param("bannerId", "1"))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void handleFileRemoveTest() throws Exception {
    given(betPackEnablerLabelRepository.findById(any())).willReturn((Optional.of(betPackLabel)));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-pack/label/remove-image/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void handleFileRemoveTestFalse() throws Exception {
    given(betPackEnablerLabelRepository.findById(any())).willReturn((Optional.of(betPackLabel)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-pack/label/remove-image/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void handleFileRemoveWithEmptyDataTest() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-pack/label/remove-image/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  private Filename getFilename(String originalFN, String generatedFN) {
    Filename filename = new Filename();
    filename.setOriginalname(originalFN);
    filename.setFilename(generatedFN);
    filename.setPath("/test/path/");
    return filename;
  }
}
