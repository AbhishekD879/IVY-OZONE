package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Feature;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.repository.FeatureExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.FeatureRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FeatureService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.WysiwygService;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@AutoConfigureMockMvc(addFilters = false)
@WebMvcTest(value = {Features.class, FeatureService.class, WysiwygService.class})
public class FeaturesTest extends AbstractControllerTest {

  @MockBean ImageServiceImpl.Size medium;

  @MockBean ImageService imageService;
  @MockBean FeatureExtendedRepository extendedRepository;
  @MockBean FeatureRepository repository;
  private Feature entity;

  @Before
  public void init() {
    String id = "9348394894";
    entity = createEntity("6789");
    when(repository.findById(id)).thenReturn(Optional.of(entity));
    when(repository.save(any())).thenReturn(entity);
  }

  @Test
  public void testUploadImage() throws Exception {
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString(), any()))
        .thenReturn(Optional.of(createFileNames("23")));
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(createFileNames("538")));
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.png", "image/png", "file".getBytes());
    this.mockMvc
        .perform(multipart("/v1/api/feature/9348394894/image").file(file))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testRemoveImage() throws Exception {
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    this.mockMvc
        .perform(delete("/v1/api/feature/9348394894/image"))
        .andExpect(status().is2xxSuccessful());
  }

  private Feature createEntity(String id) {

    Feature feature = new Feature();
    feature.setBrand("bma");
    feature.setId(id);
    feature.setShowToCustomer("show to customer");
    feature.setUriMedium("uriMedium");
    feature.setFilename(createFileNames("8699"));
    return feature;
  }

  private static Filename createFileNames(String id) {
    Filename filename = new Filename("name.png");
    filename.setFiletype("png");
    filename.setOriginalname("ogname.png");
    filename.setPath("files/images");
    filename.setSize("2");
    filename.setFullPath("files/image");
    filename.setSvg("svg");
    filename.setSvgId(id);
    return filename;
  }
}
