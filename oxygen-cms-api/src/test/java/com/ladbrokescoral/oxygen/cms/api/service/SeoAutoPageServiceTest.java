package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertTrue;

import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoAutoPage;
import com.ladbrokescoral.oxygen.cms.api.repository.SeoAutoPageRepository;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;

@WebMvcTest({SeoAutoPage.class, SeoAutoPageService.class})
@AutoConfigureMockMvc(addFilters = false)
public class SeoAutoPageServiceTest extends AbstractControllerTest {

  @MockBean private SeoAutoPageService service;
  @MockBean private SeoAutoPageRepository repository;

  private SeoAutoPage entity = new SeoAutoPage();

  @Before
  public void setUp() {
    service = new SeoAutoPageService(repository);
    entity = prepareEntity();
    given(repository.findByBrand("BMA")).willReturn(Arrays.asList(entity));
  }

  private SeoAutoPage prepareEntity() {
    SeoAutoPage seoAutoPage = new SeoAutoPage();
    seoAutoPage.setId("1");
    seoAutoPage.setBrand("BMA");
    seoAutoPage.setUri("/event");
    seoAutoPage.setMetaTitle("test");
    seoAutoPage.setMetaDescription("test");
    return seoAutoPage;
  }

  @Test
  public void testCreateWithvalidFields() throws Exception {
    when(repository.findAllByBrand("BMA")).thenReturn(Collections.singletonList(entity));
    List<SeoAutoPage> SeoAutoPageList = service.findAllByBrand("BMA");
    verify(repository, times(1)).findAllByBrand("BMA");
    assertTrue(SeoAutoPageList.contains(entity));
  }
}
