package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackFilter;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicFilterService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;

@RunWith(Parameterized.class)
public class BetPackFilterAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<BetPackFilter> {
  @Mock private BetPackMarketPlacePublicFilterService service;

  @Getter @InjectMocks private BetPackFilterAfterSaveListener listener;

  @Getter @Spy BetPackFilter entity = new BetPackFilter();

  @Getter private final List<BetPackFilter> collection = Arrays.asList(new BetPackFilter());

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma/bet-pack", "filter"},
          {"connect", "api/connect/bet-pack", "filter"}
        });
  }

  @Before
  public void init() {

    given(service.getActiveBetPackFilterByBrand(anyString())).willReturn(this.getCollection());
  }
}
