package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.CouponStatsWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.onboarding.CouponStatsWidgets;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CouponStatsWidget;
import com.ladbrokescoral.oxygen.cms.api.repository.CouponStatsWidgetRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.CouponStatsWidgetService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@WebMvcTest(value = {CouponStatsWidgets.class, CouponStatsWidgetService.class, ModelMapper.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
@MockBean(BrandService.class)
public class CouponStatsWidgetTest extends AbstractControllerTest {
  @MockBean CouponStatsWidgetRepository repository;
  @MockBean ImageService imageService;
  CouponStatsWidget entity;
  CouponStatsWidgetDto dto;
  ModelMapper mapper = new ModelMapper();

  @Before
  public void init() {
    dto = createDto();
    CouponStatsWidget entity = mapper.map(dto, CouponStatsWidget.class);
    entity.setId("12121212121");
    entity.setCreatedBy("system");
    entity.setUpdatedAt(Instant.now());
    when(repository.save(any())).thenReturn(entity);
    when(repository.findById(any())).thenReturn(Optional.of(entity));
  }

  @Test
  public void testCreateCouponStatsWidget() throws Exception {
    when(repository.existsByBrand(Mockito.anyString())).thenReturn(false);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/coupon-stats-widget")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateCouponStatsWidgetWhenActiveRecordPresent() throws Exception {
    when(repository.existsByBrand(Mockito.anyString())).thenReturn(true);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/coupon-stats-widget")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdateCouponStatsWidgetIdNotFound() throws Exception {
    String id = "118000004558668682";
    when(repository.findById(id)).thenReturn(Optional.ofNullable(null));
    dto.setId(id);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/coupon-stats-widget/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdateCouponStatsWidgetWhenIdExists() throws Exception {
    when(repository.existsByBrand(Mockito.anyString())).thenReturn(false);
    String id = "1110212913455091313";
    dto.setId(id);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/coupon-stats-widget/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToDeleteById() throws Exception {
    this.mockMvc
        .perform(
            delete("/v1/api/coupon-stats-widget/234344546566767")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/coupon-stats-widget/233")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadByIdNotFound() throws Exception {
    when(repository.findById(any())).thenReturn(Optional.ofNullable(null));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/coupon-stats-widget/233")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testReadByBrandException() throws Exception {
    when(repository.findByBrand(Mockito.anyString())).thenReturn(null);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/coupon-stats-widget/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testReadByBrand() throws Exception {
    CouponStatsWidget entity = mapper.map(createDto(), CouponStatsWidget.class);
    List<CouponStatsWidget> list = new ArrayList<>();
    list.add(entity);
    when(repository.findByBrand(Mockito.anyString())).thenReturn(list);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/coupon-stats-widget/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUploadImageSuccess() throws Exception {
    CouponStatsWidget entity = createValidCouponStatsWidget(true);
    when(repository.findById(anyString())).thenReturn(Optional.of(entity));
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(createFileNames()));
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.png", "image/png", "file".getBytes());
    this.mockMvc
        .perform(multipart("/v1/api/coupon-stats-widget/1/image").file(file))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUploadSVGImageSuccess() throws Exception {
    CouponStatsWidget entity = createValidCouponStatsWidget(true);
    when(repository.findById(anyString())).thenReturn(Optional.of(entity));
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(createSVGFileNames()));
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.svg", "image/svg", "file".getBytes());
    this.mockMvc
        .perform(multipart("/v1/api/coupon-stats-widget/1/image").file(file))
        .andExpect(status().is2xxSuccessful())
        .andDo(result -> result.getResponse())
        .andExpect(result -> result.getResponse());
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
        .perform(multipart("/v1/api/coupon-stats-widget/1/image").file(file))
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
        .perform(multipart("/v1/api/coupon-stats-widget/1/image").file(file))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUploadImageFails_FailedToUpdateImage() throws Exception {
    CouponStatsWidget entity = createValidCouponStatsWidget(true);
    when(repository.findById(anyString())).thenReturn(Optional.of(entity));
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.empty());
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.png", "image/png", "file".getBytes());
    mockMvc
        .perform(multipart("/v1/api/coupon-stats-widget/1/image").file(file))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUploadSVGImageFails_FailedToUpdateImage() throws Exception {
    CouponStatsWidget entity = createValidCouponStatsWidget(true);
    when(repository.findById(anyString())).thenReturn(Optional.of(entity));
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.empty());
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.svg", "image/svg", "file".getBytes());
    mockMvc
        .perform(multipart("/v1/api/coupon-stats-widget/1/image").file(file))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveImageSuccess() throws Exception {
    CouponStatsWidget entity = createValidCouponStatsWidget(true);
    when(repository.findById("1")).thenReturn(Optional.of(entity));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    mockMvc
        .perform(delete("/v1/api/coupon-stats-widget/2/image"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testRemoveImageIdNotExists() throws Exception {
    CouponStatsWidget entity = createValidCouponStatsWidget(true);
    when(repository.findById(anyString())).thenReturn(Optional.empty());
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    mockMvc
        .perform(delete("/v1/api/coupon-stats-widget/2/image"))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveImage_FailedtoRemove() throws Exception {
    CouponStatsWidget entity = createValidCouponStatsWidget(true);
    when(repository.findById(anyString())).thenReturn(Optional.of(entity));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(false);
    mockMvc
        .perform(delete(String.format("/v1/api/coupon-stats-widget/2/image")))
        .andExpect(status().is4xxClientError());
  }

  private CouponStatsWidgetDto createDto() {
    CouponStatsWidgetDto couponStatsWidgetDto = new CouponStatsWidgetDto();
    couponStatsWidgetDto.setButtonText("OK,Thanks");
    couponStatsWidgetDto.setImageUrl("image.com");
    couponStatsWidgetDto.setIsEnable(true);
    couponStatsWidgetDto.setDisplayFrom(Instant.now());
    couponStatsWidgetDto.setDisplayTo(Instant.now());
    couponStatsWidgetDto.setBrand("bma");
    return couponStatsWidgetDto;
  }

  private CouponStatsWidget createValidCouponStatsWidget(boolean usefileurl) {
    CouponStatsWidget widget = new CouponStatsWidget();
    widget.setIsEnable(true);
    widget.setId("1");
    widget.setBrand("bma");
    widget.setButtonText("OK");
    widget.setDisplayFrom(Instant.now());
    widget.setDisplayTo(Instant.now().plus(Duration.ofDays(5)));
    widget.setImageUrl("abc.com");
    return widget;
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
}
