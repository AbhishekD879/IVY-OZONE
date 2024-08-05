package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneSyc;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesSycService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class FanzonesSycAfterSaveListenerTest extends AbstractAfterSaveListenerTest<FanzoneSyc> {

  @Mock private FanzonesSycService service;
  @Getter @InjectMocks private FanzonesSycAfterSaveListener listener;
  @Getter @Mock private FanzoneSyc entity;
  @Getter @Mock private List<FanzoneSyc> collection = Arrays.asList(entity);

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "fanzone-syc"},
          {"connect", "api/connect", "fanzone-syc"}
        });
  }

  @Before
  public void init() {
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
