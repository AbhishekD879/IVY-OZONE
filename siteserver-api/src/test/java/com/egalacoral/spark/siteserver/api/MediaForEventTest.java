package com.egalacoral.spark.siteserver.api;

import static org.junit.Assert.assertEquals;
import static org.mockserver.model.HttpRequest.request;
import static org.mockserver.model.HttpResponse.response;

import com.egalacoral.spark.siteserver.model.MediaProvider;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.List;
import java.util.Optional;
import org.junit.Test;

public class MediaForEventTest extends BasicIntegrationMock {

  private final String serviceName = "MediaForEvent";
  private final String basePath = "/openbet-ssviewer/Media/2.27";

  @Test
  public void test() throws NoSuchAlgorithmException, KeyManagementException {
    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePath + "/" + serviceName + "/1")
                .withQueryStringParameter("translationLang", "en"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString("response/getMediaForEvent.json")));

    final SiteServerApi api =
        new SiteServerApi.Builder()
            .setUrl("http://127.0.0.1:8443")
            .setLoggingLevel(SiteServerApi.Level.BODY)
            .setConnectionTimeout(1)
            .setReadTimeout(1)
            .setMaxNumberOfRetries(1)
            .setVersion("2.27")
            .build();

    Optional<List<MediaProvider>> response = api.getMedia("1");

    assertEquals(true, response.isPresent());
    assertEquals(2, response.get().size());
    assertEquals("VST", response.get().get(0).getMediaTypeCode());
  }
}
