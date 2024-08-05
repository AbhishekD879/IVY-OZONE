package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.CouponAndMarketSwitcherDto;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.onboarding.CouponAndMarketSwitcherWidget;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CouponAndMarketSwitcher;
import com.ladbrokescoral.oxygen.cms.api.repository.CouponAndMarketSwitcherRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.CouponAndMarketSwitcherWidgetService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {CouponAndMarketSwitcherWidget.class, CouponAndMarketSwitcherWidgetService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
@MockBean(BrandService.class)
public class CouponAndMarketSwitcherWidgetTest extends AbstractControllerTest {
  @MockBean ImageService imageService;
  @MockBean CouponAndMarketSwitcherRepository repository;
  CouponAndMarketSwitcher entity;
  CouponAndMarketSwitcherDto dto;

  ModelMapper mapper = new ModelMapper();

  @Before
  public void init() {
    dto = new CouponAndMarketSwitcherDto();
    dto.setButtonText("Ok,Thanks!");
    dto.setBrand("ladbrokes");
    dto.setIsEnable(true);
    dto.setImageUrl("file.svg");

    entity = mapper.map(dto, CouponAndMarketSwitcher.class);
    entity.setId("121");
    entity.setCreatedBy("system");
    entity.setUpdatedAt(Instant.now());
    when(repository.save(any())).thenReturn(entity);
    when(repository.findById(any())).thenReturn(Optional.of(entity));
  }

  @Test
  public void testCreate() throws Exception {
    when(repository.existsByBrand(Mockito.anyString())).thenReturn(false);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/couponAndMarketSwitcherWidget")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateWhenActiveRecordPresent() throws Exception {
    when(repository.existsByBrand(Mockito.anyString())).thenReturn(true);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/couponAndMarketSwitcherWidget")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdateIdNotFound() throws Exception {
    String id = "111";
    when(repository.findById(id)).thenReturn(Optional.ofNullable(null));
    dto.setId(id);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/couponAndMarketSwitcherWidget/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdate() throws Exception {
    String id = "121";
    dto.setId(id);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/couponAndMarketSwitcherWidget/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(dto)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testToDeleteById() throws Exception {
    this.mockMvc
        .perform(
            delete("/v1/api/couponAndMarketSwitcherWidget/122")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadByIdNotFound() throws Exception {
    when(repository.findById(any())).thenReturn(Optional.ofNullable(null));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/couponAndMarketSwitcherWidget/233")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testReadById() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/couponAndMarketSwitcherWidget/121")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadByBrand() throws Exception {
    List<CouponAndMarketSwitcher> list = new ArrayList<>();
    list.add(entity);
    when(repository.findByBrand(Mockito.anyString())).thenReturn(list);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/couponAndMarketSwitcherWidget/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUploadImageSuccess() throws Exception {
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(createFileNames()));
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.png", "image/png", "file".getBytes());
    this.mockMvc
        .perform(multipart("/v1/api/couponAndMarketSwitcherWidget/1/image").file(file))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUploadSVGImageFails_FailedToUpdateImage() throws Exception {
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.empty());
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.svg", "image/svg", "file".getBytes());
    mockMvc
        .perform(multipart("/v1/api/couponAndMarketSwitcherWidget/1/image").file(file))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveImageSuccess() throws Exception {
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    mockMvc
        .perform(delete("/v1/api/couponAndMarketSwitcherWidget/1/image"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testRemoveImageIdNotExists() throws Exception {
    when(repository.findById(anyString())).thenReturn(Optional.empty());
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    mockMvc
        .perform(delete("/v1/api/couponAndMarketSwitcherWidget/2/image"))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testRemoveImage_FailedtoRemove() throws Exception {
    when(imageService.removeImage(anyString(), anyString())).thenReturn(false);
    mockMvc
        .perform(delete(String.format("/v1/api/couponAndMarketSwitcherWidget/2/image")))
        .andExpect(status().is4xxClientError());
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
}
