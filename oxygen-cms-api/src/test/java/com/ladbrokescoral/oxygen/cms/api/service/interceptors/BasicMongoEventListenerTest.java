package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.SportQuickLink;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class BasicMongoEventListenerTest extends BDDMockito {

  @Mock private DeliveryNetworkService mock;

  private BasicMongoEventListener<SportQuickLink> listener;

  @Before
  public void init() {
    listener = new BasicMongoEventListener<SportQuickLink>(mock) {};
  }

  @Test
  public void testUploadEmptyCollection() {
    ArrayList<SportQuickLink> content = new ArrayList<SportQuickLink>();
    listener.uploadCollection("bma", "v1", "links", content);
    Mockito.verify(mock, times(1)).upload("bma", "v1", "links", content);
  }

  @Test
  public void testUploadNullCollection() {
    listener.uploadCollection("bma", "v1", "links", null);
    Mockito.verify(mock, times(0)).upload("bma", "v1", "links", null);
  }

  @Test
  public void testUploadCollection() {
    ArrayList<SportQuickLink> content = new ArrayList<SportQuickLink>();
    content.add(new SportQuickLink());
    listener.uploadCollection("bma", "v1", "links", content);
    Mockito.verify(mock, times(1)).upload("bma", "v1", "links", content);
  }

  @Test
  public void testUploadMap() {
    SportQuickLink sportQuickLink = new SportQuickLink();
    Map<String, SportQuickLink> map = new HashMap<>();

    listener.uploadMap("bma", "v1", "links", map);
    Mockito.verify(mock, times(0)).upload("bma", "v1", "links", map);
  }

  @Test
  public void testUploadMapForNonEmpty() {
    SportQuickLink sportQuickLink = new SportQuickLink();
    Map<String, SportQuickLink> map = new HashMap<>();
    map.put("1", sportQuickLink);
    listener.uploadMap("bma", "v1", "links", map);
    Mockito.verify(mock, times(1)).upload("bma", "v1", "links", map);
  }

  @Test
  public void testUploadOptionalForEmpty() {
    Optional<SportQuickLink> optionalSportQuickLink = Optional.empty();
    listener.uploadOptional("bma", "v1", "links", optionalSportQuickLink);
    Mockito.verify(mock, times(0)).upload("bma", "v1", "links", optionalSportQuickLink);
  }

  @Test
  public void testUploadCFContentForEmpty() {
    Optional<SportQuickLink> optionalSportQuickLink = Optional.empty();
    listener.uploadOptional("bma", "v1", "links", optionalSportQuickLink);
    Mockito.verify(mock, times(0)).uploadCFContent("bma", "v1", "links", optionalSportQuickLink);
  }
}
