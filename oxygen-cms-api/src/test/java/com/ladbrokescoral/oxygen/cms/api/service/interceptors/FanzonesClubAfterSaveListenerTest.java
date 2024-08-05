package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneClub;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesClubService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class FanzonesClubAfterSaveListenerTest extends AbstractAfterSaveListenerTest<FanzoneClub> {

  @Mock private FanzonesClubService service;
  @Getter @InjectMocks private FanzonesClubAfterSaveListener listener;
  @Getter @Mock private FanzoneClub entity;
  @Getter @Mock private List<FanzoneClub> collection = Arrays.asList(entity);

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "fanzone-club"},
          {"connect", "api/connect", "fanzone-club"}
        });
  }

  @Before
  public void init() {
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
