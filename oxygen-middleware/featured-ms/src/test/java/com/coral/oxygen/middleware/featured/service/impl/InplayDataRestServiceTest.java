package com.coral.oxygen.middleware.featured.service.impl;

import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.featured.exception.InplayDataException;
import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportEvents;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import java.io.EOFException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Answers;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import retrofit2.Response;

@RunWith(MockitoJUnitRunner.class)
public class InplayDataRestServiceTest {

  @Mock private InPlayData inPlayData;

  @Mock(answer = Answers.RETURNS_DEEP_STUBS)
  private InplayApi inplayApi;

  private InplayDataRestService inplayDataRestService;

  private okhttp3.Request.Builder builder = new okhttp3.Request.Builder().url("http://localhost");
  private okhttp3.Request request = builder.build();
  private static final String version = "12345";

  @Before
  public void setUp() {
    inplayDataRestService = new InplayDataRestService(inplayApi);
  }

  @Test
  public void getInplayDataVersion() throws IOException {
    when(inplayApi.getVersion().execute()).thenReturn(Response.success(version));
    Assert.assertEquals(version, inplayDataRestService.getInplayDataVersion());
  }

  @Test
  public void getInplayDataVersionEmptyResponse() throws IOException {
    when(inplayApi.getVersion().execute()).thenReturn(Response.success(""));
    Assert.assertEquals("", inplayDataRestService.getInplayDataVersion());
  }

  @Test(expected = InplayDataException.class)
  // impossible case in real life :-)
  // InplayApi Call<String> getVersion() will be casted to empty string
  public void getInplayDataVersionNullResponse() throws IOException {
    when(inplayApi.getVersion().execute()).thenReturn(Response.success(null));
    inplayDataRestService.getInplayDataVersion();
  }

  @Test
  public void getInplayData() throws IOException {
    when(inplayApi.getInPlayModel(version).execute()).thenReturn(Response.success(inPlayData));
    Assert.assertEquals(inPlayData, inplayDataRestService.getInplayData(version));
  }

  @Test(expected = InplayDataException.class)
  public void getInplayDataEmptyResponse() throws IOException {
    when(inplayApi.getInPlayModel(version).execute()).thenReturn(null);
    inplayDataRestService.getInplayData(version);
  }

  @Test
  public void retrieveEmptyInPlayDataOnEOFException() throws IOException {
    when(inplayApi.getInPlayModel(version).request()).thenReturn(request);
    when(inplayApi.getInPlayModel(version).execute()).thenThrow(new EOFException());
    InPlayData inplayData = inplayDataRestService.getInplayData(version);

    Assert.assertNull(inplayData.getSportsRibbon());
    assertEmpty(inplayData.getLivenow().getEventsIds());
    assertEmpty(inplayData.getUpcoming().getEventsIds());
  }

  private void assertEmpty(Collection collection) {
    Assert.assertTrue(collection.isEmpty());
  }

  @Test(expected = InplayDataException.class)
  public void getInplayDataThrowsIOException() throws IOException {
    when(inplayApi.getInPlayModel(version).request()).thenReturn(request);
    when(inplayApi.getInPlayModel(version).execute()).thenThrow(new IOException());
    inplayDataRestService.getInplayData(version);
  }

  @Test
  public void getVirtualSportData() throws IOException {
    List<VirtualSportEvents> retVal = new ArrayList<>();
    when(inplayApi.getVirtualSportsData(version).request()).thenReturn(request);
    when(inplayApi.getVirtualSportsData(version).execute()).thenReturn(Response.success(retVal));
    assertEmpty(inplayDataRestService.getVirtualSportData(version));
  }

  @Test
  public void getVirtualSportDataException() throws IOException {
    when(inplayApi.getVirtualSportsData(version).request()).thenReturn(request);
    when(inplayApi.getVirtualSportsData(version).execute()).thenThrow(new RuntimeException());
    assertEmpty(inplayDataRestService.getVirtualSportData(version));
  }
}
