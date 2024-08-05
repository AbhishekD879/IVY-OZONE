package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.AssetManagement;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.repository.AssetManagementRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SecondaryNameToAssetRepository;
import com.ladbrokescoral.oxygen.cms.api.service.AssetManagementService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.SvgImageParser;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({AssetManagements.class, AssetManagementService.class})
@AutoConfigureMockMvc(addFilters = false)
public class AssetManagementsTest extends AbstractControllerTest {

  @MockBean private AssetManagementRepository repository;

  @MockBean private SecondaryNameToAssetRepository secondaryNameToAssetRepository;
  @MockBean private ImageService imageService;
  @MockBean private SvgImageParser svgImageParser;

  private AssetManagement entity;
  private String path = "/images/uploads/svg";

  @Before
  public void init() {
    entity = createAssetManagement();
    given(repository.findById(any(String.class))).willReturn(Optional.of(entity));
    given(repository.save(any(AssetManagement.class))).will(AdditionalAnswers.returnsFirstArg());
  }

  @Test
  public void uploadImage() throws Exception {

    final MockMultipartFile file =
        new MockMultipartFile("file", "android.svg", "image/svg", "file".getBytes());
    given(repository.findById("1")).willReturn(Optional.of(entity));
    given(imageService.upload(anyString(), any(), eq(path)))
        .willReturn(Optional.of(getFilename("android.svg", "323566.svg")));
    Svg svg = new Svg();
    svg.setSvg("<svg>");
    given(svgImageParser.parse(any())).willReturn(Optional.of(svg));
    this.mockMvc
        .perform(
            multipart("/v1/api/asset-management/uploadimage/1")
                .file("contestLogo", file.getBytes())
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
    Assert.assertNotNull(entity.getBrand());
  }

  @Test
  public void deleteImage() throws Exception {
    given(repository.findById("1")).willReturn(Optional.of(entity));
    given(imageService.removeImage(anyString(), anyString())).willReturn(true);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/asset-management/deleteimage/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
    Assert.assertNotNull(entity.getBrand());
  }

  private static AssetManagement createAssetManagement() {
    AssetManagement assetManagement = new AssetManagement();
    assetManagement.setBrand("ladbrokes");
    assetManagement.setSportId(16);

    return assetManagement;
  }

  private static Filename getFilename(String originalFN, String generatedFN) {
    Filename filename = new Filename();
    filename.setOriginalname(originalFN);
    filename.setFilename(generatedFN);
    filename.setPath("/test/path/");
    return filename;
  }
}
