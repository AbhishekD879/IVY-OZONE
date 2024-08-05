package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoPage;
import com.ladbrokescoral.oxygen.cms.api.service.SeoPageService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SeoPagePublicService;
import java.util.List;
import java.util.Map;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.http.ResponseEntity;

@RunWith(MockitoJUnitRunner.class)
public class SeoPageApiTest {

  private SeoPagePublicService seoPageService;
  @Mock private SeoPageService service;

  private SeoPageApi seoPageApi;

  @Before
  public void init() {
    seoPageService = new SeoPagePublicService(service);
    seoPageApi = new SeoPageApi(seoPageService);
  }

  @Test
  public void testFindByBrand() throws Exception {
    List<SeoPage> seoPages =
        TestUtil.deserializeListWithJackson("controller/public_api/seoPages.json", SeoPage.class);

    when(service.findAllByBrandAndDisabled("bma")).thenReturn(seoPages);
    ResponseEntity response = seoPageApi.findByBrand("bma");
    Map<String, String> responseMap = (Map<String, String>) response.getBody();

    assertEquals(2, responseMap.size());
    assertEquals("5746afad99780489e0f04c95", responseMap.get("/football"));
    assertEquals("5746b66799780489e0f04c9802", responseMap.get("/volleyball"));
  }
}
