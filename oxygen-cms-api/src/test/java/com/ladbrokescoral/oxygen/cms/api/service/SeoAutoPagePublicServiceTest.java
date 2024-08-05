package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.SeoAutoInitDataDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoAutoPage;
import com.ladbrokescoral.oxygen.cms.api.repository.SeoAutoPageRepository;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SeoAutoPagePublicService;
import java.util.Collections;
import java.util.Map;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SeoAutoPagePublicServiceTest {
  @Mock private SeoAutoPageRepository repository;
  private SeoAutoPagePublicService service;
  private String brand = "BMA";

  @Before
  public void init() {
    SeoAutoPageService seoService = new SeoAutoPageService(this.repository);
    this.service = new SeoAutoPagePublicService(seoService);
  }

  @Test
  public void testFindByBrand() {
    SeoAutoPage seoAutoPage = new SeoAutoPage();
    seoAutoPage.setBrand("BMA");
    seoAutoPage.setUri("/event");
    seoAutoPage.setMetaTitle("test");
    seoAutoPage.setMetaDescription("test");
    Mockito.when(this.repository.findAllByBrand(brand))
        .thenReturn(Collections.singletonList(seoAutoPage));
    Map<String, SeoAutoInitDataDto> result = this.service.find(brand);
    Assert.assertEquals(1, result.size());
    Assert.assertEquals("test", result.get("/event").getMetaTitle());
    Assert.assertEquals("test", result.get("/event").getMetaDescription());
  }
}
