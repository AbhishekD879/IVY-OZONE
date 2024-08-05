package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewGamingPopUp;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewGamingPopUpService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class FanzonesNewGamingPopUpAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<FanzoneNewGamingPopUp> {

  @Mock private FanzonesNewGamingPopUpService service;
  @Getter @InjectMocks private FanzonesNewGamingPopUpAfterSaveListener listener;
  @Getter @Mock private FanzoneNewGamingPopUp entity;
  @Getter @Mock private List<FanzoneNewGamingPopUp> collection = Arrays.asList(entity);

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "fanzone-new-gaming-pop-up"},
          {"connect", "api/connect", "fanzone-new-gaming-pop-up"}
        });
  }

  @Before
  public void init() {
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
