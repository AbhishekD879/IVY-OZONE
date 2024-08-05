package com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve;

import com.newrelic.api.agent.ExternalParameters;
import com.newrelic.api.agent.HttpParameters;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import java.io.IOException;
import java.nio.charset.Charset;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okio.Buffer;
import org.apache.commons.io.IOUtils;

@Slf4j
public class LiveServerCall implements Call {

  private OkHttpClient client;

  public LiveServerCall(OkHttpClient client) {
    this.client = client;
  }

  @Trace(metricName = "Call/Execute", dispatcher = true)
  @Override
  public Response execute(Request request) throws IOException {
    ExternalParameters params =
        HttpParameters.library("OkHttpClient")
            .uri(request.url().uri())
            .procedure("push")
            .noInboundHeaders()
            .build();

    Buffer body = new Buffer();
    request.body().writeTo(body);
    String requestBody = IOUtils.toString(body.inputStream(), Charset.defaultCharset());
    log.debug("REQUEST:  {} - {} ", request, requestBody);
    Response response = client.newCall(request).execute();
    log.debug("RESPONSE:  {}", response);
    NewRelic.getAgent().getTracedMethod().reportAsExternal(params);
    return response;
  }

  public OkHttpClient getClient() {
    return client;
  }

  public void setClient(OkHttpClient client) {
    this.client = client;
  }
}
