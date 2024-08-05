package com.coral.oxygen.middleware.common.service;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class AbstractSiteServeServiceTest {
  @Mock private SiteServerApi siteServerApi;
  @Mock private MarketTemplateNameService marketTemplateNameService;

  private static class TestSiteServeServiceSub extends AbstractSiteServeService {
    TestSiteServeServiceSub(
        SiteServerApi siteServerApi, MarketTemplateNameService marketTemplateNameService) {
      super(siteServerApi, marketTemplateNameService);
    }
  }

  @Test
  void testGetCommentaryForEvent() throws IOException {
    List<String> eventIds = Arrays.asList("1", "2", "3");
    InputStream commentaryStream =
        getClass().getClassLoader().getResourceAsStream("commentary.json");
    ObjectMapper mapper = new ObjectMapper();
    mapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
    List<Event> lsEvents = mapper.readValue(commentaryStream, new TypeReference<List<Event>>() {});
    Mockito.when(siteServerApi.getCommentaryForEvent(eventIds)).thenReturn(Optional.of(lsEvents));
    AbstractSiteServeService service =
        new TestSiteServeServiceSub(siteServerApi, marketTemplateNameService);
    Map<String, Event> result = service.getCommentaryForEvent(eventIds);
    Assert.assertEquals(3, result.size());
  }
}
