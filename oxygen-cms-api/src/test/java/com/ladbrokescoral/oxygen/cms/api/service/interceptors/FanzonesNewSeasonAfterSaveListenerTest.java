package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSeason;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewSeasonService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class FanzonesNewSeasonAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<FanzoneNewSeason> {

  @Mock private FanzonesNewSeasonService service;
  @Getter @InjectMocks private FanzonesNewSeasonAfterSaveListener listener;
  @Getter @Mock private FanzoneNewSeason entity;
  @Getter @Mock private List<FanzoneNewSeason> collection = Arrays.asList(entity);

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "fanzone-new-season"},
          {"connect", "api/connect", "fanzone-new-season"}
        });
  }

  @Before
  public void init() {
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
