package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.NavigationPointDto;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.service.NavigationPointService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;

@RunWith(Parameterized.class)
public class NavigationPointAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<NavigationPoint> {

  @Mock private NavigationPointService service;
  @Getter @InjectMocks private NavigationPointsAfterSaveListener listener;

  @Getter @Spy NavigationPoint entity = new NavigationPoint();
  @Getter private List<NavigationPointDto> collection = Arrays.asList(new NavigationPointDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "navigation-points"},
          {"connect", "api/connect", "navigation-points"}
        });
  }

  @Before
  public void init() {
    given(service.getNavigationPointByBrandEnabled(anyString())).willReturn(this.getCollection());
  }

  @Test
  public void shouldAfterSaveEvent() throws Exception {

    // given
    given(getEntity().getBrand()).willReturn(brand);

    // when
    this.getListener()
        .onAfterSave(new AfterSaveEvent<NavigationPoint>(getEntity(), null, "navigationPoint"));

    // then
    if (null != getCollection()) {
      then(context).should().upload(brand, path, filename, getCollection());
    }
  }
}
