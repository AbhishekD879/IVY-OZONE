package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Football3DBanner;
import com.ladbrokescoral.oxygen.cms.api.repository.Football3DBannerRepository;
import com.ladbrokescoral.oxygen.cms.api.service.Football3DBannerService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import java.time.Instant;
import java.util.Optional;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@AutoConfigureMockMvc(addFilters = false)
@WebMvcTest(value = {Football3DBanners.class, Football3DBannerService.class})
public class Football3DBannersTest extends AbstractControllerTest {

  @MockBean Football3DBannerRepository repository;
  @MockBean ImageService imageService;

  @Test
  public void testUploadImage() throws Exception {
    String id = "9348394894";
    Football3DBanner entity = createEntity("6789");
    when(repository.findById(id)).thenReturn(Optional.of(entity));
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString(), any()))
        .thenReturn(Optional.of(createFileNames("23")));
    when(imageService.upload(anyString(), any(MockMultipartFile.class), anyString()))
        .thenReturn(Optional.of(createFileNames("538")));
    when(repository.save(any())).thenReturn(entity);

    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.png", "image/png", "file".getBytes());
    this.mockMvc
        .perform(multipart("/v1/api/football-3d-banner/9348394894/image").file(file))
        .andExpect(status().is2xxSuccessful());
  }

  private Football3DBanner createEntity(String id) {
    Football3DBanner banner = new Football3DBanner();
    banner.setTargetUri("targetURI");
    banner.setDisplayDuration(20);
    banner.setId(id);
    banner.setName("name");
    banner.setValidityPeriodEnd(Instant.now());
    banner.setValidityPeriodEnd(Instant.now().plusMillis(1000000));
    banner.setDisabled(false);
    return banner;
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
