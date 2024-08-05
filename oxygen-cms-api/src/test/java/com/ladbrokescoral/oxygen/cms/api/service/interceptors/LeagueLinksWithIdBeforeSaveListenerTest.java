package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.LeagueLink;
import com.ladbrokescoral.oxygen.cms.api.service.LeagueLinkService;
import java.io.IOException;
import java.util.*;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;

@RunWith(Parameterized.class)
public class LeagueLinksWithIdBeforeSaveListenerTest
    extends AbstractBeforeSaveListenerTest<LeagueLink> {
  @Mock LeagueLinkService service;
  @Getter @InjectMocks private LeagueLinksSaveListener listener;

  @Getter @Spy
  LeagueLink entity =
      new ObjectMapper()
          .readValue(
              TestUtil.class.getResourceAsStream("service/interceptors/leagueLinkWithId.json"),
              new TypeReference<LeagueLink>() {});

  @Getter List<LeagueLink> collection;

  public LeagueLinksWithIdBeforeSaveListenerTest() throws IOException {}

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma/league-links", "4"},
          {"ladbrokes", "api/ladbrokes/league-links", "4"}
        });
  }

  @Before
  public void init() throws IOException {
    final ObjectMapper jsonMapper = new ObjectMapper();
    entity.setId("123");
    collection = new ArrayList<>();
    /* jsonMapper.readValue(
    TestUtil.class.getResourceAsStream("service/interceptors/leagueLinks.json"),
    new TypeReference<List<LeagueLink>>() {});*/
    given(service.getEnabledLeagueLinksByCouponId(anyString(), anyInt()))
        .willReturn(
            jsonMapper.readValue(
                TestUtil.class.getResourceAsStream(
                    "service/interceptors/leagueLinksWithLinkIds.json"),
                new TypeReference<List<LeagueLink>>() {}));
    LeagueLink ll =
        new LeagueLink("bma", false, new LinkedList<>(Arrays.asList(3, 4)), 5, 7, "string");
    ll.setId("123");
    given(service.findOne(anyString())).willReturn(Optional.of(ll));
  }
}
