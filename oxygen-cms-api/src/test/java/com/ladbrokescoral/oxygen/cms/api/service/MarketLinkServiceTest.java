package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.MarketLink;
import com.ladbrokescoral.oxygen.cms.api.repository.impl.MarketLinkRepository;
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
public class MarketLinkServiceTest {

  @Mock private MarketLinkRepository marketLinkRepository;

  @InjectMocks private MarketLinkService service;

  List<MarketLink> marketLinks;

  @Before
  public void init() throws IOException {
    service = new MarketLinkService(marketLinkRepository);
    final ObjectMapper jsonMapper = new ObjectMapper();
    marketLinks =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("service/marketLinks.json"),
            new TypeReference<List<MarketLink>>() {});
  }

  @Test
  public void testToGetMarketLinksByBrand() {
    when(marketLinkRepository.findByBrandEqualsAndEnabledTrue(anyString())).thenReturn(marketLinks);
    List<MarketLink> response = service.getMarketLinksByBrand("bma");
    Assert.assertNotNull(response);
    Assert.assertEquals(marketLinks, response);
  }
}
