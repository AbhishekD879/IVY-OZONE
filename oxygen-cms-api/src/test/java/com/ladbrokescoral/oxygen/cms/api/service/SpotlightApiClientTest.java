package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.spotlight.SpotlightEventInfo;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.spotlight.SpotlightItems;
import com.ladbrokescoral.oxygen.cms.api.service.showdown.ShowdownService;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import okhttp3.OkHttpClient;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SpotlightApiClientTest {
  public static final String EVENT_ID = "23443";
  private SpotlightApiClient spotlightApiClient;

  @Mock ShowdownService showdownService;

  @Mock OkHttpClient okHttpClient;

  @Mock BrandService brandService;

  @Before
  public void setUp() throws Exception {
    mockBrands();
    when(showdownService.invokeSyncRequest(Mockito.any())).thenReturn(Optional.of(getItems()));
    spotlightApiClient = new SpotlightApiClient(brandService, showdownService, okHttpClient);
    Method initApis = SpotlightApiClient.class.getDeclaredMethod("initApis");
    initApis.setAccessible(true);
    initApis.invoke(spotlightApiClient);
  }

  private void mockBrands() {
    List<Brand> brands = new ArrayList<>();
    Brand brand = new Brand();
    brand.setBrandCode("ladbrokes");
    brand.setTitle("ladbrokes");
    brand.setSiteServerEndPoint("https://ss-aka-ori.ladbrokes.com/");
    brand.setSpotlightEndpoint("https://sb-api.ladbrokes.com/");
    brand.setSpotlightApiKey("298437be2343");
    brands.add(brand);

    brand = new Brand();
    brand.setBrandCode("test");
    brand.setTitle("test");
    brand.setSiteServerEndPoint("https://ss-aka-ori.ladbrokes.com/");
    brand.setSpotlightEndpoint("https://sb-api.ladbrokes.com/");
    brand.setSpotlightApiKey(null);
    brands.add(brand);

    brand = new Brand();
    brand.setBrandCode("testOther");
    brand.setTitle("testOther");
    brand.setSiteServerEndPoint("https://ss-aka-ori.ladbrokes.com/");
    brand.setSpotlightEndpoint(null);
    brand.setSpotlightApiKey("3443453");
    brands.add(brand);

    brand = new Brand();
    brand.setBrandCode("inSecureUrl");
    brand.setTitle("inSecureUrl");
    brand.setSiteServerEndPoint("file://ss-aka-ori.ladbrokes.com/");
    brand.setSpotlightEndpoint(null);
    brand.setSpotlightApiKey("3443453");
    brands.add(brand);

    brand = new Brand();
    brand.setBrandCode("emptyUrl");
    brand.setTitle("emptyUrl");
    brand.setSiteServerEndPoint(null);
    brand.setSpotlightEndpoint(null);
    brand.setSpotlightApiKey("3443453");
    brands.add(brand);

    brand = new Brand();
    brand.setBrandCode("sample");
    brand.setTitle("sample");
    brand.setSiteServerEndPoint(null);
    brand.setSpotlightEndpoint(null);
    brand.setSpotlightApiKey("3443453");
    brands.add(brand);

    when(brandService.findAll()).thenReturn(brands);
  }

  @Test
  public void testFetchingSpotlightDataForEventId() {
    when(showdownService.invokeSyncRequest(Mockito.any())).thenReturn(Optional.of(getItems()));
    SpotlightEventInfo spotlightEventInfo =
        spotlightApiClient.fetchSpotlightByEventId("ladbrokes", EVENT_ID);
    assertEquals(1, spotlightEventInfo.getHorses().size());
  }

  @Test
  public void testFetchingSpotlightDataEmptyForEventId() {
    when(showdownService.invokeSyncRequest(Mockito.any())).thenReturn(Optional.empty());
    SpotlightEventInfo spotlightEventInfo =
        spotlightApiClient.fetchSpotlightByEventId("ladbrokes", EVENT_ID);
    assertEquals(true, spotlightEventInfo.getError());
    assertEquals(0, spotlightEventInfo.getHorses().size());
  }

  @Test
  public void testFetchingSpotlightDataForUnexistingBrand() {
    SpotlightEventInfo spotlightEventInfo =
        spotlightApiClient.fetchSpotlightByEventId("sample", EVENT_ID);
    assertEquals(true, spotlightEventInfo.getError());
    assertEquals(0, spotlightEventInfo.getHorses().size());
  }

  @Test
  public void testValidatinUrl() {
    SpotlightEventInfo spotlightEventInfo =
        spotlightApiClient.fetchSpotlightByEventId("inSecureUrl", EVENT_ID);
    assertEquals(true, spotlightEventInfo.getError());
  }

  @Test
  public void testValidatinUrl_empty() {
    SpotlightEventInfo spotlightEventInfo =
        spotlightApiClient.fetchSpotlightByEventId("emptyUrl", EVENT_ID);
    assertEquals(true, spotlightEventInfo.getError());
  }

  private SpotlightItems getItems() {
    SpotlightItems spotlightItems = new SpotlightItems();
    Map<String, SpotlightEventInfo> map = new LinkedHashMap<>();
    SpotlightEventInfo spotlightsForEvent = new SpotlightEventInfo();
    spotlightsForEvent.setHorses(Arrays.asList(new SpotlightEventInfo.HorseInfo()));
    map.put(EVENT_ID, spotlightsForEvent);
    spotlightItems.setSpotlightPostsByEventId(map);
    return spotlightItems;
  }
}
