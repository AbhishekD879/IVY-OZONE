package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.LeagueLink;
import com.ladbrokescoral.oxygen.cms.api.service.LeagueLinkService;
import java.io.IOException;
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
public class LeagueLinksAfterSaveListenerTest extends AbstractAfterSaveListenerTest<LeagueLink> {
  @Mock LeagueLinkService service;
  @Getter @InjectMocks private LeagueLinksSaveListener listener;

  @Getter @Spy LeagueLink entity = new LeagueLink("bma", false, Arrays.asList(3), 5, 7, "string");
  @Getter List<LeagueLink> collection;

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma/league-links", "3"},
          {"ladbrokes", "api/ladbrokes/league-links", "3"}
        });
  }

  @Before
  public void init() throws IOException {
    final ObjectMapper jsonMapper = new ObjectMapper();
    collection =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("service/interceptors/leagueLinks.json"),
            new TypeReference<List<LeagueLink>>() {});
    given(service.getEnabledLeagueLinksByCouponId(anyString(), anyInt()))
        .willReturn(this.getCollection());
  }
}
