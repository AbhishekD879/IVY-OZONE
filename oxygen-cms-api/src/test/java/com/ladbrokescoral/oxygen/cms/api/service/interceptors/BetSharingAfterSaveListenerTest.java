package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.BetSharingEntity;
import com.ladbrokescoral.oxygen.cms.api.service.BetSharingService;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class BetSharingAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<BetSharingEntity> {
  @Mock private BetSharingService service;
  @Getter @InjectMocks private BetSharingAfterSaveListener listener;
  @Getter @Mock private BetSharingEntity entity = new BetSharingEntity();
  @Getter private Optional<BetSharingEntity> modelClass = Optional.ofNullable(entity);
  @Getter private List<BetSharingEntity> collection = null;

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "bet-sharing"},
          {"connect", "api/connect", "bet-sharing"}
        });
  }

  @Before
  public void init() {
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
