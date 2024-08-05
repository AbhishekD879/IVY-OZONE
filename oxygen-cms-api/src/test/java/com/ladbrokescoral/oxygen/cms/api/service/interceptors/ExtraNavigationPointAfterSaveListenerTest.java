package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.ExtraNavigationPointPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ExtraNavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ExtraNavigationPointPublicService;
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
public class ExtraNavigationPointAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<ExtraNavigationPoint> {

  @Mock private ExtraNavigationPointPublicService service;
  @Getter @InjectMocks private ExtraNavigationPointAfterSaveListener listener;

  @Getter @Spy ExtraNavigationPoint entity = new ExtraNavigationPoint();

  @Getter
  private List<ExtraNavigationPointPublicDto> collection =
      Arrays.asList(new ExtraNavigationPointPublicDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "extra-navigation-points"},
          {"connect", "api/connect", "extra-navigation-points"}
        });
  }

  @Before
  public void init() {
    given(service.findAllActiveExtraNavPointsByBrand(anyString())).willReturn(this.getCollection());
  }

  @Test
  public void shouldAfterSaveEvent() throws Exception {

    // given
    given(getEntity().getBrand()).willReturn(brand);

    // when
    this.getListener().onAfterSave(new AfterSaveEvent<>(getEntity(), null, "extraNavigationPoint"));

    // then
    if (null != getCollection()) {
      then(context).should().upload(brand, path, filename, getCollection());
    }
  }
}
