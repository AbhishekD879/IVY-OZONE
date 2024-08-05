package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSignposting;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewSignpostingService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class FanzoneNewSignpostingAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<FanzoneNewSignposting> {

  @Mock private FanzonesNewSignpostingService service;
  @Getter @InjectMocks private FanzoneNewSignpostingAfterSaveListener listener;
  @Getter @Mock private FanzoneNewSignposting entity;
  @Getter @Mock private List<FanzoneNewSignposting> collection = Arrays.asList(entity);

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "fanzone-new-signposting"},
          {"connect", "api/connect", "fanzone-new-signposting"}
        });
  }

  @Before
  public void init() {
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
