package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.mockito.AdditionalAnswers.returnsFirstArg;
import static org.mockito.BDDMockito.given;
import static org.mockito.Matchers.any;
import static org.mockito.Matchers.anyString;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgImage;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgSprite;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.SvgImageService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import java.util.Collections;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

@RunWith(SpringRunner.class)
@WebMvcTest(
    value = {
      Users.class,
      AuthenticationService.class,
      BrandService.class,
      SvgImages.class,
      SvgImageService.class
    })
@AutoConfigureMockMvc(addFilters = false)
public class SvgImagesTest {

  @MockBean private BrandService brandService;
  @MockBean private UserService userServiceMock;

  @MockBean private SvgImageService service;

  @Autowired private MockMvc mockMvc;

  @Before
  public void setUp() {
    given(brandService.findByBrandCode(anyString())).willReturn(Optional.of(new Brand()));

    given(userServiceMock.findOne(anyString())).willReturn(Optional.empty());
    given(service.findOne(anyString())).willReturn(Optional.of(new SvgImage()));

    doAnswer(returnsFirstArg()).when(service).prepareModelBeforeSave(any(SvgImage.class));
    doAnswer(returnsFirstArg()).when(service).save(any(SvgImage.class));
  }

  @Test
  public void testCreateSvgImage() throws Exception {
    doAnswer(returnsFirstArg())
        .when(service)
        .createSvgImage(any(SvgImage.class), any(), anyString());

    final MockMultipartFile file =
        new MockMultipartFile("file", "android.svg", "image/svg", "file".getBytes());
    mockMvc
        .perform(
            multipart("/v1/api/svg-images")
                .file(file)
                .param("svgId", "svg-1")
                .param("brand", "bma")
                .param("sprite", SvgSprite.ADDITIONAL.getSpriteName()))
        .andExpect(status().isCreated());
  }

  @Test
  public void testFailCreateSvgImageWithLargeImage() throws Exception {
    doAnswer(returnsFirstArg())
        .when(service)
        .createSvgImage(any(SvgImage.class), any(), anyString());

    final byte[] largeInput = new byte[60000];
    final MockMultipartFile file =
        new MockMultipartFile("file", "android.svg", "image/svg", largeInput);
    mockMvc
        .perform(
            multipart("/v1/api/svg-images")
                .file(file)
                .param("svgId", "svg-1")
                .param("brand", "bma")
                .param("sprite", SvgSprite.ADDITIONAL.getSpriteName()))
        .andExpect(status().isBadRequest());
  }

  @Test
  public void testUploadSvg_OK() throws Exception {
    when(service.replaceSvgImage(anyString(), any(MockMultipartFile.class), any(SvgImage.class)))
        .thenReturn(new SvgImage());
    when(service.update(any(SvgImage.class), any(SvgImage.class))).thenReturn(new SvgImage());

    MockMultipartFile file =
        new MockMultipartFile("file", "android.svg", "image/png", "file".getBytes());
    mockMvc
        .perform(
            multipart("/v1/api/svg-images/1")
                .file(file)
                .param("svgId", "svg-1")
                .param("brand", "bma"))
        .andExpect(status().isOk());
  }

  @Test
  public void readByBrand_OK() throws Exception {
    SvgImage svg = new SvgImage();
    given(service.searchByBrand("bma", null, null)).willReturn(Collections.singletonList(svg));

    mockMvc
        .perform(get(String.format("/v1/api/svg-images/brand/%s", "bma")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void readByBrandAndSprite_OK() throws Exception {
    SvgImage svg = new SvgImage();
    given(service.findAllByBrandAndSprite("bma", "virtual"))
        .willReturn(Collections.singletonList(svg));

    mockMvc
        .perform(get(String.format("/v1/api/svg-images/brand/%s/sprite/%s", "bma", "virtual")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void readByBrandWithFilter_OK() throws Exception {
    SvgImage svg = new SvgImage();
    given(service.searchByBrand("bma", "some text", false))
        .willReturn(Collections.singletonList(svg));

    mockMvc
        .perform(
            get(
                String.format(
                    "/v1/api/svg-images/brand/%s?search=%s&active=%s", "bma", "some text", false)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void read_OK() throws Exception {
    mockMvc
        .perform(get(String.format("/v1/api/svg-images/%s", "id")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void read_Sprites() throws Exception {

    mockMvc
        .perform(get(String.format("/v1/api/svg-images/brand/%s/sprites", "id")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void delete_OK() throws Exception {
    mockMvc
        .perform(delete(String.format("/v1/api/svg-images/%s", "id")))
        .andExpect(status().is2xxSuccessful());
  }
}
