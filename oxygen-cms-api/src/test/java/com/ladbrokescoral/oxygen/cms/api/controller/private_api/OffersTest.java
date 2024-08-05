package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Offer;
import com.ladbrokescoral.oxygen.cms.api.repository.OfferExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.OfferRepository;
import com.ladbrokescoral.oxygen.cms.api.service.*;
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
@WebMvcTest(value = {Offers.class, OfferService.class})
public class OffersTest extends AbstractControllerTest {

  @MockBean OfferRepository repository;
  @MockBean OfferExtendedRepository extendedRepository;
  @MockBean OfferModuleService offerModuleService;
  @MockBean ImageService imageService;
  private Offer entity;

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
    final MockMultipartFile file =
        new MockMultipartFile("file", "test1.png", "image/png", "file".getBytes());
    this.mockMvc
        .perform(multipart("/v1/api/offer/9348394894/image").file(file))
        .andExpect(status().is2xxSuccessful());
  }

  private Offer createEntity(String id) {
    Offer offer = new Offer();
    offer.setId(id);
    offer.setModuleName("module name");
    offer.setTargetUri("target URI");
    offer.setDisplayFrom(Instant.now());
    offer.setDisplayTo(Instant.now().plusMillis(1000000));
    offer.setBrand("bma");
    offer.setImage(createFileNames(id));
    return offer;
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
