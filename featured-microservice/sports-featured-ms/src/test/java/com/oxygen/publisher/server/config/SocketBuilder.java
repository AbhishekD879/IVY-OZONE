package com.oxygen.publisher.server.config;

import io.socket.client.IO;
import io.socket.client.Socket;
import io.socket.emitter.Emitter;
import java.net.URISyntaxException;
import java.util.Arrays;
import java.util.function.Consumer;

/** Created by Aliaksei Yarotski on 12/26/17. */
// TODO move to accumulator project, refactor to simple test framework
public class SocketBuilder {

  public static final String QUERY_PARAMS_DEFAULT =
      "transport=websocket&EIO=3&version=1.0"; // version=1.0
  public Socket clientSocket;

  public static class TopicListener implements Emitter.Listener {

    private final String topicName;
    private final Consumer<Object[]> onEmit;

    public TopicListener(String topicName, Consumer<Object[]> onEmit) {
      this.topicName = topicName;
      this.onEmit = onEmit;
    }

    public String getTopicName() {
      return topicName;
    }

    @Override
    public void call(Object... args) {
      onEmit.accept(args);
    }
  }

  public SocketBuilder connectionUrl(String serverEndpoint, String query, String context)
      throws URISyntaxException {
    IO.Options opts = new IO.Options();
    opts.forceNew = true;
    opts.query = query;
    opts.path = context;
    clientSocket = IO.socket(serverEndpoint, opts);
    return this;
  }

  public SocketBuilder connectionUrl(String serverEndpoint, String context)
      throws URISyntaxException {
    return connectionUrl(serverEndpoint, QUERY_PARAMS_DEFAULT, context);
  }

  public SocketBuilder topicListeners(TopicListener... listeners) {
    Arrays.stream(listeners)
        .forEach(
            l ->
                clientSocket
                    .on(
                        Socket.EVENT_CONNECT,
                        new Emitter.Listener() {

                          @Override
                          public void call(Object... args) {
                            clientSocket.emit(l.getTopicName(), "hi");
                            // clientSocket.disconnect();
                          }
                        })
                    .on(l.getTopicName(), l)
                    .on(
                        Socket.EVENT_DISCONNECT,
                        new Emitter.Listener() {

                          @Override
                          public void call(Object... args) {}
                        }));
    return this;
  }

  public Socket initClient() throws Exception {
    clientSocket.connect();
    int count = 10;
    while (!clientSocket.connected() && count > 0) {
      Thread.sleep(400);
      count--;
    }
    if (!clientSocket.connected()) {
      throw new RuntimeException("Socket relation does not connect.");
    }
    return clientSocket;
  }
}
