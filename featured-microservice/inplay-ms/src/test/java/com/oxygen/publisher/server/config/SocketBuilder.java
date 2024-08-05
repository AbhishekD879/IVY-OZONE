package com.oxygen.publisher.server.config;

import io.socket.client.IO;
import io.socket.client.Socket;
import java.net.URISyntaxException;

/** Created by Aliaksei Yarotski on 12/26/17. */
public class SocketBuilder {

  public static final String IN_PLAY_QUERY_PARAMS = "transport=websocket&EIO=3";
  public static final String IN_PLAY_SERVER_CONTEXT = "/websocket";
  public static final String FEATURED_QUERY_PARAMS = "transport=websocket&EIO=3&module=featured";
  public static final String FEATURED_1_0_QUERY_PARAMS =
      "transport=websocket&EIO=3&module=featured&version=1.0";
  public static final String FEATURED_SERVER_CONTEXT = "/socket.io";
  private static final String TEST_SERVER_URL = "http://localhost:8083";

  public Socket clientSocket;

  public SocketBuilder(String serverEndpoint, String query, String context) {
    IO.Options opts = new IO.Options();
    opts.forceNew = true;
    opts.query = query;
    opts.path = context;
    try {
      clientSocket = IO.socket(serverEndpoint, opts);
    } catch (URISyntaxException e) {
      throw new IllegalStateException(e);
    }
  }

  public static SocketBuilder getInplaySocket() {
    return new SocketBuilder(TEST_SERVER_URL, IN_PLAY_QUERY_PARAMS, IN_PLAY_SERVER_CONTEXT);
  }

  public Socket initClient() throws Exception {
    clientSocket.connect();
    int count = 10;
    while (!clientSocket.connected() && count > 0) {
      Thread.sleep(400);
      count--;
    }
    if (!clientSocket.connected()) {
      throw new IllegalStateException("Socket relation does not connect.");
    }
    return clientSocket;
  }
}
