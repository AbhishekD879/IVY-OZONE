package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.assertEquals;

import com.ladbrokescoral.oxygen.cms.api.dto.WidgetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ShowOn;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.Widget;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BybTabAvailabilityService;
import com.ladbrokescoral.oxygen.cms.api.service.WidgetService;
import java.util.Collections;
import java.util.List;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class WidgetPublicServiceTest extends BDDMockito {
  @Mock WidgetService service;
  @Mock SportCategoryRepository sportCategoryRepository;
  @Mock BybTabAvailabilityService bybTabAvailabilityService;

  @Test
  public void findByBrandTest() {
    WidgetPublicService widgetPublicService =
        new WidgetPublicService(service, sportCategoryRepository, bybTabAvailabilityService);

    ShowOn showOn = new ShowOn();
    showOn.setSports(Collections.singletonList("16"));
    Widget widget = new Widget();
    widget.setId("1234");
    widget.setShowOn(showOn);
    widget.setShowOnDesktop(false);
    widget.setShowOnMobile(false);
    widget.setShowOnTablet(false);
    widget.setType("stream");
    when(service.findAllByBrandAndDisabled("bma")).thenReturn(Collections.singletonList(widget));

    SportCategory sportCategory = new SportCategory();
    sportCategory.setTargetUri("targetUri");
    when(sportCategoryRepository.findAllByMatchingIds(Collections.singletonList("16")))
        .thenReturn(Collections.singletonList(sportCategory));

    List<WidgetDto> result = widgetPublicService.findByBrand("bma");
    assertEquals(1, result.size());
  }
}
