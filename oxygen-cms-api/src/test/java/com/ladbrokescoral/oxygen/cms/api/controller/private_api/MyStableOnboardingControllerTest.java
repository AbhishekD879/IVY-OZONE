package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.MyStableOnboardingDto;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.onboarding.MyStableOnboardingController;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.MyStableOnboarding;
import com.ladbrokescoral.oxygen.cms.api.exception.MyStableOnboardingException;
import com.ladbrokescoral.oxygen.cms.api.repository.MyStableOnboardingRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.MyStableOnboardingService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
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

@WebMvcTest(value = {MyStableOnboardingController.class, MyStableOnboardingService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class MyStableOnboardingControllerTest extends AbstractControllerTest {
  @MockBean private MyStableOnboardingRepository repository;
  @MockBean private ImageService imageService;
  @Mock private MyStableOnboardingService myStableOnboardingService;

  public static final String ImageFileType = "png";

  private MyStableOnboarding entity;
  private MyStableOnboardingDto dto;
  private MockMultipartFile multipartFile;

  private MockMultipartHttpServletRequestBuilder multipartPutReq;

  private MockMultipartHttpServletRequestBuilder multipartImagePutReq;

  private MockMultipartFile onboardingImageUpdate;

  ModelMapper mapper = new ModelMapper();

  public static final String JSON_INPUT_BASE_URL = "controller/private_api/";

  private final String path = "/images/uploads/onboarding/my-stable";

  @Before
  public void init() throws IOException {
    dto = createDto();
    multipartPutReq =
        (MockMultipartHttpServletRequestBuilder)
            multipart("/v1/api/my-stable/1/image")
                .with(
                    request -> {
                      request.setMethod(String.valueOf(HttpMethod.PUT));
                      return request;
                    });
    String putUrl = String.format("/v1/api/my-stable/1/image");
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
            "controller/private_api/myStableOnboarding.json", MyStableOnboarding.class);
    entity.setImageUrl("/images/uploads/mystable/medium/9cfea3ed-afd9-4bc4-8584-9acfd04d3cb4.png");
    multipartFile =
        new MockMultipartFile("onboardImg", "test1.png", "image/png", "file".getBytes());
  }

  @Test
  public void testCreateMyStableOnboarding() throws Exception {
    given(repository.save(any(MyStableOnboarding.class))).will(AdditionalAnswers.returnsFirstArg());
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(createFileNames()));
    this.mockMvc
        .perform(
            multipart("/v1/api/my-stable/image")
                .file(multipartFile)
                .param("brand", "bma")
                .param("fileType", "png")
                .param("buttonText", "Onboarding")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateMyStableOnboardingError() throws Exception {

    when(myStableOnboardingService.attachImage(any(), any()))
        .thenThrow(new MyStableOnboardingException("Exception"));

    this.mockMvc
        .perform(
            multipart("/v1/api/my-stable/image")
                .file(multipartFile)
                .param("brand", "bma")
                .param("fileType", "png")
                .param("buttonText", "Onboarding")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void testCreateEachWayOnboardingDto_Exception() throws Exception {
    MyStableOnboarding myStableOnboarding = Mockito.mock(MyStableOnboarding.class);
    dto = createDto();
    when(repository.findById(any())).thenReturn(Optional.ofNullable(null));
    when(repository.save(any())).thenReturn(entity);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/my-stable/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateEachWayOnboardingDtoSave_Exception() throws Exception {
    MyStableOnboarding entity = new MyStableOnboarding();
    entity.setBrand("abc");
    when(repository.findById(any())).thenReturn(Optional.ofNullable(entity));
    when(repository.existsByBrand(anyString())).thenReturn(true);

    when(repository.save(any())).thenThrow(MyStableOnboardingException.class);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/my-stable/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void testCreateEachWayOnboardingDto() throws Exception {
    MyStableOnboarding myStableOnboarding = Mockito.mock(MyStableOnboarding.class);
    when(repository.findById(any())).thenReturn(Optional.of(entity));
    given(repository.save(any(MyStableOnboarding.class))).will(AdditionalAnswers.returnsFirstArg());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/my-stable/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateEachWayOnboardingDtoEntityNull() throws Exception {
    MyStableOnboarding myStableOnboarding = new MyStableOnboarding();

    // entity.setBrand("NotValid");
    entity.setId(null);
    entity.setOnboardImageDetails(null);
    dto.setId(null);
    dto.setBrand(null);

    when(repository.findById(any())).thenReturn(Optional.of(entity));
    given(repository.save(any(MyStableOnboarding.class))).will(AdditionalAnswers.returnsFirstArg());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/my-stable/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void createFailedWithFileUploadError() throws Exception {
    when(repository.findById(any())).thenReturn(Optional.of(entity));
    given(repository.save(any(MyStableOnboarding.class))).will(AdditionalAnswers.returnsFirstArg());
    multipartFile =
        new MockMultipartFile("onboardImg", "test1.png", "image/png", "file".getBytes());
    Mockito.when(imageService.upload(anyString(), any(MockMultipartFile.class), any()))
        .thenThrow(new MyStableOnboardingException("creation error!!"));
    this.mockMvc
        .perform(
            multipart("/v1/api/my-stable/image")
                .file(multipartFile)
                .param("brand", "bma")
                .param("fileType", "png")
                .param("buttonText", "Onboarding")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void createFailedWithFileUpload5xxError() throws Exception {
    when(repository.findById(any())).thenReturn(Optional.of(entity));
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.empty());
    this.mockMvc
        .perform(
            multipart("/v1/api/my-stable/image")
                .file(multipartFile)
                .param("brand", "bma")
                .param("fileType", "png")
                .param("buttonText", "Onboarding")
                .param("onboardImageDetails.filename", "first.png")
                .param("onboardImageDetails.path", "/images/uploads")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void testMyStableOnboardingWhenActiveRecordPresent() throws Exception {

    when(repository.existsByBrand(Mockito.anyString())).thenReturn(true);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/my-stable")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdateMyStableOnboardingIdNotFound() throws Exception {
    String id = "118000004558668682";
    when(repository.findById(id)).thenReturn(Optional.ofNullable(null));
    dto.setId(id);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/my-stable/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdateMyStableOnboardingWhenIdExists() throws Exception {
    when(repository.existsByBrand(Mockito.anyString())).thenReturn(false);
    when(repository.findById(any())).thenReturn(Optional.of(entity));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    given(repository.save(any(MyStableOnboarding.class))).will(AdditionalAnswers.returnsFirstArg());
    String id = "1110212913455091313";
    dto.setId(id);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/my-stable/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToDeleteById() throws Exception {
    this.mockMvc
        .perform(
            delete("/v1/api/my-stable/234344546566767").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadById() throws Exception {
    when(repository.findById(any())).thenReturn(Optional.of(entity));
    given(repository.save(any(MyStableOnboarding.class))).will(AdditionalAnswers.returnsFirstArg());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/my-stable/233")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadByIdNotFound() throws Exception {
    when(repository.findById(any())).thenReturn(Optional.ofNullable(null));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/my-stable/233")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testReadByBrandException() throws Exception {
    when(repository.findByBrand(Mockito.anyString())).thenReturn(null);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/my-stable/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNoContent());
  }

  @Test
  public void testReadByBrandNoContent() throws Exception {
    when(repository.findByBrand(Mockito.anyString())).thenReturn(Arrays.asList());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/my-stable/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNoContent());
  }

  @Test
  public void testReadByBrand() throws Exception {
    MyStableOnboarding entity = mapper.map(createDto(), MyStableOnboarding.class);
    List<MyStableOnboarding> list = new ArrayList<>();
    list.add(entity);
    when(repository.findByBrand(Mockito.anyString())).thenReturn(list);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/my-stable/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUploadImageSuccess() throws Exception {
    MyStableOnboarding entity = createValidEachWayOnboarding(true);
    when(repository.findById(any())).thenReturn(Optional.of(entity));
    given(repository.save(any(MyStableOnboarding.class))).will(AdditionalAnswers.returnsFirstArg());
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(createFileNames()));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/my-stable/image")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUploadImageFailsWhenIdNotExists() throws Exception {

    when(repository.findById(anyString())).thenReturn(Optional.empty());
    when(imageService.upload(
            anyString(),
            any(MockMultipartFile.class),
            anyString(),
            any(ImageServiceImpl.Size.class)))
        .thenReturn(Optional.of(createFileNames()));
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.png", "image/png", "file".getBytes());
    mockMvc
        .perform(multipart("/v1/api/my-stable/1/image").file(file))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUploadSVGImageFailsWhenIdNotExists() throws Exception {

    when(repository.findById(anyString())).thenReturn(Optional.empty());
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(createSVGFileNames()));
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.svg", "image/svg", "file".getBytes());
    mockMvc
        .perform(multipart("/v1/api/my-stable/1/image").file(file))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUploadImageFails_FailedToUpdateImage() throws Exception {
    MyStableOnboarding entity = createValidEachWayOnboarding(true);
    when(repository.findById(anyString())).thenReturn(Optional.of(entity));
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.empty());
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.png", "image/png", "file".getBytes());
    mockMvc
        .perform(multipart("/v1/api/my-stable/1/image").file(file))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUploadImageFails_FailedToUpdateImage_Success() throws Exception {
    MyStableOnboarding entity = createValidEachWayOnboarding(true);
    when(repository.findById(anyString())).thenReturn(Optional.of(entity));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(createFileNames()));
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.png", "image/png", "file".getBytes());
    mockMvc
        .perform(multipart("/v1/api/my-stable/1/image").file(file))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUploadSVGImageFails_FailedToUpdateImage() throws Exception {
    MyStableOnboarding entity = createValidEachWayOnboarding(true);
    when(repository.findById(anyString())).thenReturn(Optional.of(entity));
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.empty());
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.svg", "image/svg", "file".getBytes());
    mockMvc
        .perform(multipart("/v1/api/my-stable/1/image").file(file))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveImageIdNotExists() throws Exception {
    MyStableOnboarding entity = createValidEachWayOnboarding(true);
    when(repository.findById(anyString())).thenReturn(Optional.empty());
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    mockMvc.perform(delete("/v1/api/my-stable/2/image")).andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveImage_FailedtoRemove() throws Exception {
    MyStableOnboarding entity = createValidEachWayOnboarding(true);
    when(repository.findById(anyString())).thenReturn(Optional.of(entity));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(false);

    mockMvc
        .perform(delete(String.format("/v1/api/my-stable/2/image")))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void deleteImage() throws Exception {

    MyStableOnboardingDto dto = createDto();
    when(repository.findById(any())).thenReturn(Optional.of(entity));

    given(repository.save(any(MyStableOnboarding.class))).will(AdditionalAnswers.returnsFirstArg());
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/my-stable/1/images")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk());
    Assert.assertNotNull(entity.getBrand());
  }

  @Test
  public void deleteImageByIdNotFound() throws Exception {

    MyStableOnboardingDto dto = createDto();
    when(repository.findById(any())).thenReturn(Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/my-stable/1/images")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
    Assert.assertNotNull(entity.getBrand());
  }

  @Test
  public void deleteImageElse() throws Exception {

    MyStableOnboardingDto dto = createDto();
    entity.setOnboardImageDetails(null);
    when(repository.findById(any())).thenReturn(Optional.of(entity));

    given(repository.save(any(MyStableOnboarding.class))).will(AdditionalAnswers.returnsFirstArg());
    when(imageService.removeImage(anyString(), anyString())).thenReturn(false);

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/my-stable/1/images")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void deleteImageException() throws Exception {
    given(repository.findById("1")).willReturn(null);
    given(imageService.removeImage(anyString(), anyString())).willReturn(false);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/my-stable/1/images")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void deleteImage5xxServerError() throws Exception {
    entity.setImageUrl(null);
    when(repository.findById(any())).thenReturn(Optional.of(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/my-stable/1/images")
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
            MockMvcRequestBuilders.delete("/v1/api/my-stable/1/images")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void postAttachImageFailed() throws Exception {
    given(imageService.upload(anyString(), any(), anyString())).willReturn(Optional.empty());
    this.mockMvc
        .perform(
            multipart("/v1/api/my-stable/image")
                .file(multipartFile)
                .param("brand", "bma")
                .param("fileType", "png")
                .param("buttonText", "Onboarding")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  private MyStableOnboarding createValidEachWayOnboarding(boolean usefileurl) {
    MyStableOnboarding onboarding = new MyStableOnboarding();
    onboarding.setIsEnable(true);
    onboarding.setId("1");
    onboarding.setBrand("bma");
    onboarding.setButtonText("OK");
    onboarding.setImageUrl("abc.com");
    return onboarding;
  }

  private static Filename createSVGFileNames() {
    Filename filename = new Filename("name.svg");
    filename.setFiletype("svg");
    filename.setOriginalname("ogname.svg");
    filename.setPath("files/images");
    filename.setSize("2");
    filename.setFullPath("files/image");
    filename.setSvg("svg");
    filename.setSvgId("23");
    return filename;
  }

  private MyStableOnboardingDto createDto() {
    MyStableOnboardingDto myStableOnboardingDto = new MyStableOnboardingDto();

    myStableOnboardingDto.setId("1");
    myStableOnboardingDto.setButtonText("OK,Thanks");
    myStableOnboardingDto.setImageUrl("image.com");
    myStableOnboardingDto.setIsEnable(true);
    myStableOnboardingDto.setBrand("bma");
    return myStableOnboardingDto;
  }

  private MyStableOnboarding getmyStableOnboarding() {
    MyStableOnboarding myStableOnboarding = new MyStableOnboarding();
    myStableOnboarding.setBrand("ladbrokes");
    Filename f = new Filename();
    myStableOnboarding.setOnboardImageDetails(createFileNames());
    myStableOnboarding.setButtonText("buttonText");
    return myStableOnboarding;
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
  public void putEachWayOnboardingTest_5xx() throws Exception {
    String id = "2";
    entity.setId("1");
    given(repository.findById(any())).willReturn((Optional.of(entity)));
    given(repository.save(any())).willReturn(entity);
    this.mockMvc
        .perform(
            multipartPutReq
                .file(multipartFile)
                .param("id", "1")
                .param("brand", "bma")
                .param("fileType", "png")
                .param("isActive", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void putBetpackOnboardingTest_5xx_2() throws Exception {

    String id = "2";
    entity.setId("1");
    given(repository.findById(any())).willThrow(new MyStableOnboardingException("Invalid data"));

    this.mockMvc
        .perform(
            multipartPutReq
                .file(onboardingImageUpdate)
                .param("id", "1")
                .param("brand", "bma")
                .param("isActive", "true")
                .contentType(MediaType.MULTIPART_FORM_DATA_VALUE))
        .andExpect(status().is5xxServerError());
  }

  @Test
  public void putBetPackOnboardingImageTest_2xx() throws Exception {

    when(repository.findById(anyString())).thenReturn(Optional.of(entity));
    when(imageService.removeImage(entity.getBrand(), entity.getImageUrl())).thenReturn(true);

    doReturn(Optional.of(createFileNames()))
        .when(imageService)
        .upload(anyString(), any(MockMultipartFile.class), anyString());
    given(repository.save(any(MyStableOnboarding.class))).will(AdditionalAnswers.returnsFirstArg());
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
  public void putMyStableOnboardingImageTest_2xx_Update() throws Exception {

    when(repository.findById(anyString())).thenReturn(Optional.of(entity));
    when(imageService.removeImage(any(), any())).thenReturn(true);
    doReturn(Optional.of(createFileNames()))
        .when(imageService)
        .upload(anyString(), any(MockMultipartFile.class), anyString());
    given(repository.save(any(MyStableOnboarding.class))).will(AdditionalAnswers.returnsFirstArg());
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
  public void putMyStableOnboardingImageTest_2xx_UpdateFalse() throws Exception {

    when(repository.findById(anyString())).thenReturn(Optional.of(entity));
    when(imageService.removeImage(entity.getBrand(), entity.getImageUrl())).thenReturn(false);
    when(imageService.upload(anyString(), any(), anyString()))
        .thenReturn(Optional.of(createFileNames()));
    given(repository.save(any(MyStableOnboarding.class))).will(AdditionalAnswers.returnsFirstArg());
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
  public void putMyStableOnboardingImageTest_2xx_UpdateException() throws Exception {

    when(repository.findById(anyString())).thenReturn(Optional.of(entity));
    when(imageService.removeImage(any(), any())).thenReturn(true);

    when(imageService.upload(anyString(), any(), anyString())).thenReturn(Optional.empty());

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
  public void putMyStableOnboardingImageTest_3xx_UpdateException() throws Exception {

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

    when(repository.findById(anyString())).thenReturn(Optional.of(getmyStableOnboarding()));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);

    doReturn(Optional.of(createFileNames()))
        .when(imageService)
        .upload(anyString(), any(MockMultipartFile.class), anyString());
    given(repository.save(any(MyStableOnboarding.class))).will(AdditionalAnswers.returnsFirstArg());

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
    given(repository.save(any(MyStableOnboarding.class))).will(AdditionalAnswers.returnsFirstArg());
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
    given(repository.save(any(MyStableOnboarding.class))).will(AdditionalAnswers.returnsFirstArg());
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
  public void putBetPackOnboardingImageTest_updatefailed2() throws Exception {
    given(repository.findById(anyString())).willReturn(Optional.ofNullable(entity));
    given(repository.save(any(MyStableOnboarding.class))).will(AdditionalAnswers.returnsFirstArg());
    dto = createDto();
    dto.setOnboardImageDetails(null);
    dto.setOnboardImg(null);
    Mockito.when(imageService.removeImage(anyString(), anyString())).thenReturn(false);
    when(imageService.upload(anyString(), any(), anyString()))
        .thenThrow(new MyStableOnboardingException("save failed"));

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
}
