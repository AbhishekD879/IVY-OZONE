package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackOnboarding;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.exception.BetPackMarketPlaceException;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackMarketplaceOnboardingRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceOnboardingService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import com.mongodb.client.result.UpdateResult;
import java.util.Arrays;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.mockito.Mockito;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {BPMPOnBoardingController.class, BetPackMarketPlaceOnboardingService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class BPMPOnBoardingControllerTest extends AbstractControllerTest {

  @MockBean private MongoTemplate mongoTemplate;
  @MockBean private BetPackMarketplaceOnboardingRepository repository;

  @MockBean private ImageService imageService;

  @MockBean private UpdateResult updateResult;

  private BetPackOnboarding betPackOnboarding;
  private MockMultipartFile onboardingImage;
  private MockMultipartFile invalidOnboardImage;
  private MockMultipartHttpServletRequestBuilder multipartPutReq;
  private MockMultipartHttpServletRequestBuilder multipartImagePutReq;
  private MockMultipartFile onboardingImageUpdate;
  private MockMultipartHttpServletRequestBuilder multipartImageErrorPutReq;

  private final String path = "/images/uploads/onboarding/betPackOnboarding";

  private static final String BRAND = "coral";
  private static final String ImageFileType = "png";

  @Before
  public void setUp() throws Exception {
    betPackOnboarding =
        TestUtil.deserializeWithJackson(
            "controller/private_api/betpack-enabler/BetpackOnboarding.json",
            BetPackOnboarding.class);

    given(repository.save(any(BetPackOnboarding.class))).will(AdditionalAnswers.returnsFirstArg());
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(Optional.of(getFilename("first_image.png", "test.png")));

    onboardingImage =
        new MockMultipartFile(
            "images[0].onboardImg", "first_image.png", "image/png", "file".getBytes());

    invalidOnboardImage =
        new MockMultipartFile(
            "images[0].onboardImg", "first_image.svg", "image/svg", "file".getBytes());
    onboardingImageUpdate =
        new MockMultipartFile("onboardImg", "first_image.png", "image/png", "file".getBytes());

    multipartPutReq =
        (MockMultipartHttpServletRequestBuilder)
            multipart("/v1/api/bet-pack/onboarding/1")
                .with(
                    request -> {
                      request.setMethod(String.valueOf(HttpMethod.PUT));
                      return request;
                    });
    String putUrl =
        String.format(
            "/v1/api/bet-pack/onboarding/%s/images/%s",
            "62cd9ce3fa2d927e6d9c18ad", "62cd9dfefa2d927e6d9c18c4");
    multipartImagePutReq =
        (MockMultipartHttpServletRequestBuilder)
            multipart(putUrl)
                .with(
                    request -> {
                      request.setMethod(String.valueOf(HttpMethod.PUT));
                      return request;
                    });

    String putUrlError =
        String.format("/v1/api/bet-pack/onboarding/%s/images/%s", "62cd9ce3fa2d927e6d9c18ad", "1");
    multipartImageErrorPutReq =
        (MockMultipartHttpServletRequestBuilder)
            multipart(putUrlError)
                .with(
                    request -> {
                      request.setMethod(String.valueOf(HttpMethod.PUT));
                      return request;
                    });
    System.out.println(betPackOnboarding);
  }

  @Test
  public void postBetpackOnboardingTest_2xx() throws Exception {

    betPackOnboarding.setId("1");
    betPackOnboarding.getImages().get(0).setOnboardImageDetails(null);

    given(repository.findById(any())).willReturn((Optional.of(betPackOnboarding)));

    this.mockMvc
        .perform(
            multipart("/v1/api/bet-pack/onboarding")
                .file(onboardingImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("images[0].imageLabel", "Image 1")
                .param("images[0].nextCTAButtonLabel", "NEXT")
                .param("images[0].imageType", "Onboarding")
                .param("isActive", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void putBetpackOnboardingTest_2xx() throws Exception {
    betPackOnboarding.setId("1");
    String id = "2";
    given(repository.findById(any())).willReturn((Optional.of(betPackOnboarding)));
    /* when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
            .thenReturn(Optional.of(getFilename("first_image.png", "test.png")));*/
    this.mockMvc
        .perform(
            multipartPutReq
                .file(onboardingImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("images[0].imageLabel", "Image 1")
                .param("images[0].nextCTAButtonLabel", "NEXT")
                .param("images[0].imageType", "Onboarding")
                .param("isActive", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().isOk());
  }

  @Test
  public void putBetPackOnboardingImageTestWithoutImage_2xx() throws Exception {

    // betPackOnboarding.getImages().get(0).setId(null);
    when(repository.findById(anyString())).thenReturn(Optional.of(betPackOnboarding));
    this.mockMvc
        .perform(
            multipartImagePutReq
                // .file(null)
                .param("id", betPackOnboarding.getImages().get(0).getId().toString())
                .param("fileType", ImageFileType)
                .param("imageLabel", "Image 1")
                .param("nextCTAButtonLabel", "NEXT")
                .param("imageType", "Onboarding")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void postBetpackOnboardingTest_5xx() throws Exception {

    given(repository.save(any())).willThrow(new BetPackMarketPlaceException("Invalid data"));

    this.mockMvc
        .perform(
            multipart("/v1/api/bet-pack/onboarding")
                .file(onboardingImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("images[0].imageLabel", "Image 1")
                .param("images[0].nextCTAButtonLabel", "NEXT")
                .param("images[0].imageType", "Onboarding")
                .param("isActive", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void postBetpackOnboardingTest_invalidImageformat_4xx() throws Exception {

    // given(repository.save(any())).willThrow(new BetPackMarketPlaceException("Invalid data"));

    this.mockMvc
        .perform(
            multipart("/v1/api/bet-pack/onboarding")
                .file(invalidOnboardImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("images[0].imageLabel", "Image 1")
                .param("images[0].nextCTAButtonLabel", "NEXT")
                .param("images[0].imageType", "Onboarding")
                .param("isActive", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void putBetpackOnboardingTest_5xx() throws Exception {

    String id = "2";
    betPackOnboarding.setId("1");
    given(repository.findById(any())).willReturn((Optional.of(betPackOnboarding)));

    /* when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
            .thenReturn(Optional.of(getFilename("first_image.png", "test.png")));*/
    given(repository.save(any())).willThrow(new BetPackMarketPlaceException("Invalid data"));
    // given(repository.findById(any())).willThrow(new BetPackMarketPlaceException("Invalid data"));

    this.mockMvc
        .perform(
            multipartPutReq
                .file(onboardingImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("images[0].imageLabel", "Image 1")
                .param("images[0].nextCTAButtonLabel", "NEXT")
                .param("images[0].imageType", "Onboarding")
                .param("isActive", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void putBetpackOnboardingTest_5xx_2() throws Exception {

    String id = "2";
    betPackOnboarding.setId("1");
    // given(repository.findById(any())).willReturn((Optional.of(betPackOnboarding)));

    /* when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
            .thenReturn(Optional.of(getFilename("first_image.png", "test.png")));*/
    /* given(repository.save(any())).willThrow(new BetPackMarketPlaceException("Invalid data"));*/
    given(repository.findById(any())).willThrow(new BetPackMarketPlaceException("Invalid data"));

    this.mockMvc
        .perform(
            multipartPutReq
                .file(onboardingImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("images[0].imageLabel", "Image 1")
                .param("images[0].nextCTAButtonLabel", "NEXT")
                .param("images[0].imageType", "Onboarding")
                .param("isActive", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void putBetpackOnboardingTest_NotFound_4xx() throws Exception {

    given(repository.findById(anyString())).willReturn(Optional.empty());

    // given(repository.findById(any())).willReturn((Optional.of(betPackOnboarding)));
    /*Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
    .thenReturn(Optional.of(getFilename("first_image.png", "test.png")));*/

    this.mockMvc
        .perform(
            multipartPutReq
                .file(onboardingImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("images[0].imageLabel", "Image 1")
                .param("images[0].nextCTAButtonLabel", "NEXT")
                .param("images[0].imageType", "Onboarding")
                .param("isActive", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void putBetpackOnboardingTest_ImageUploadFailed() throws Exception {

    betPackOnboarding.setId("1");
    // betPackOnboarding.setBannerImage(null);
    betPackOnboarding.getImages().get(0).setOnboardImageDetails(null);
    // betPackOnboarding.getImages().get(0).setId(new ObjectId("1"));

    given(repository.findById(any())).willReturn((Optional.of(betPackOnboarding)));
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(Optional.empty());

    this.mockMvc
        .perform(
            multipartPutReq
                .file(onboardingImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("images[0].imageLabel", "Image 1")
                .param("images[0].nextCTAButtonLabel", "NEXT")
                .param("images[0].imageType", "Onboarding")
                .param("isActive", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void postBetpackOnboardingTest_ImageUploadFailed() throws Exception {

    betPackOnboarding.setId("1");
    // betPackOnboarding.setBannerImage(null);
    // betPackOnboarding.getImages().get(0).setOnboardImageDetails(null);
    // betPackOnboarding.getImages().get(0).setId(new ObjectId("1"));

    given(repository.findById(any())).willReturn((Optional.of(betPackOnboarding)));
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), eq(path)))
        .thenReturn(Optional.empty());

    this.mockMvc
        .perform(
            multipart("/v1/api/bet-pack/onboarding")
                .file(onboardingImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("images[0].imageLabel", "Image 1")
                .param("images[0].nextCTAButtonLabel", "NEXT")
                .param("images[0].imageType", "Onboarding")
                .param("isActive", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void getOnBoardDetails_2xx() throws Exception {
    when(repository.findByBrand(anyString())).thenReturn(Arrays.asList(betPackOnboarding));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/bet-pack/onboarding/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void getOnBoardDetails_No_Content() throws Exception {
    when(repository.findByBrand(anyString())).thenReturn(Arrays.asList());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/bet-pack/onboarding/brand/" + BRAND)
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNoContent());
  }

  @Test
  public void getImageTest_2xx() throws Exception {

    when(repository.findById(anyString())).thenReturn(Optional.of(betPackOnboarding));

    String getUrl =
        String.format(
            "/v1/api/bet-pack/onboarding/%s/images/%s",
            "62cd9ce3fa2d927e6d9c18ad", "62cd9dfefa2d927e6d9c18c4");
    this.mockMvc
        .perform(MockMvcRequestBuilders.get(getUrl).contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void getImageTest_5xx() throws Exception {

    when(repository.findById(anyString())).thenReturn(Optional.of(betPackOnboarding));

    String getUrl =
        String.format(
            "/v1/api/bet-pack/onboarding/%s/images/%s", "62cd9ce3fa2d927e6d9c18ad", "1234");
    this.mockMvc
        .perform(MockMvcRequestBuilders.get(getUrl).contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void deleteOnboardingImageTest_2xx() throws Exception {

    String deleteUrl =
        String.format(
            "/v1/api/bet-pack/onboarding/%s/images/%s",
            "62cd9ce3fa2d927e6d9c18ad", "62cd9dfefa2d927e6d9c18c4");

    when(repository.findById(anyString())).thenReturn(Optional.of(betPackOnboarding));
    when(mongoTemplate.updateMulti(any(), any(), eq(BetPackOnboarding.class)))
        .thenReturn(updateResult);

    this.mockMvc
        .perform(MockMvcRequestBuilders.delete(deleteUrl).contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void deleteOnboardingImageTest_5xx() throws Exception {

    String deleteUrl =
        String.format(
            "/v1/api/bet-pack/onboarding/%s/images/%s", "62cd9ce3fa2d927e6d9c18ad", "abcd");

    when(repository.findById(anyString())).thenReturn(Optional.of(betPackOnboarding));
    when(mongoTemplate.updateMulti(any(), any(), eq(BetPackOnboarding.class)))
        .thenReturn(updateResult);

    this.mockMvc
        .perform(MockMvcRequestBuilders.delete(deleteUrl).contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void deleteBpMp_2xx() throws Exception {

    String deleteUrl = String.format("/v1/api/bet-pack/onboarding/%s", betPackOnboarding.getId());
    doNothing().when(repository).deleteById(anyString());

    this.mockMvc
        .perform(MockMvcRequestBuilders.delete(deleteUrl).contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
  }

  @Test
  public void deleteBpMp_5xx() throws Exception {

    String deleteUrl = String.format("/v1/api/bet-pack/onboarding/%s", betPackOnboarding.getId());
    doThrow(new BetPackMarketPlaceException("Id : " + betPackOnboarding.getId() + "doesn't exist"))
        .when(repository)
        .deleteById(anyString());

    this.mockMvc
        .perform(MockMvcRequestBuilders.delete(deleteUrl).contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void testOnboarding() {
    BetPackOnboarding betPackOnboarding = new BetPackOnboarding();
    betPackOnboarding.setBrand("coral");
    assertEquals(betPackOnboarding, betPackOnboarding.content());
  }

  @Test
  public void putBetPackOnboardingImageTest_4xx() throws Exception {

    //    betPackOnboarding.getImages().get(0).setId(null);
    given(repository.findById(any())).willReturn((Optional.empty()));
    // given(repository.save(any())).willThrow(new BetPackMarketPlaceException("Invalid data"));
    this.mockMvc
        .perform(
            multipartImagePutReq
                .file(onboardingImageUpdate)
                .param("id", "1")
                .param("fileType", ImageFileType)
                .param("imageLabel", "Image 1")
                .param("nextCTAButtonLabel", "NEXT")
                .param("imageType", "Onboarding")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void putBetPackOnboardingImageTest_2xx() throws Exception {

    // betPackOnboarding.getImages().get(0).setId(null);
    when(repository.findById(anyString())).thenReturn(Optional.of(betPackOnboarding));
    this.mockMvc
        .perform(
            multipartImagePutReq
                .file(onboardingImageUpdate)
                .param("id", betPackOnboarding.getImages().get(0).getId().toString())
                .param("fileType", ImageFileType)
                .param("imageLabel", "Image 1")
                .param("nextCTAButtonLabel", "NEXT")
                .param("imageType", "Onboarding")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void postBetpackOnboardingTest_WithNLP() throws Exception {

    BetPackOnboarding mockBetPackOnboarding = Mockito.mock(BetPackOnboarding.class);
    given(repository.save(any(BetPackOnboarding.class))).willReturn(mockBetPackOnboarding);
    Mockito.doThrow(NullPointerException.class).when(mockBetPackOnboarding).getId();

    given(repository.findById(any())).willReturn((Optional.of(betPackOnboarding)));

    this.mockMvc
        .perform(
            multipart("/v1/api/bet-pack/onboarding")
                .file(onboardingImage)
                .param("id", "1")
                .param("brand", BRAND)
                .param("fileType", ImageFileType)
                .param("images[0].imageLabel", "Image 1")
                .param("images[0].nextCTAButtonLabel", "NEXT")
                .param("images[0].imageType", "Onboarding")
                .param("isActive", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void putBetPackOnboardingImageNotFoundTest_4xx() throws Exception {

    // betPackOnboarding.getImages().get(0).setId(null);
    when(repository.findById(anyString())).thenReturn(Optional.of(betPackOnboarding));

    this.mockMvc
        .perform(
            multipartImageErrorPutReq
                .file(onboardingImageUpdate)
                .param("id", betPackOnboarding.getImages().get(0).getId().toString())
                .param("fileType", ImageFileType)
                .param("imageLabel", "Image 1")
                .param("nextCTAButtonLabel", "NEXT")
                .param("imageType", "Onboarding")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void putBetPackOnboardingRemoveImageTest_2xx() throws Exception {

    // betPackOnboarding.getImages().get(0).setId(null);
    when(repository.findById(anyString())).thenReturn(Optional.of(betPackOnboarding));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    // onboardingImageUpdate.set
    this.mockMvc
        .perform(
            multipartImagePutReq
                .file(onboardingImageUpdate)
                .param("id", betPackOnboarding.getImages().get(0).getId().toString())
                .param("fileType", ImageFileType)
                .param("imageLabel", "Image 1")
                .param("nextCTAButtonLabel", "NEXT")
                .param("imageType", "Onboarding")
                .param("onboardImageDetails.filename", "abac-123-cser-1456-asfgr.png")
                .param("originalname", "first_image.png")
                .param("path", "/images/uploads/onboarding/betPackOnboarding")
                .param("filetype", "image/png")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void putBetPackOnboardingRemoveImageTest_Exception() throws Exception {

    // betPackOnboarding.getImages().get(0).setId(null);
    when(repository.findById(anyString())).thenReturn(Optional.of(betPackOnboarding));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(false);

    this.mockMvc
        .perform(
            multipartImagePutReq
                .file(onboardingImageUpdate)
                .param("id", betPackOnboarding.getImages().get(0).getId().toString())
                .param("fileType", ImageFileType)
                .param("imageLabel", "Image 1")
                .param("nextCTAButtonLabel", "NEXT")
                .param("imageType", "Onboarding")
                .param("onboardImageDetails.filename", "abac-123-cser-1456-asfgr.png")
                .param("originalname", "first_image.png")
                .param("path", "/images/uploads/onboarding/betPackOnboarding")
                .param("filetype", "image/png")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  private Filename getFilename(String originalFN, String generatedFN) {
    Filename filename = new Filename();
    filename.setOriginalname(originalFN);
    filename.setFilename(generatedFN);
    filename.setPath("/test/path/");
    return filename;
  }
}
