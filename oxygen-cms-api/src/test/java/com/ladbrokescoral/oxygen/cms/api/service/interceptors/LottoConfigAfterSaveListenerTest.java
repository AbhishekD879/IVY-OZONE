package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.LottoConfig;
import com.ladbrokescoral.oxygen.cms.api.service.LottoConfigService;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.context.annotation.Import;

@RunWith(Parameterized.class)
@Import(ModelMapperConfig.class)
public class LottoConfigAfterSaveListenerTest extends AbstractAfterSaveListenerTest<LottoConfig> {
  @Mock private LottoConfigService service;
  @Getter @InjectMocks private LottoConfigAfterSaveListener listener;
  @Getter @Mock private LottoConfig entity = new LottoConfig();
  @Getter private Optional<LottoConfig> modelClass = Optional.ofNullable(entity);
  @Getter private List<LottoConfig> collection = null;

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "lotto-configs"},
          {"connect", "api/connect", "lotto-configs"}
        });
  }

  @Before
  public void init() {
    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
