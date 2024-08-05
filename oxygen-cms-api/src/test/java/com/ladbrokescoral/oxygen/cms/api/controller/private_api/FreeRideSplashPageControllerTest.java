package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideSplashPage;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.FreeRideSplashPageFailureException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.FreeRideSplashPageRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FreeRideSplashPageService;
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

@WebMvcTest(value = {FreeRideSplashPageController.class, FreeRideSplashPageService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class FreeRideSplashPageControllerTest extends AbstractControllerTest {

  @MockBean private FreeRideSplashPageRepository freeRideSplashPageRepository;

  @MockBean private ImageService imageService;

  private FreeRideSplashPage createSplashpage;
  private FreeRideSplashPage updateSplashpage;

  private MockMultipartFile splashImage;
  private MockMultipartFile bannerImage;
  private MockMultipartFile freeRideLogo;

  private MockMultipartFile splashImageUpdated;
  private MockMultipartFile bannerImageUpdated;
  private MockMultipartFile freeRideLogoUpdated;

  private List<FreeRideSplashPage> freeRideSplashpageList;

  private MockMultipartHttpServletRequestBuilder multipartPutReq;

  private final String path = "/images/uploads/freeRideSplashPage";

  private static final String BRAND = "ladbrokes";
  private static final String ImageFileType = "png";

  @Before
  public void init() throws IOException {
    createSplashpage =
        TestUtil.deserializeWithJackson(
            "controller/private_api/free_ride/createSplashpage.json", FreeRideSplashPage.class);

    updateSplashpage =
        TestUtil.deserializeWithJackson(
            "controller/private_api/free_ride/updateSplashpage.json", FreeRideSplashPage.class);

    freeRideSplashpageList = new ArrayList<>();

    given(freeRideSplashPageRepository.save(any(FreeRideSplashPage.class)))
        .will(AdditionalAnswers.returnsFirstArg());

    splashImage = new MockMultipartFile("splashImg", "test1.png", "image/png", "file".getBytes());
    bannerImage = new MockMultipartFile("bannerImg", "test2.png", "image/png", "file".getBytes());
    freeRideLogo =
        new MockMultipartFile("freeRideLogoImg", "test3.png", "image/png", "file".getBytes());

    splashImageUpdated =
        new MockMultipartFile("splashImg", "test4.png", "image/png", "file".getBytes());
    bannerImageUpdated =
        new MockMultipartFile("bannerImg", "test4.png", "image/png", "file".getBytes());
    freeRideLogoUpdated =
        new MockMultipartFile("freeRideLogoImg", "test4.png", "image/png", "file".getBytes());

    multipartPutReq =
        (MockMultipartHttpServletRequestBuilder)
            multipart("/v1/api/freeride/splashpage/1")
                .with(
                    request -> {
                      request.setMethod(String.valueOf(HttpMethod.PUT));
                      return request;
                    });
  }

  @Test
  public void createWithSplashImage() throws Exception {
    given(freeRideSplashPageRepository.findById(any())).willReturn((Optional.of(createSplashpage)));
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(Optional.of(getFilename("test1.png", "splash.png")));

    this.mockMvc
        .perform(
            multipart("/v1/api/freeride/splashpage")
                .file(splashImage)
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "Free")
                .param("buttonText", "Free Ride Banner")
                .param("termsAndCondition", "Terms and Condition applied")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createWithBannerImage() throws Exception {
    given(freeRideSplashPageRepository.findById(any())).willReturn((Optional.of(createSplashpage)));
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(Optional.of(getFilename("test2.png", "banner.png")));

    this.mockMvc
        .perform(
            multipart("/v1/api/freeride/splashpage")
                .file(bannerImage)
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "Free")
                .param("buttonText", "Free Ride Banner")
                .param("termsAndCondition", "Terms and Condition applied")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createWithFreeRideLogo() throws Exception {
    given(freeRideSplashPageRepository.findById(any())).willReturn((Optional.of(createSplashpage)));
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(Optional.of(getFilename("test3.png", "frLogo.png")));

    this.mockMvc
        .perform(
            multipart("/v1/api/freeride/splashpage")
                .file(freeRideLogo)
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "Free")
                .param("buttonText", "Free Ride Banner")
                .param("termsAndCondition", "Terms and Condition applied")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createFailedWithFileUploadError() throws Exception {
    given(freeRideSplashPageRepository.findById(any())).willReturn((Optional.of(createSplashpage)));
    when(imageService.upload(anyString(), any(MockMultipartFile.class), any()))
        .thenReturn(Optional.empty());

    this.mockMvc
        .perform(
            multipart("/v1/api/freeride/splashpage")
                .file(splashImage)
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "Free")
                .param("buttonText", "Free Ride Banner")
                .param("termsAndCondition", "Terms and Condition applied")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void createFailedWithFileUploadRunTimeError() throws Exception {
    given(freeRideSplashPageRepository.save(any(FreeRideSplashPage.class)))
        .willReturn(createSplashpage);
    given(freeRideSplashPageRepository.findById(any())).willReturn((Optional.of(createSplashpage)));
    when(imageService.upload(anyString(), any(MockMultipartFile.class), any()))
        .thenThrow(new RuntimeException("Error Occured"));

    this.mockMvc
        .perform(
            multipart("/v1/api/freeride/splashpage")
                .file(splashImage)
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "Free")
                .param("buttonText", "Free Ride Banner")
                .param("termsAndCondition", "Terms and Condition applied")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void createFailedWithFileUploadIdNullError() throws Exception {
    createSplashpage.setId(null);
    given(freeRideSplashPageRepository.save(any(FreeRideSplashPage.class)))
        .willReturn(createSplashpage);
    given(freeRideSplashPageRepository.findById(any())).willReturn((Optional.of(createSplashpage)));
    when(imageService.upload(anyString(), any(MockMultipartFile.class), any()))
        .thenThrow(new RuntimeException("Error Occured"));

    this.mockMvc
        .perform(
            multipart("/v1/api/freeride/splashpage")
                .file(splashImage)
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "Free")
                .param("buttonText", "Free Ride Banner")
                .param("termsAndCondition", "Terms and Condition applied")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void createFailedWithFileUploadNullPointerError() throws Exception {
    FreeRideSplashPage mockSplashPage = Mockito.mock(FreeRideSplashPage.class);
    given(freeRideSplashPageRepository.save(any(FreeRideSplashPage.class)))
        .willReturn(mockSplashPage);
    Mockito.doThrow(NullPointerException.class).when(mockSplashPage).getId();
    given(freeRideSplashPageRepository.findById(any())).willReturn((Optional.of(createSplashpage)));
    when(imageService.upload(anyString(), any(MockMultipartFile.class), any()))
        .thenThrow(new RuntimeException("Error Occured"));

    this.mockMvc
        .perform(
            multipart("/v1/api/freeride/splashpage")
                .file(splashImage)
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "Free")
                .param("buttonText", "Free Ride Banner")
                .param("termsAndCondition", "Terms and Condition applied")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void updateWithoutUpdatingImage() throws Exception {
    given(freeRideSplashPageRepository.findById(any())).willReturn((Optional.of(updateSplashpage)));
    this.mockMvc
        .perform(
            multipartPutReq
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("welcomeMsg", "New Message")
                .param("buttonText", "Let's GO")
                .param("termsAndCondition", "Terms and Condition applied")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE)
                .content(TestUtil.convertObjectToJsonBytes(updateSplashpage)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateWithSplashImage() throws Exception {
    given(freeRideSplashPageRepository.findById(any())).willReturn((Optional.of(updateSplashpage)));

    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(getFilename("test4.png", "splash.png")));

    this.mockMvc
        .perform(
            multipartPutReq
                .file(splashImageUpdated)
                .param("brand", BRAND)
                .param("welcomeMsg", "New Benefits")
                .param("buttonText", "Let's GO")
                .param("termsAndCondition", "Terms and Condition applied")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE)
                .content(TestUtil.convertObjectToJsonBytes(updateSplashpage)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateWithBannerImage() throws Exception {
    given(freeRideSplashPageRepository.findById(any())).willReturn((Optional.of(updateSplashpage)));

    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(getFilename("test4.png", "banner.png")));

    this.mockMvc
        .perform(
            multipartPutReq
                .file(bannerImageUpdated)
                .param("brand", BRAND)
                .param("welcomeMsg", "New Benefits")
                .param("buttonText", "Let's GO")
                .param("termsAndCondition", "Terms and Condition applied")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE)
                .content(TestUtil.convertObjectToJsonBytes(updateSplashpage)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateWithFreeRideLogo() throws Exception {
    given(freeRideSplashPageRepository.findById(any())).willReturn((Optional.of(updateSplashpage)));

    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(getFilename("test4.png", "frLogo.png")));

    this.mockMvc
        .perform(
            multipartPutReq
                .file(freeRideLogoUpdated)
                .param("brand", BRAND)
                .param("welcomeMsg", "New Benefits")
                .param("buttonText", "Let's GO")
                .param("termsAndCondition", "Terms and Condition applied")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE)
                .content(TestUtil.convertObjectToJsonBytes(updateSplashpage)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void updateFailedWithFileRemoveError() throws Exception {
    given(freeRideSplashPageRepository.findById(any())).willReturn((Optional.of(updateSplashpage)));

    Mockito.when(imageService.removeImage(anyString(), any()))
        .thenReturn(Boolean.FALSE)
        .thenThrow(new FreeRideSplashPageFailureException("Error occurred while removing image"));

    this.mockMvc
        .perform(
            multipartPutReq
                .file(splashImageUpdated)
                .param("brand", BRAND)
                .param("welcomeMsg", "New Benefits")
                .param("buttonText", "Let's GO")
                .param("termsAndCondition", "Terms and Condition applied")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE)
                .content(TestUtil.convertObjectToJsonBytes(updateSplashpage)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void updateFailedWithFileUploadError() throws Exception {
    given(freeRideSplashPageRepository.findById(any())).willReturn((Optional.of(updateSplashpage)));

    given(imageService.removeImage(anyString(), any())).willReturn(Boolean.TRUE);
    given(imageService.upload(anyString(), any(MockMultipartFile.class), any()))
        .willThrow(new FileUploadException("File Upload Failed"));

    this.mockMvc
        .perform(
            multipartPutReq
                .file(splashImageUpdated)
                .param("brand", BRAND)
                .param("welcomeMsg", "New Benefits")
                .param("buttonText", "Let's GO")
                .param("termsAndCondition", "Terms and Condition applied")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE)
                .content(TestUtil.convertObjectToJsonBytes(updateSplashpage)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void updateFailedWithServerError() throws Exception {
    given(freeRideSplashPageRepository.findById(any()))
        .willThrow(new NotFoundException("Error occurred while updating splash page"));

    this.mockMvc
        .perform(
            multipartPutReq
                .param("id", "1")
                .param("brand", BRAND)
                .param("welcomeMsg", "New Benefits")
                .param("buttonText", "Let's GO")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE)
                .content(TestUtil.convertObjectToJsonBytes(updateSplashpage)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void getSplashPageByBrandWhenSplashPageExists() throws Exception {
    freeRideSplashpageList.add(updateSplashpage);
    given(freeRideSplashPageRepository.findAllByBrand(anyString()))
        .willReturn(freeRideSplashpageList);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/freeride/splashpage/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(updateSplashpage)))
        .andExpect(status().isOk());
  }

  @Test
  public void getSplashPageByBrandWhenSplashPageNotExists() throws Exception {
    given(freeRideSplashPageRepository.findAllByBrand(anyString()))
        .willReturn(freeRideSplashpageList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/freeride/splashpage/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  private Filename getFilename(String originalFN, String generatedFN) {
    Filename filename = new Filename();
    filename.setOriginalname(originalFN);
    filename.setFilename(generatedFN);
    filename.setPath("/test/path/");
    return filename;
  }
}
