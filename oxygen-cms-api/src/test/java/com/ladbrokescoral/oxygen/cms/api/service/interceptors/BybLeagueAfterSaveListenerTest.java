package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BybLeagueDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybLeague;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BybLeaguePublicService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class BybLeagueAfterSaveListenerTest extends AbstractAfterSaveListenerTest<BybLeague> {

  @Mock private BybLeaguePublicService service;
  @Getter @InjectMocks private BybLeagueAfterSaveListener listener;

  @Getter @Mock private BybLeague entity;
  @Getter private List<BybLeagueDto> collection = Arrays.asList(new BybLeagueDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "byb-leagues"},
          {"connect", "api/connect", "byb-leagues"}
        });
  }

  @Before
  public void init() {

    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
