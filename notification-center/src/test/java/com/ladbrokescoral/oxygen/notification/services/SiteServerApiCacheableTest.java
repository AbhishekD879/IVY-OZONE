package com.ladbrokescoral.oxygen.notification.services;

import static com.googlecode.catchexception.CatchException.catchException;
import static com.googlecode.catchexception.CatchException.caughtException;
import static com.ladbrokescoral.oxyegn.test.utils.Utils.fromFile;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.util.Collections;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SiteServerApiCacheableTest {

  private SiteServerApiService siteServerApiService;
  private static final String MOCK_OUTCOME_ID = "933253816";
  private static final String MOCK_OUTCOME_ID_NO_EVENTS = "933253810";
  private static final String MOCK_OUTCOME_ID_NO_OUTCOME = "933253811";
  private static final String EXPECTED_OUTCOME_NAME = "Any Bunny";
  private static final String TEST_EVENT_ID = "4801432878";

  @Mock private SiteServerApi siteServerApi;
  private Gson gson = new GsonBuilder().create();

  @Before
  public void setUp() {
    siteServerApiService = new SiteServerApiCacheable(siteServerApi, "VST12");

    when(siteServerApi.getEventToOutcomeForOutcome(
            eq(Collections.singletonList(MOCK_OUTCOME_ID)), any(), any(), anyBoolean()))
        .thenReturn(
            Optional.of(
                Collections.singletonList(
                    fromFile(gson, "ssEvents/event_for_outcome.json", Event.class))));

    when(siteServerApi.getEventToOutcomeForOutcome(
            eq(Collections.singletonList(MOCK_OUTCOME_ID_NO_OUTCOME)), any(), any(), anyBoolean()))
        .thenReturn(
            Optional.of(
                Collections.singletonList(
                    fromFile(gson, "ssEvents/event_no_outcome.json", Event.class))));
  }

  @Test
  public void getOutcomeName() {
    Assert.assertEquals(
        EXPECTED_OUTCOME_NAME, siteServerApiService.getOutcomeName(MOCK_OUTCOME_ID));
  }

  @Test
  public void getOutcomeNameShouldThrowExceptionNoEvents() {
    catchException(() -> siteServerApiService.getOutcomeName(MOCK_OUTCOME_ID_NO_EVENTS));
    Assert.assertTrue(caughtException() instanceof IllegalStateException);
  }

  @Test
  public void getOutcomeNameShouldThrowExceptionNoOutcomes() {
    catchException(() -> siteServerApiService.getOutcomeName(MOCK_OUTCOME_ID_NO_OUTCOME));
    Assert.assertTrue(caughtException() instanceof IllegalStateException);
  }

  @Test
  public void getEvent() {
    siteServerApiService.getEvent(TEST_EVENT_ID);
    Mockito.verify(siteServerApi).getEvent(TEST_EVENT_ID, true);
  }
}
