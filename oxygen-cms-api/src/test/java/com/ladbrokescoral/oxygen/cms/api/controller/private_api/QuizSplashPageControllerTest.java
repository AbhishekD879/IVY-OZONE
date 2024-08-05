package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.mockito.BDDMockito.given;
import static org.mockito.Matchers.any;
import static org.mockito.Matchers.anyString;
import static org.mockito.Matchers.eq;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.SplashPage;
import com.ladbrokescoral.oxygen.cms.api.repository.QuestionEngineRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.QuizSplashPageRepository;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.QuizSplashPageService;
import com.ladbrokescoral.oxygen.cms.api.service.SvgImageParser;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import java.util.Collections;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      Users.class,
      AuthenticationService.class,
      QuizSplashPageController.class,
      QuizSplashPageService.class,
      QuizSplashPageRepository.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class QuizSplashPageControllerTest {

  @MockBean private QuizSplashPageRepository repository;
  @MockBean private ImageService imageService;
  @MockBean private SvgImageParser svgImageParser;

  @MockBean private QuestionEngineRepository questionEngineRepository;
  @MockBean private MongoTemplate mongoTemplate;
  @MockBean private UserService userServiceMock;
  @Autowired private MockMvc mockMvc;

  private SplashPage splashPage;
  private String path = "/images/uploads/quizSplashPage";

  @Before
  public void setUp() throws Exception {
    splashPage = getSimpleSPData();
    given(repository.findById("1")).willReturn(Optional.of(splashPage));
    given(repository.findByBrand("1")).willReturn(Collections.singletonList(splashPage));
    given(repository.save(any(SplashPage.class))).willReturn(splashPage);
  }

  @Test
  public void create() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/splash-page")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(splashPage)))
        .andExpect(status().isCreated());
  }

  @Test
  public void getAll() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/splash-page")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void readById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/splash-page/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void readByBrand() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/splash-page/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void update() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/splash-page/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(splashPage)))
        .andExpect(status().isOk());
  }

  @Test
  public void delete() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/splash-page/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNoContent());
  }

  @Test
  public void uploadImageLogo() throws Exception {

    final MockMultipartFile file =
        new MockMultipartFile("file", "android.svg", "image/svg", "file".getBytes());
    given(repository.findById("1")).willReturn(Optional.of(splashPage));
    given(imageService.upload(anyString(), any(), eq(path)))
        .willReturn(Optional.of(getFilename("android.svg", "323566.svg")));
    Svg svg = new Svg();
    svg.setSvg("<svg>");
    given(svgImageParser.parse(any())).willReturn(Optional.of(svg));
    this.mockMvc
        .perform(
            multipart("/v1/api/splash-page/1/file?svg=true")
                .file("logo", file.getBytes())
                .content(TestUtil.convertObjectToJsonBytes(splashPage)))
        .andExpect(status().isOk());

    Assert.assertNotNull(splashPage.getLogoSvgFile());
    Assert.assertEquals("android.svg", splashPage.getLogoSvgFilename());
  }

  @Test
  public void uploadImageBackground() throws Exception {

    final MockMultipartFile file =
        new MockMultipartFile("file", "android.svg", "image/svg", "file".getBytes());
    given(repository.findById("1")).willReturn(Optional.of(splashPage));
    given(imageService.upload(anyString(), any(), eq(path)))
        .willReturn(Optional.of(getFilename("android.svg", "323566.svg")));
    Svg svg = new Svg();
    svg.setSvg("<svg>");
    given(svgImageParser.parse(any())).willReturn(Optional.of(svg));
    this.mockMvc
        .perform(
            multipart("/v1/api/splash-page/1/file?svg=true")
                .file("background", file.getBytes())
                .content(TestUtil.convertObjectToJsonBytes(splashPage)))
        .andExpect(status().isOk());

    Assert.assertEquals("android.svg", splashPage.getBackgroundSvgFilename());
  }

  @Test
  public void deleteImage() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/splash-page/1/file?imageType=FOOTER")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void deleteImageBackground() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/splash-page/1/file?imageType=LOGO")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  private SplashPage getSimpleSPData() {
    SplashPage splashPage = new SplashPage();
    splashPage.setId("1");
    splashPage.setBrand("bma");
    splashPage.setTitle("SP");
    return splashPage;
  }

  private Filename getFilename(String originalFN, String generatedFN) {
    Filename filename = new Filename();
    filename.setOriginalname(originalFN);
    filename.setFilename(generatedFN);
    filename.setPath("/test/path/");
    return filename;
  }
}
