package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneComingBack;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesComingBackService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class FanzonesComingBackAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<FanzoneComingBack> {

  @Mock private FanzonesComingBackService service;
  @Getter @InjectMocks private FanzonesComingBackAfterSaveListener listener;
  @Getter @Mock private FanzoneComingBack entity;
  @Getter @Mock private List<FanzoneComingBack> collection = Arrays.asList(entity);

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "fanzone-coming-back"},
          {"connect", "api/connect", "fanzone-coming-back"}
        });
  }

  @Before
  public void init() {
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
