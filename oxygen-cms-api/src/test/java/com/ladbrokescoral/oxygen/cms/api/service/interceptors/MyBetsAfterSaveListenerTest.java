package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.MyBet;
import com.ladbrokescoral.oxygen.cms.api.service.MyBetsService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;

@RunWith(Parameterized.class)
public class MyBetsAfterSaveListenerTest extends AbstractAfterSaveListenerTest<MyBet> {
  @Getter @InjectMocks private MyBetsAfterSaveListener listener;

  @Getter @Mock private MyBet entity;

  @Mock private MyBetsService myBetsService;

  @Getter @Mock private final List<MyBet> collection = Arrays.asList(new MyBet());

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma", "my-bets"}});
  }

  @Before
  public void init() {
    given(myBetsService.findByBrand(brand)).willReturn(Arrays.asList(new MyBet()));
  }

  @Test
  public void shouldAfterSaveEvent() throws Exception {

    // given
    given(getEntity().getBrand()).willReturn(brand);

    // when
    this.getListener().onAfterSave(new AfterSaveEvent<MyBet>(getEntity(), null, "11"));

    // then
    if (null != getCollection()) {
      then(context).should().upload(brand, path, filename, Arrays.asList(new MyBet()));
    }
  }
}
