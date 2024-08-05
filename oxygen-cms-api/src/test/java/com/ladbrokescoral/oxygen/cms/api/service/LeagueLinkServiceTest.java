package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.LeagueLink;
import com.ladbrokescoral.oxygen.cms.api.repository.impl.LeagueLinkRepository;
import java.io.IOException;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class LeagueLinkServiceTest {

  @Mock private LeagueLinkRepository leagueLinkRepository;

  @InjectMocks private LeagueLinkService service;

  List<LeagueLink> leagueLinks;

  @Before
  public void init() throws IOException {
    service = new LeagueLinkService(leagueLinkRepository);
    final ObjectMapper jsonMapper = new ObjectMapper();
    leagueLinks =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("service/leagueLinks.json"),
            new TypeReference<List<LeagueLink>>() {});
  }

  @Test
  public void testToGetEnabledLeagueLinksByCouponId() {
    when(leagueLinkRepository.findByCouponIdsContainsAndEnabledTrueAndBrandEquals(
            anyInt(), anyString()))
        .thenReturn(leagueLinks);
    List<LeagueLink> response = service.getEnabledLeagueLinksByCouponId("bma", 123);
    Assert.assertNotNull(response);
    Assert.assertEquals(leagueLinks, response);
  }
}
