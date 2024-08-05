package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.NetworkIndicatorConfig;
import com.ladbrokescoral.oxygen.cms.api.repository.NetworkIndicatorRepository;
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
public class NetworkIndicatorAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<NetworkIndicatorConfig> {

  @Getter @InjectMocks private NetworkIndicatorAfterSaveListener listener;

  @Getter @Mock private NetworkIndicatorConfig entity;

  @Mock private NetworkIndicatorRepository networkIndicatorRepository;

  @Getter @Mock
  private final List<NetworkIndicatorConfig> collection =
      Arrays.asList(new NetworkIndicatorConfig());

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(new Object[][] {{"bma", "api/bma", "network-indicator"}});
  }

  @Before
  public void init() {
    given(networkIndicatorRepository.findOneByBrand(Mockito.any()))
        .willReturn(Optional.of(new NetworkIndicatorConfig()));
  }

  @Test
  public void shouldAfterSaveEvent() throws Exception {

    // given
    given(getEntity().getBrand()).willReturn(brand);

    // when
    this.getListener()
        .onAfterSave(new AfterSaveEvent<NetworkIndicatorConfig>(getEntity(), null, "11"));

    // then
    if (null != getCollection()) {
      then(context).should().upload(brand, path, filename, new NetworkIndicatorConfig());
    }
  }
}
