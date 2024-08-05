package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.SsoPage;
import com.ladbrokescoral.oxygen.cms.api.repository.SsoPageExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SsoPageRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.SsoPageService;
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
@WebMvcTest(value = {SsoPages.class, SsoPageService.class})
public class SsoPagesTest extends AbstractControllerTest {
  @MockBean SsoPageRepository repository;
  @MockBean SsoPageExtendedRepository extendedRepository;
  @MockBean ImageService imageService;
  private SsoPage entity;

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
        .perform(multipart("/v1/api/sso-page/9348394894/image").file(file))
        .andExpect(status().is2xxSuccessful());
  }

  private SsoPage createEntity(String id) {
    SsoPage page = new SsoPage();
    page.setTitle("title");
    page.setBrand("bma");
    page.setFilename(createFileNames(id));
    return page;
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
