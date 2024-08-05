package com.coral.oxygen.middleware.featured.service.impl;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.featured.exception.TrendingBetDataException;
import com.coral.oxygen.middleware.featured.service.PopularBetService;
import com.coral.oxygen.middleware.pojos.model.cms.featured.PopularAccaWidgetData;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.PopularAccaResponse;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.TrendingBetsDto;
import java.io.EOFException;
import java.io.IOException;
import java.util.Arrays;
import okhttp3.MediaType;
import okhttp3.ResponseBody;
import org.junit.Before;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;
import org.junit.runner.RunWith;
import org.mockito.Answers;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import retrofit2.Response;

@RunWith(MockitoJUnitRunner.class)
public class PopularBetServiceTest {

  @Mock(answer = Answers.RETURNS_DEEP_STUBS)
  private PopularBetApi popularBetApi;

  PopularBetService popularBetService;

  private okhttp3.Request.Builder builder = new okhttp3.Request.Builder().url("http://localhost");
  private okhttp3.Request request = builder.build();

  private static final String ACCA_TYPE = "EVENT";
  private static final int ACCA_RANGE_MIN = 2;
  private static final int ACCA_RANGE_MAX = 5;
  private static final String EVENT_IDS = "12432";

  @Before
  public void init() {
    popularBetService = new PopularBetRestService(popularBetApi);
  }

  @Test
  public void popularBetApiTestExceptionSuccess() throws IOException {

    when(popularBetApi.getTrendingBetEvents("test").execute()).thenThrow(new EOFException());

    Assertions.assertThrows(
        TrendingBetDataException.class, () -> popularBetService.getTrendingBetByChannel("test"));
  }

  @Test
  public void popularBetApiTest() throws IOException {

    when(popularBetApi.getTrendingBetEvents("test").execute())
        .thenThrow(new NullPointerException());

    Assertions.assertThrows(
        TrendingBetDataException.class, () -> popularBetService.getTrendingBetByChannel("test"));
  }

  @Test
  public void popularBetApiTestResponseError() throws IOException {

    when(popularBetApi.getTrendingBetEvents("test").execute())
        .thenReturn(
            Response.error(
                500,
                ResponseBody.create(
                    "{\"error\":\"failed\"}", MediaType.parse("application/json"))));

    Assertions.assertThrows(
        TrendingBetDataException.class, () -> popularBetService.getTrendingBetByChannel("test"));
  }

  @Test
  public void popularBetApiTestSuccess() throws IOException {

    when(popularBetApi.getTrendingBetEvents("test").execute())
        .thenReturn(Response.success(new TrendingBetsDto()));

    Assertions.assertDoesNotThrow(() -> popularBetService.getTrendingBetByChannel("test"));
  }

  @Test
  public void testPopularAcca() throws IOException {

    when(popularBetApi.getPopularAcca(any()).execute())
        .thenReturn(Response.success(PopularAccaResponse.builder().build()));

    Assertions.assertDoesNotThrow(
        () -> popularBetService.getPopularAccaForData(new PopularAccaWidgetData()));
  }

  @Test
  public void testPopularAccaWithException() throws IOException {

    when(popularBetApi.getPopularAcca(any()).execute()).thenReturn(Response.success(null));
    PopularAccaWidgetData widgetData = new PopularAccaWidgetData();
    widgetData.setAccaIdsType(ACCA_TYPE);
    widgetData.setAccaRangeMin(ACCA_RANGE_MIN);
    widgetData.setAccaRangeMax(ACCA_RANGE_MAX);
    widgetData.setMarketTemplateIds(Arrays.asList(EVENT_IDS));
    widgetData.setListOfIds(Arrays.asList(EVENT_IDS));
    widgetData.setNumberOfTimeBackedThreshold(ACCA_RANGE_MAX);
    Assertions.assertThrows(
        TrendingBetDataException.class, () -> popularBetService.getPopularAccaForData(widgetData));
  }
}
