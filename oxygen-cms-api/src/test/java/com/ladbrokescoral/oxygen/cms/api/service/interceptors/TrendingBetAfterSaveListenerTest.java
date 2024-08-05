package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.TrendingBet;
import com.ladbrokescoral.oxygen.cms.api.service.TrendingBetService;
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
public class TrendingBetAfterSaveListenerTest extends AbstractAfterSaveListenerTest<TrendingBet> {
  @Mock private TrendingBetService service;
  @Getter @InjectMocks private TrendingBetAfterSaveListener listener;
  @Getter @Mock private TrendingBet entity = new TrendingBet();
  @Getter private Optional<TrendingBet> modelClass = Optional.ofNullable(entity);
  @Getter private List<TrendingBet> collection = null;

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "trending-bet/bet-receipt"},
          {"bma", "api/bma", "trending-bet/bet-slip"},
          {"connect", "api/connect", "trending-bet/bet-receipt"},
          {"connect", "api/connect", "trending-bet/bet-slip"}
        });
  }

  @Before
  public void init() {
    given(service.getTrendingBetsByBrand("bma", "bet-slip"))
        .willReturn(Optional.of(new TrendingBet()));
  }
}
