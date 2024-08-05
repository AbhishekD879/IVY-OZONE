package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.HRQuickLink;
import com.ladbrokescoral.oxygen.cms.api.repository.HRQuickLinkRepository;
import com.ladbrokescoral.oxygen.cms.api.service.HRQuickLinkService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import java.time.Instant;
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
@WebMvcTest(value = {HRQuickLinks.class, HRQuickLinkService.class})
public class HRQuickLinksTest extends AbstractControllerTest {
  @MockBean HRQuickLinkRepository repository;
  @MockBean ImageService imageService;
  private HRQuickLink entity;

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
        .perform(multipart("/v1/api/hr-quick-link/9348394894/image").file(file))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testRemoveImage() throws Exception {
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    this.mockMvc
        .perform(delete("/v1/api/hr-quick-link/9348394894/image"))
        .andExpect(status().is2xxSuccessful());
  }

  private HRQuickLink createEntity(String id) {
    HRQuickLink link = new HRQuickLink();
    link.setBrand("bma");
    link.setTarget("target");
    link.setValidityPeriodEnd(Instant.now().plusMillis(10000));
    link.setValidityPeriodStart(Instant.now());
    link.setDisabled(false);
    link.setFilename(createFileNames(id));
    link.setUriMedium("uriMedium");
    return link;
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
