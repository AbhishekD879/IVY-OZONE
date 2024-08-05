package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.PromotionWithSectionContainerDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PromotionSection;
import com.ladbrokescoral.oxygen.cms.api.service.PromotionSectionService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.PromotionPublicService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.After;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;

@RunWith(Parameterized.class)
public class PromotionSectionsAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<PromotionSection> {

  @Mock private PromotionPublicService service;
  @Mock private PromotionSectionService promotionSectionService;

  @Getter @InjectMocks private PromotionSectionsAfterSaveListener listener;

  @Getter @Spy private PromotionSection entity;
  @Getter private List<?> collection = null;

  private PromotionWithSectionContainerDto data = new PromotionWithSectionContainerDto();

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "grouped-promotions"},
          {"connect", "api/connect", "grouped-promotions"}
        });
  }

  @Before
  public void init() {
    entity.setId(brand);
    given(service.findByBrandGroupedBySections(anyString())).willReturn(data);
  }

  @After
  public void verify() {

    then(context).should().upload(brand, path, filename, data);
  }
}
