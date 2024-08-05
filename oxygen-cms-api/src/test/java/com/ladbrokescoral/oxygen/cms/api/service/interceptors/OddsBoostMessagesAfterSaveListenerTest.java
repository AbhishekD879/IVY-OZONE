package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.OddsBoostMessage;
import com.ladbrokescoral.oxygen.cms.api.repository.OddsBoostMessageRepository;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import lombok.Getter;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;

@RunWith(Parameterized.class)
public class OddsBoostMessagesAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<OddsBoostMessage> {

  @Getter @InjectMocks private OddsBoostMessagesAfterSaveListener listener;

  @Getter @Mock private OddsBoostMessage entity;

  @Mock private OddsBoostMessageRepository oddsBoostMessageRepository;

  @Getter @Mock
  private final List<OddsBoostMessage> collection = Arrays.asList(new OddsBoostMessage());

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma", "odds-boost"}});
  }

  @Before
  public void init() {
    given(oddsBoostMessageRepository.findOneByBrand(Mockito.any()))
        .willReturn(Optional.of(new OddsBoostMessage()));
  }

  @Override
  @Test
  public void shouldAfterSaveEvent() throws Exception {

    // given
    given(getEntity().getBrand()).willReturn(brand);

    // when
    this.getListener().onAfterSave(new AfterSaveEvent<OddsBoostMessage>(getEntity(), null, "11"));

    // then
    if (null != getCollection()) {
      then(context).should().upload(brand, path, filename, new OddsBoostMessage());
    }
  }
}
