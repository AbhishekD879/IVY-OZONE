package com.egalacoral.spark.liveserver;

import com.google.common.io.CharStreams;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okio.Buffer;

@Slf4j
public class LiveServerCall implements Call {

  private OkHttpClient client;

  public LiveServerCall(OkHttpClient client) {
    this.client = client;
  }

  @Override
  public Response execute(Request request) throws IOException {

    Buffer body = new Buffer();
    request.body().writeTo(body);

    String requestBody = null;
    try (final Reader reader = new InputStreamReader(body.inputStream())) {
      requestBody = CharStreams.toString(reader);
    }

    log.debug("REQUEST:  {} - {} ", request, requestBody);
    Response response = client.newCall(request).execute();
    log.debug("RESPONSE:  {}", response);

    return response;
  }

  public OkHttpClient getClient() {
    return client;
  }

  public void setClient(OkHttpClient client) {
    this.client = client;
  }
}
