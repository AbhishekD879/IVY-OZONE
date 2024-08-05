package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideSplashPage;
import com.ladbrokescoral.oxygen.cms.api.repository.FreeRideSplashPageRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FreeRideSplashPageService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FreeRideSplashPagePublicService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest({FreeRideSplashPageApi.class, FreeRideSplashPagePublicService.class})
@Import(ModelMapperConfig.class)
@AutoConfigureMockMvc(addFilters = false)
public class FreeRideSplashPageApiTest extends AbstractControllerTest {

  @MockBean private FreeRideSplashPageRepository repository;
  @MockBean private FreeRideSplashPageService service;
  private FreeRideSplashPage freeRideSplashPage;
  private List<FreeRideSplashPage> splashPageList;
  public static final String BRAND = "ladbrokes";

  @Before
  public void init() throws IOException {
    freeRideSplashPage = new FreeRideSplashPage();
    freeRideSplashPage.setId("1");
    freeRideSplashPage.setBrand(BRAND);
    freeRideSplashPage.setWelcomeMsg("Free Bet");
    freeRideSplashPage.setTermsAndCondition("T and C");
    freeRideSplashPage.setTermsAndConditionLink("https://TAndC");
    freeRideSplashPage.setTermsAndConditionHyperLinkText("This is the text for the link");
    freeRideSplashPage.setButtonText("Lets go");
    splashPageList = new ArrayList<>();
  }

  @Test
  public void freeRideSplashPageByBrand() throws Exception {
    freeRideSplashPage.setSplashImage(getFilename("test1.png", "Splash.png"));
    freeRideSplashPage.setBannerImage(getFilename("test2.png", "banner.png"));
    freeRideSplashPage.setFreeRideLogo(getFilename("test3.png", "FRlogo.png"));
    splashPageList.add(freeRideSplashPage);
    given(service.getFreeRideSplashPageByBrand(anyString())).willReturn(splashPageList);
    given(repository.findAllByBrand(anyString())).willReturn(splashPageList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/" + BRAND + "/freeride-splashpage")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void freeRideSplashPageByBrandWithoutImage() throws Exception {
    splashPageList.add(freeRideSplashPage);
    given(service.getFreeRideSplashPageByBrand(anyString())).willReturn(splashPageList);
    given(repository.findAllByBrand(anyString())).willReturn(splashPageList);
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/cms/api/" + BRAND + "/freeride-splashpage")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private Filename getFilename(String originalFN, String generatedFN) {
    Filename filename = new Filename();
    filename.setOriginalname(originalFN);
    filename.setFilename(generatedFN);
    filename.setPath("/test/path");
    filename.setFiletype("image/png");
    return filename;
  }
}
