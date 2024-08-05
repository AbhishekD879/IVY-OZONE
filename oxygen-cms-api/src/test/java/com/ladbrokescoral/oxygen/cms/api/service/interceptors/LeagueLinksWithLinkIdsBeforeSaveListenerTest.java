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
public class LeagueLinksWithLinkIdsBeforeSaveListenerTest
    extends AbstractBeforeSaveListenerTest<LeagueLink> {
  @Mock LeagueLinkService service;
  @Getter @InjectMocks private LeagueLinksSaveListener listener;

  @Getter @Spy
  LeagueLink entity =
      new ObjectMapper()
          .readValue(
              TestUtil.class.getResourceAsStream("service/interceptors/leagueLink.json"),
              new TypeReference<LeagueLink>() {});

  @Getter List<LeagueLink> collection;

  public LeagueLinksWithLinkIdsBeforeSaveListenerTest() throws IOException {}

  @Parameterized.Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma/league-links", "4"}, {"ladbrokes", "api/ladbrokes/league-links", "4"}
        });
  }

  @Before
  public void init() throws IOException {}
}
