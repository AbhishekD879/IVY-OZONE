package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterLogo;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgFilename;
import com.ladbrokescoral.oxygen.cms.api.repository.FooterLogoRepository;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import java.util.Optional;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@RunWith(SpringRunner.class)
@AutoConfigureMockMvc(addFilters = false)
@WebMvcTest(value = {FooterLogos.class, FooterLogoService.class, SvgEntityService.class})
public class FooterLogosTest extends AbstractControllerTest {
  @MockBean FooterLogoRepository repository;
  @MockBean ImageService imageService;
  @MockBean SvgImageParser parser;
  private FooterLogo entity;

  @Test
  public void testDelete() throws Exception {
    when(repository.findById(anyString())).thenReturn(Optional.of(createEntity("99586")));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    this.mockMvc
        .perform(MockMvcRequestBuilders.delete("/v1/api/footer-logo/99586"))
        .andExpect(status().is2xxSuccessful());
  }

  private FooterLogo createEntity(String id) {
    FooterLogo logo = new FooterLogo();
    logo.setId(id);
    logo.setUriMedium("uri medium");
    logo.setUriOriginal("uri original");
    logo.setBrand("bma");
    logo.setFilename(createFileNames(id));
    logo.setSvgFilename(createSvgFilenames());
    return logo;
  }

  private SvgFilename createSvgFilenames() {

    SvgFilename filename = new SvgFilename();
    filename.setFiletype("svg");
    filename.setOriginalname("ogname.svg");
    filename.setPath("files/images");
    filename.setSize(1999);
    filename.setFilename("filename");
    return filename;
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
