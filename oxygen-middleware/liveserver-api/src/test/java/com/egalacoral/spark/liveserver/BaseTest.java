package com.egalacoral.spark.liveserver;

import java.io.IOException;
import java.nio.charset.Charset;
import okhttp3.Protocol;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.internal.http.RealResponseBody;
import okio.Buffer;
import org.apache.commons.io.IOUtils;

public abstract class BaseTest {

  public Response createResponse() throws IOException {
    Response.Builder responseBuilder = new Response.Builder();
    Buffer buffer = new Buffer();
    String content = loadResponseContent();
    buffer.writeString(content, Charset.defaultCharset());
    responseBuilder.body(new RealResponseBody("Content-Type", 0, buffer));
    Request.Builder requestBuilder = new Request.Builder();
    requestBuilder.url("http://test.push.com");
    responseBuilder.request(requestBuilder.build());
    responseBuilder.protocol(Protocol.HTTP_2);
    responseBuilder.code(200);
    responseBuilder.message("?");
    Response response = responseBuilder.build();
    return response;
  }

  public String loadResponseContent() throws IOException {
    return IOUtils.toString(
        getClass().getClassLoader().getResourceAsStream("response.txt"), Charset.defaultCharset());
  }
}
