package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.repository.PromotionRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.PromotionSectionRepository;
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
@WebMvcTest(
    value = {
      Promotions.class,
      PromotionService.class,
      WysiwygService.class,
      PromotionSectionService.class
    })
public class PromotionsTest extends AbstractControllerTest {
  @MockBean PromotionRepository repository;
  @MockBean ImageService imageService;
  @MockBean PromotionSectionRepository promotionSectionRepository;
  @MockBean PromotionLeaderboardMsgPublishService promotionLeaderboardMsgPublishService;
  @MockBean PromoLeaderboardValidationService promoLeaderboardValidationService;
  @MockBean NavItemService navItemService;
  private Promotion entity;

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
        .perform(multipart("/v1/api/promotion/9348394894/image").file(file))
        .andExpect(status().is2xxSuccessful());
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

  private Promotion createEntity(String id) {
    Promotion promotion = new Promotion();
    promotion.setBrand("bma");
    promotion.setPromoKey("promo key");
    promotion.setShortDescription("short desc");
    promotion.setTitle("title");
    promotion.setValidityPeriodEnd(Instant.now().plusMillis(10000));
    promotion.setValidityPeriodStart(Instant.now());
    promotion.setShowToCustomer("show to customer");
    return promotion;
  }
}
