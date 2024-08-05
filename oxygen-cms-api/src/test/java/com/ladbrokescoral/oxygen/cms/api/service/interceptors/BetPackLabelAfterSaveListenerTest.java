package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackLabel;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicLabelService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.After;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;

@RunWith(Parameterized.class)
public class BetPackLabelAfterSaveListenerTest extends AbstractAfterSaveListenerTest<BetPackLabel> {

  @Mock private BetPackMarketPlacePublicLabelService service;

  @Getter @InjectMocks private BetPackLabelAfterSaveListener listener;

  @Getter @Spy BetPackLabel entity = new BetPackLabel();

  @Getter private final List<BetPackLabel> collection = null;

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma/bet-pack", "label"}});
  }

  @Before
  public void init() {
    given(service.getBetPackLabelByBrand(anyString())).willReturn(Arrays.asList(entity));
  }

  @After
  public void verify() {
    then(context).should().upload(brand, "api/bma/bet-pack", filename, entity);
  }
}
