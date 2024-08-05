package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.junit.Assert.assertEquals;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.CrcOnBoardingDto;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.onboarding.CrcOnBoardingController;
import com.ladbrokescoral.oxygen.cms.api.dto.CrcOnBoardingCFDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CrcOnBoarding;
import com.ladbrokescoral.oxygen.cms.api.exception.CrcOnBoardingException;
import com.ladbrokescoral.oxygen.cms.api.repository.CrcOnBoardingRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.CrcOnBoardingService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = {CrcOnBoardingController.class, CrcOnBoardingService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class CrcOnBoardingControllerTest extends AbstractControllerTest {
  @MockBean private CrcOnBoardingRepository repository;
  @MockBean private ImageService imageService;
  @Mock private CrcOnBoardingService crcOnboardingService;

  public static final String ImageFileType = "png";

  private CrcOnBoarding entity;
  private CrcOnBoardingDto dto;
  private MockMultipartFile multipartFile;

  private MockMultipartHttpServletRequestBuilder multipartPutReq;

  private MockMultipartHttpServletRequestBuilder multipartImagePutReq;

  private MockMultipartFile onboardingImageUpdate;

  ModelMapper mapper = new ModelMapper();

  public static final String JSON_INPUT_BASE_URL = "controller/private_api/";

  private final String path = "/images/uploads/onboarding/crc";

  @Before
  public void init() throws IOException {
    dto = createDto();
    multipartPutReq =
        (MockMultipartHttpServletRequestBuilder)
            multipart("/v1/api/crc-onboarding/1/image")
                .with(
                    request -> {
                      request.setMethod(String.valueOf(HttpMethod.PUT));
                      return request;
                    });
    String putUrl = "/v1/api/crc-onboarding/1/image";

    onboardingImageUpdate =
        new MockMultipartFile("onboardImg", "first_image.png", "image/png", "file".getBytes());

    multipartImagePutReq =
        (MockMultipartHttpServletRequestBuilder)
            multipart(putUrl)
                .with(
                    request -> {
                      request.setMethod(String.valueOf(HttpMethod.PUT));
                      return request;
                    });

    entity =
        TestUtil.deserializeWithJackson(
            "controller/private_api/crcOnboarding.json", CrcOnBoarding.class);
    entity.setImageUrl("/images/uploads/crc/medium/9cfea3ed-afd9-4bc4-8584-9acfd04d3cb4.png");
    multipartFile =
        new MockMultipartFile("onboardImg", "test1.png", "image/png", "file".getBytes());
  }

  @Test
  public void testCreateCrcOnboarding() throws Exception {
    given(repository.save(any(CrcOnBoarding.class))).will(AdditionalAnswers.returnsFirstArg());
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(createFileNames()));
    this.mockMvc
        .perform(
            multipart("/v1/api/crc-onboarding/image")
                .file(multipartFile)
                .param("brand", "bma")
                .param("fileType", "png")
                .param("buttonText", "Onboarding")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateEachWayOnboardingDto_Exception() throws Exception {
    dto = createDto();
    when(repository.findById(any())).thenReturn(Optional.ofNullable(null));
    when(repository.save(any())).thenReturn(entity);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/crc-onboarding/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateEachWayOnboardingDtoSave_Exception() throws Exception {
    CrcOnBoarding entityData = new CrcOnBoarding();
    entityData.setBrand("abc");
    when(repository.findById(any())).thenReturn(Optional.ofNullable(entityData));
    when(repository.existsByBrand(anyString())).thenReturn(true);

    when(repository.save(any())).thenThrow(CrcOnBoardingException.class);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/crc-onboarding/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entityData)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void testCreateEachWayOnboardingDtoEntityNull() throws Exception {

    entity.setId(null);
    entity.setOnboardImageDetails(null);
    dto.setId(null);
    dto.setBrand(null);

    when(repository.findById(any())).thenReturn(Optional.of(entity));
    given(repository.save(any(CrcOnBoarding.class))).will(AdditionalAnswers.returnsFirstArg());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/crc-onboarding/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateCrcOnboardingIdNotFound() throws Exception {
    String id = "118000004558668682";
    when(repository.findById(id)).thenReturn(Optional.ofNullable(null));
    dto.setId(id);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/crc-onboarding/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdateCrcOnboardingWhenIdExists() throws Exception {
    when(repository.existsByBrand(Mockito.anyString())).thenReturn(false);
    when(repository.findById(any())).thenReturn(Optional.of(entity));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    given(repository.save(any(CrcOnBoarding.class))).will(AdditionalAnswers.returnsFirstArg());
    String id = "1110212913455091313";
    dto.setId(id);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/crc-onboarding/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToDeleteById() throws Exception {
    this.mockMvc
        .perform(
            delete("/v1/api/crc-onboarding/234344546566767")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadByBrand() throws Exception {
    CrcOnBoarding entityInfo = mapper.map(createDto(), CrcOnBoarding.class);
    List<CrcOnBoarding> list = new ArrayList<>();
    list.add(entityInfo);
    when(repository.findByBrand(Mockito.anyString())).thenReturn(list);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/crc-onboarding/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadByBrand_NoContent() throws Exception {
    when(repository.findByBrand(Mockito.anyString())).thenReturn(Collections.emptyList());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/crc-onboarding/brand/content")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNoContent());
  }

  @Test
  public void testUploadImageSuccess() throws Exception {
    CrcOnBoarding entityCollection = createValidEachWayOnboarding();
    when(repository.findById(any())).thenReturn(Optional.of(entityCollection));
    given(repository.save(any(CrcOnBoarding.class))).will(AdditionalAnswers.returnsFirstArg());
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(createFileNames()));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/crc-onboarding/image")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void deleteImage() throws Exception {

    when(repository.findById(any())).thenReturn(Optional.of(entity));

    given(repository.save(any(CrcOnBoarding.class))).will(AdditionalAnswers.returnsFirstArg());
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/crc-onboarding/1/images")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
    Assert.assertNotNull(entity.getBrand());
  }

  @Test
  public void deleteImageByIdNotFound() throws Exception {

    when(repository.findById(any())).thenReturn(Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/crc-onboarding/1/images")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
    Assert.assertNotNull(entity.getBrand());
  }

  @Test
  public void deleteImageElse() throws Exception {

    entity.setOnboardImageDetails(null);
    when(repository.findById(any())).thenReturn(Optional.of(entity));

    given(repository.save(any(CrcOnBoarding.class))).will(AdditionalAnswers.returnsFirstArg());
    when(imageService.removeImage(anyString(), anyString())).thenReturn(false);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/crc-onboarding/1/images")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void deleteImageFailed() throws Exception {
    entity.setImageUrl(null);

    when(repository.findById(any())).thenReturn(Optional.of(entity));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(false);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/crc-onboarding/1/images")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void postAttachImageFailed() throws Exception {
    given(imageService.upload(anyString(), any(), anyString())).willReturn(Optional.empty());
    this.mockMvc
        .perform(
            multipart("/v1/api/crc-onboarding/image")
                .file(multipartFile)
                .param("brand", "bma")
                .param("fileType", "png")
                .param("buttonText", "Onboarding")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  private CrcOnBoarding createValidEachWayOnboarding() {
    CrcOnBoarding onboarding = new CrcOnBoarding();
    onboarding.setIsEnable(true);
    onboarding.setId("1");
    onboarding.setBrand("bma");
    onboarding.setButtonText("OK");
    onboarding.setImageUrl("abc.com");
    return onboarding;
  }

  private CrcOnBoardingDto createDto() {
    CrcOnBoardingDto crcOnboardingDto = new CrcOnBoardingDto();

    crcOnboardingDto.setId("1");
    crcOnboardingDto.setButtonText("OK,Thanks");
    crcOnboardingDto.setImageUrl("image.com");
    crcOnboardingDto.setIsEnable(true);
    crcOnboardingDto.setBrand("bma");
    return crcOnboardingDto;
  }

  private CrcOnBoarding getcrcOnboarding() {
    CrcOnBoarding crcOnboarding = new CrcOnBoarding();
    crcOnboarding.setBrand("ladbrokes");
    crcOnboarding.setOnboardImageDetails(createFileNames());
    crcOnboarding.setButtonText("buttonText");
    return crcOnboarding;
  }

  private static Filename createFileNames() {
    Filename filename = new Filename("name.png");
    filename.setFiletype("png");
    filename.setOriginalname("ogname.png");
    filename.setPath("files/images");
    filename.setSize("2");
    filename.setFullPath("files/image");
    filename.setSvg("svg");
    filename.setSvgId("23");
    return filename;
  }

  @Test
  public void putCrcOnboardingImageTest_2xx_Update() throws Exception {

    when(repository.findById(anyString())).thenReturn(Optional.of(entity));
    when(imageService.removeImage(any(), any())).thenReturn(true);
    doReturn(Optional.of(createFileNames()))
        .when(imageService)
        .upload(anyString(), any(MockMultipartFile.class), anyString());
    given(repository.save(any(CrcOnBoarding.class))).will(AdditionalAnswers.returnsFirstArg());
    this.mockMvc
        .perform(
            multipartImagePutReq
                .file(multipartFile)
                .param("brand", "bma")
                .param("fileType", "png")
                .param("buttonText", "Onboarding")
                .param("onboardImageDetails.filename", "onboarding.png")
                .param("onboardImageDetails.path", "/images/uploads")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void putCrcOnboardingImageTest_2xx_UpdateFalse() throws Exception {

    when(repository.findById(anyString())).thenReturn(Optional.of(entity));
    when(imageService.removeImage(entity.getBrand(), entity.getImageUrl())).thenReturn(false);
    when(imageService.upload(anyString(), any(), anyString()))
        .thenReturn(Optional.of(createFileNames()));
    given(repository.save(any(CrcOnBoarding.class))).will(AdditionalAnswers.returnsFirstArg());
    this.mockMvc
        .perform(
            multipartImagePutReq
                .file(multipartFile)
                .param("brand", "bma")
                .param("fileType", "png")
                .param("buttonText", "Onboarding")
                .param("onboardImageDetails.filename", "onboarding.png")
                .param("onboardImageDetails.path", "/images/uploads")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void putCrcOnboardingImageTest_3xx_UpdateException() throws Exception {

    when(repository.findById(anyString())).thenReturn(Optional.of(entity));
    when(imageService.removeImage(any(), any())).thenReturn(true);
    when(imageService.upload(anyString(), any(), anyString())).thenReturn(Optional.empty());
    when(repository.save(any())).thenReturn(entity);

    this.mockMvc
        .perform(
            multipartImagePutReq
                .file(multipartFile)
                .param("brand", "bma")
                .param("fileType", "png")
                .param("buttonText", "Onboarding")
                .param("onboardImageDetails.filename", "onboarding.png")
                .param("onboardImageDetails.path", "/images/uploads")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void putBetPackOnboardingImageTest_2xx_1() throws Exception {

    when(repository.findById(anyString())).thenReturn(Optional.of(getcrcOnboarding()));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);

    doReturn(Optional.of(createFileNames()))
        .when(imageService)
        .upload(anyString(), any(MockMultipartFile.class), anyString());
    given(repository.save(any(CrcOnBoarding.class))).will(AdditionalAnswers.returnsFirstArg());

    this.mockMvc
        .perform(
            multipartImagePutReq
                .file(multipartFile)
                .param("brand", "bma")
                .param("fileType", "png")
                .param("buttonText", "Onboarding")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void putBetPackOnboardingImageTest_NotFoundException() throws Exception {

    given(repository.findById(anyString())).willReturn(Optional.empty());

    this.mockMvc
        .perform(
            multipartImagePutReq
                .file(multipartFile)
                .param("brand", "bma")
                .param("fileType", "png")
                .param("buttonText", "Onboarding")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void putBetPackOnboardingImageTest_updatefailed() throws Exception {
    given(repository.findById(anyString())).willReturn(Optional.ofNullable(entity));
    given(repository.save(any(CrcOnBoarding.class))).will(AdditionalAnswers.returnsFirstArg());
    dto = createDto();
    dto.setOnboardImg(null);
    dto.setOnboardImageDetails(null);

    this.mockMvc
        .perform(
            multipartImagePutReq
                .file(new MockMultipartFile("Shifu", (String) null, (String) null, (byte[]) null))
                .param("brand", "bma")
                .param("fileType", "png")
                .param("buttonText", "Onboarding")
                .content(TestUtil.convertObjectToJsonBytes(dto))
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void putBetPackOnboardingImageTest_updatefailed1() throws Exception {
    given(repository.findById(anyString())).willReturn(Optional.ofNullable(entity));
    given(repository.save(any(CrcOnBoarding.class))).will(AdditionalAnswers.returnsFirstArg());
    dto = createDto();
    dto.setOnboardImg(null);
    dto.setOnboardImageDetails(null);

    Mockito.when(imageService.removeImage(anyString(), anyString())).thenReturn(false);

    this.mockMvc
        .perform(
            multipartImagePutReq
                .file(multipartFile)
                .param("brand", "bma")
                .param("fileType", "png")
                .param("buttonText", "Onboarding")
                .content(TestUtil.convertObjectToJsonBytes(dto))
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void testConvertToCFDto() {
    crcOnboardingService = new CrcOnBoardingService(null, null, null, null, mapper);
    CrcOnBoarding entityObj = new CrcOnBoarding();
    Optional<CrcOnBoardingCFDto> result = crcOnboardingService.convertToCFDto(entityObj);
    assertEquals(Optional.of(new CrcOnBoardingCFDto()), result);
  }
}
