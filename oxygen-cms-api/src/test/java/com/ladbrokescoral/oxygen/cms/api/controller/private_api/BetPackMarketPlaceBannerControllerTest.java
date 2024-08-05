package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackBanner;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackEnablerBannerRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceBannerService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.*;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {BetPackMarketPlaceBannerController.class, BetPackMarketPlaceBannerService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class BetPackMarketPlaceBannerControllerTest extends AbstractControllerTest {

  @MockBean private BetPackEnablerBannerRepository repository;

  // @MockBean private BetPackMarketPlaceBannerService service;

  @MockBean private ImageService imageService;

  private BetPackBanner banner;
  private BetPackBanner updateBanner;
  List<BetPackBanner> bannerList;
  private MockMultipartFile bannerImage;

  private MockMultipartFile bannerImgInMarketPlacePage;

  private MockMultipartFile bannerImgInReviewPage;
  private MockMultipartFile bannerImageUpdated;

  private MockMultipartFile bannerImgInMarketPlacePageUpdated;

  private MockMultipartFile bannerImgInReviewPageUpdated;
  private MockMultipartHttpServletRequestBuilder multipartPutReq;

  private final String path = "/images/uploads/betPackBanner";

  private static final String BRAND = "bma";
  private static final String ImageFileType = "png";

  @Before
  public void init() throws IOException {
    banner =
        TestUtil.deserializeWithJackson(
            "controller/private_api/betpack-enabler/CreateBetpackBanner.json", BetPackBanner.class);
    updateBanner =
        TestUtil.deserializeWithJackson(
            "controller/private_api/betpack-enabler/BetpackBanner.json", BetPackBanner.class);
    given(repository.save(any(BetPackBanner.class))).will(AdditionalAnswers.returnsFirstArg());
    bannerList = new ArrayList<>();
    bannerImage = new MockMultipartFile("bannerImg", "test2.png", "image/png", "file".getBytes());
    bannerImgInMarketPlacePage =
        new MockMultipartFile(
            "bannerImgInMarketPlacePage",
            "bannerImgInMarketPlacePage.png",
            "image/png",
            "file".getBytes());
    bannerImgInReviewPage =
        new MockMultipartFile(
            "bannerImgInReviewPage", "bannerImgInReviewPage.png", "image/png", "file".getBytes());
    bannerImageUpdated =
        new MockMultipartFile("bannerImg", "test4.png", "image/png", "file".getBytes());

    bannerImgInMarketPlacePageUpdated =
        new MockMultipartFile(
            "bannerImgInReviewPageUpdated",
            "bannerImgInReviewPageUpdated.png",
            "image/png",
            "file".getBytes());
    bannerImgInReviewPageUpdated =
        new MockMultipartFile(
            "bannerImgInReviewPageUpdated",
            "bannerImgInReviewPageUpdated.png",
            "image/png",
            "file".getBytes());
    multipartPutReq =
        (MockMultipartHttpServletRequestBuilder)
            multipart("/v1/api/bet-pack/banner/1")
                .with(
                    request -> {
                      request.setMethod(String.valueOf(HttpMethod.PUT));
                      return request;
                    });
  }

  @Test
  public void createBannerTest() throws Exception {
    banner.setId("1");
    banner.setBannerImage(null);
    given(repository.findById(any())).willReturn((Optional.of(banner)));
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(Optional.of(getFilename("test2.png", "banner.png")));

    this.mockMvc
        .perform(
            multipart("/v1/api/bet-pack/banner")
                .file(bannerImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "welcomeMsg")
                .param("termsAndCondition", "termsAndCondition")
                .param("termsAndCondition", "Terms and Condition applied")
                .param("termsAndConditionLink", "termsAndConditionLink")
                .param("buttonText", "buttonText")
                .param("termsAndConditionHyperLinkText", "termsAndConditionHyperLinkText")
                .param("enabled", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createBannerImgInMarketPlacePageTest() throws Exception {
    banner.setId("1");
    banner.setBannerImage(null);
    given(repository.findById(any())).willReturn((Optional.of(banner)));
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(
            Optional.of(
                getFilename("bannerImgInMarketPlacePage.png", "bannerImgInMarketPlacePage.png")));

    this.mockMvc
        .perform(
            multipart("/v1/api/bet-pack/banner")
                .file(bannerImgInMarketPlacePage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "welcomeMsg")
                .param("termsAndCondition", "termsAndCondition")
                .param("termsAndCondition", "Terms and Condition applied")
                .param("termsAndConditionLink", "termsAndConditionLink")
                .param("buttonText", "buttonText")
                .param("termsAndConditionHyperLinkText", "termsAndConditionHyperLinkText")
                .param("enabled", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createBannerImgInReviewTest() throws Exception {
    banner.setId("1");
    banner.setBannerImage(null);
    given(repository.findById(any())).willReturn((Optional.of(banner)));
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(
            Optional.of(getFilename("bannerImgInReviewPage.png", "bannerImgInReviewPage.png")));

    this.mockMvc
        .perform(
            multipart("/v1/api/bet-pack/banner")
                .file(bannerImgInReviewPage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "welcomeMsg")
                .param("termsAndCondition", "termsAndCondition")
                .param("termsAndCondition", "Terms and Condition applied")
                .param("termsAndConditionLink", "termsAndConditionLink")
                .param("buttonText", "buttonText")
                .param("termsAndConditionHyperLinkText", "termsAndConditionHyperLinkText")
                .param("enabled", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createBannerTestWithException() throws Exception {
    banner.setId("1");
    banner.setBannerImage(null);
    given(repository.findById(any())).willReturn((Optional.of(banner)));
    when(imageService.upload(anyString(), any(MockMultipartFile.class), any()))
        .thenReturn(Optional.empty());
    this.mockMvc
        .perform(
            multipart("/v1/api/bet-pack/banner")
                .file(bannerImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "welcomeMsg")
                .param("termsAndCondition", "termsAndCondition")
                .param("termsAndConditionLink", "termsAndConditionLink")
                .param("buttonText", "buttonText")
                .param("termsAndConditionHyperLinkText", "termsAndConditionHyperLinkText")
                .param("enabled", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void createBannerTestWithRunTimeException() throws Exception {
    given(repository.save(any(BetPackBanner.class))).willReturn(banner);
    banner.setId("1");
    banner.setBannerImage(null);
    given(repository.findById(any())).willReturn((Optional.of(banner)));
    when(imageService.upload(anyString(), any(MockMultipartFile.class), any()))
        .thenThrow(new RuntimeException("Exception"));
    this.mockMvc
        .perform(
            multipart("/v1/api/bet-pack/banner")
                .file(bannerImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "welcomeMsg")
                .param("termsAndCondition", "termsAndCondition")
                .param("termsAndConditionLink", "termsAndConditionLink")
                .param("buttonText", "buttonText")
                .param("termsAndConditionHyperLinkText", "termsAndConditionHyperLinkText")
                .param("enabled", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void createBannerTestWithNullException() throws Exception {
    BetPackBanner mockBetPackBanner = Mockito.mock(BetPackBanner.class);
    given(repository.save(any(BetPackBanner.class))).willReturn(mockBetPackBanner);
    Mockito.doThrow(NullPointerException.class).when(mockBetPackBanner).getId();
    given(repository.findById(any())).willReturn(Optional.of(banner));
    when(imageService.upload(anyString(), any(MockMultipartFile.class), any()))
        .thenThrow(new RuntimeException("Exception"));
    this.mockMvc
        .perform(
            multipart("/v1/api/bet-pack/banner")
                .file(bannerImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "welcomeMsg")
                .param("termsAndCondition", "termsAndCondition")
                .param("termsAndConditionLink", "termsAndConditionLink")
                .param("buttonText", "buttonText")
                .param("termsAndConditionHyperLinkText", "termsAndConditionHyperLinkText")
                .param("enabled", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void createBannerTestWithBannerImage() throws Exception {
    given(repository.findById(any())).willReturn((Optional.of(updateBanner)));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    when(imageService.upload(anyString(), any(MockMultipartFile.class), any()))
        .thenReturn(Optional.of(getFilename("test4.png", "banner.png")));
    this.mockMvc
        .perform(
            multipartPutReq
                .file(bannerImageUpdated)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "welcomeMsg")
                .param("termsAndCondition", "termsAndCondition")
                .param("termsAndConditionLink", "termsAndConditionLink")
                .param("buttonText", "buttonText")
                .param("termsAndConditionHyperLinkText", "termsAndConditionHyperLinkText")
                .param("enabled", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createBannerTestExceptionBannerIdNull() throws Exception {
    given(repository.save(any(BetPackBanner.class))).willReturn(banner);
    banner.setBannerImage(null);
    banner.setId(null);
    given(repository.findById(any())).willReturn((Optional.of(banner)));

    when(imageService.upload(anyString(), any(MockMultipartFile.class), any()))
        .thenThrow(new RuntimeException("Exception"));
    this.mockMvc
        .perform(
            multipart("/v1/api/bet-pack/banner")
                .file(bannerImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "welcomeMsg")
                .param("termsAndCondition", "termsAndCondition")
                .param("termsAndConditionLink", "termsAndConditionLink")
                .param("buttonText", "buttonText")
                .param("termsAndConditionHyperLinkText", "termsAndConditionHyperLinkText")
                .param("enabled", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void updateBanner() throws Exception {
    banner.setId("1");
    given(repository.findById(any())).willReturn((Optional.of(updateBanner)));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(Optional.of(getFilename("test2.png", "banner.png")));
    Filename filename = getFilename("test2.png", "banner.png");

    this.mockMvc
        .perform(
            multipartPutReq
                .file(bannerImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "welcomeMsg")
                .param("termsAndCondition", "termsAndCondition")
                .param("termsAndCondition", "Terms and Condition applied")
                .param("termsAndConditionLink", "termsAndConditionLink")
                .param("buttonText", "buttonText")
                .param("termsAndConditionHyperLinkText", "termsAndConditionHyperLinkText")
                .param("enabled", "true")
                .param("bannerImage", String.valueOf(filename))
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateBannerImgInMarketPlacePage() throws Exception {
    banner.setId("1");
    given(repository.findById(any())).willReturn((Optional.of(updateBanner)));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(
            Optional.of(
                getFilename("bannerImgInMarketPlacePage.png", "bannerImgInMarketPlacePage.png")));
    Filename filename =
        getFilename("bannerImgInMarketPlacePage.png", "bannerImgInMarketPlacePage.png");

    this.mockMvc
        .perform(
            multipartPutReq
                .file(bannerImgInMarketPlacePage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "welcomeMsg")
                .param("termsAndCondition", "termsAndCondition")
                .param("termsAndCondition", "Terms and Condition applied")
                .param("termsAndConditionLink", "termsAndConditionLink")
                .param("buttonText", "buttonText")
                .param("termsAndConditionHyperLinkText", "termsAndConditionHyperLinkText")
                .param("enabled", "true")
                .param("bannerInMarketPlacePage", String.valueOf(filename))
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateBannerImgInReviewTest() throws Exception {
    banner.setId("1");
    given(repository.findById(any())).willReturn((Optional.of(updateBanner)));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(
            Optional.of(getFilename("bannerImgInReviewPage.png", "bannerImgInReviewPage.png")));
    Filename filename = getFilename("bannerImgInReviewPage.png", "bannerImgInReviewPage.png");

    this.mockMvc
        .perform(
            multipartPutReq
                .file(bannerImgInReviewPage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "welcomeMsg")
                .param("termsAndCondition", "termsAndCondition")
                .param("termsAndCondition", "Terms and Condition applied")
                .param("termsAndConditionLink", "termsAndConditionLink")
                .param("buttonText", "buttonText")
                .param("termsAndConditionHyperLinkText", "termsAndConditionHyperLinkText")
                .param("enabled", "true")
                .param("bannerInReviewPage", String.valueOf(filename))
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateBannerRemoveImageFalse() throws Exception {
    banner.setId("1");
    given(repository.findById(any())).willReturn((Optional.of(updateBanner)));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(false);
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(Optional.of(getFilename("test2.png", "banner.png")));
    Filename filename = getFilename("test2.png", "banner.png");

    this.mockMvc
        .perform(
            multipartPutReq
                .file(bannerImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "welcomeMsg")
                .param("termsAndCondition", "termsAndCondition")
                .param("termsAndCondition", "Terms and Condition applied")
                .param("termsAndConditionLink", "termsAndConditionLink")
                .param("buttonText", "buttonText")
                .param("termsAndConditionHyperLinkText", "termsAndConditionHyperLinkText")
                .param("enabled", "true")
                .param("bannerImage", String.valueOf(filename))
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void updateBannerWithImageNull() throws Exception {
    given(repository.findById(any())).willReturn((Optional.of(updateBanner)));
    this.mockMvc
        .perform(
            multipartPutReq
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "welcomeMsg")
                .param("termsAndCondition", "termsAndCondition")
                .param("termsAndCondition", "Terms and Condition applied")
                .param("termsAndConditionLink", "termsAndConditionLink")
                .param("buttonText", "buttonText")
                .param("termsAndConditionHyperLinkText", "termsAndConditionHyperLinkText")
                .param("enabled", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateBannerWithException() throws Exception {
    banner.setId("1");
    given(repository.findById(any())).willReturn((Optional.of(updateBanner)));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(Optional.empty());

    this.mockMvc
        .perform(
            multipartPutReq
                .file(bannerImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "welcomeMsg")
                .param("termsAndCondition", "termsAndCondition")
                .param("termsAndCondition", "Terms and Condition applied")
                .param("termsAndConditionLink", "termsAndConditionLink")
                .param("buttonText", "buttonText")
                .param("termsAndConditionHyperLinkText", "termsAndConditionHyperLinkText")
                .param("enabled", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void updateBannerTest() throws Exception {
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(Optional.of(getFilename("test2.png", "banner.png")));
    this.mockMvc
        .perform(
            multipartPutReq
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "welcomeMsg")
                .param("termsAndCondition", "termsAndCondition")
                .param("termsAndCondition", "Terms and Condition applied")
                .param("termsAndConditionLink", "termsAndConditionLink")
                .param("buttonText", "buttonText")
                .param("termsAndConditionHyperLinkText", "termsAndConditionHyperLinkText")
                .param("enabled", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void updateBannerTestFailure() throws Exception {
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), any()))
        .thenThrow(new RuntimeException("Error Occured"));

    this.mockMvc
        .perform(
            multipartPutReq
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "welcomeMsg")
                .param("termsAndCondition", "termsAndCondition")
                .param("termsAndCondition", "Terms and Condition applied")
                .param("termsAndConditionLink", "termsAndConditionLink")
                .param("buttonText", "buttonText")
                .param("termsAndConditionHyperLinkText", "termsAndConditionHyperLinkText")
                .param("enabled", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void getBetPackBannersByBrand() throws Exception {

    bannerList.add(banner);
    given(repository.findByBrand(anyString())).willReturn(bannerList);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/bet-pack/banner/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateBanner)))
        .andExpect(status().isOk());
  }

  @Test
  public void getBetPackBannersByBrandWithNoContent() throws Exception {
    List<BetPackBanner> list = new ArrayList<>();
    given(repository.findByBrand(anyString())).willReturn(list);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/bet-pack/banner/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteById() throws Exception {
    given(repository.findById(any())).willReturn((Optional.of(banner)));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/bet-pack/banner/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private Filename getFilename(String originalFN, String generatedFN) {
    Filename filename = new Filename();
    filename.setOriginalname(originalFN);
    filename.setFilename(generatedFN);
    filename.setPath("/test/path/");
    return filename;
  }
}
