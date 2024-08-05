package com.coral.siteserver.api;

import com.coral.siteserver.model.Event;
import com.coral.siteserver.model.Market;
import com.coral.siteserver.model.Outcome;
import com.coral.siteserver.model.Price;
import com.coral.siteserver.model.SSResponse;
import java.io.IOException;
import java.net.SocketTimeoutException;
import java.net.URL;
import java.net.URLConnection;
import java.util.stream.Collectors;
import java.util.stream.LongStream;
import org.junit.Assert;
import org.junit.Ignore;
import org.junit.Test;
import org.mockito.Mockito;
import retrofit2.Response;

/** Created by azayats on 25.07.17. */
public class SiteServerServiceTest {

  @Test
  public void testPageSize() throws IOException {
    CallsAPI api = Mockito.mock(CallsAPI.class);
    retrofit2.Call call = Mockito.mock(retrofit2.Call.class);
    Mockito.when(api.getEvents(Mockito.any(), Mockito.any(), Mockito.any())).thenReturn(call);
    Mockito.when(call.clone()).thenReturn(call);
    SSResponse ssResponse =
        new SSResponse() {
          {
            this.response = new SSResponse.SSChildResponse();
          }
        };
    Mockito.when(call.execute()).thenReturn(Response.success(ssResponse));

    SiteServerService service = new SiteServerService(api, "2.22", 1);
    service.setPageSize(100);

    service.getEventIdS(LongStream.rangeClosed(1, 299).boxed().collect(Collectors.toList()));

    Mockito.verify(api)
        .getEvents(
            "2.22",
            LongStream.rangeClosed(1, 100)
                .boxed()
                .map(String::valueOf)
                .collect(Collectors.joining(",")),
            false);
    Mockito.verify(api)
        .getEvents(
            "2.22",
            LongStream.rangeClosed(101, 200)
                .boxed()
                .map(String::valueOf)
                .collect(Collectors.joining(",")),
            false);
    Mockito.verify(api)
        .getEvents(
            "2.22",
            LongStream.rangeClosed(201, 299)
                .boxed()
                .map(String::valueOf)
                .collect(Collectors.joining(",")),
            false);
  }

  @Test
  // don't have expectation: Shouldn't fall with NPE
  public void testSSTimeout() throws IOException {
    CallsAPI api = Mockito.mock(CallsAPI.class);
    retrofit2.Call call = Mockito.mock(retrofit2.Call.class);
    okhttp3.Request.Builder builder = new okhttp3.Request.Builder().url("http://localhost");
    okhttp3.Request request = builder.build();

    Mockito.when(api.getEvents(Mockito.any(), Mockito.any(), Mockito.any())).thenReturn(call);
    Mockito.when(call.request()).thenReturn(request);
    Mockito.when(call.clone()).thenReturn(call);
    Mockito.when(call.execute()).thenThrow(new SocketTimeoutException());

    SiteServerService service = new SiteServerService(api, "2.22", 1);
    service.setPageSize(10);

    // shouldn't throw NPE
    try {
      service.getEventIdS(LongStream.rangeClosed(1, 10).boxed().collect(Collectors.toList()));
    } catch (Exception e) {
      Assert.fail(e.getMessage());
    }
  }

  @SuppressWarnings({"serial", "rawtypes", "unchecked"})
  @Test
  public void testGetSelectioncall() throws IOException {
    CallsAPI api = Mockito.mock(CallsAPI.class);
    retrofit2.Call call = Mockito.mock(retrofit2.Call.class);
    Mockito.when(api.getEvents(Mockito.any(), Mockito.any(), Mockito.any())).thenReturn(call);
    Mockito.when(call.clone()).thenReturn(call);
    SSResponse ssResponse =
        new SSResponse() {
          {
            this.response = new SSResponse.SSChildResponse();
          }
        };
    Mockito.when(call.execute()).thenReturn(Response.success(ssResponse));
    Event event = new Event();
    event.getEventFlagCodes();
    Market market = new Market();
    market.getFlags();
    Outcome outcome = new Outcome();
    outcome.getHasPriceStream();
    Price price = new Price();
    price.getPriceStreamType();
    price.getPriceAmerican();
    SiteServerService service = new SiteServerService(api, "2.65", 1);
    try {
      service.getSelectionCall(200763786L);
    } catch (Exception e) {
      Assert.fail(e.getMessage());
    }
  }

  @Ignore
  @Test
  /** Test for adding subscription for manual QA needs */
  public void testALotSubscriptions() throws IOException {
    long initialId = 6195284;
    int count = 330;
    String baseUrl =
        "https://oxygen-liveupdates-phoeinx.symphony-solutions.eu:446/qa/subscription/add/sEVENT";

    for (long id = initialId; id < initialId + count; id++) {
      String idStr = String.valueOf(id);
      while (idStr.length() < 10) {
        idStr = "0" + idStr;
      }
      URL url = new URL(baseUrl + idStr);
      URLConnection urlConnection = url.openConnection();
      Object content = urlConnection.getContent();
      System.out.println(content);
    }
  }
}
