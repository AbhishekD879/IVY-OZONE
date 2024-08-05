package com.oxygen.publisher.server.config;

import io.socket.client.IO;
import io.socket.client.Socket;
import io.socket.emitter.Emitter;
import java.net.URISyntaxException;
import java.util.Arrays;
import java.util.function.Consumer;

/** Created by Aliaksei Yarotski on 12/26/17. */
public class SocketBuilder {

  public static final String QUERY_PERAMS_DEFAULT = "module=featured&EIO=3&transport=websocket";
  private Socket clientSocket;

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

  public SocketBuilder connectionUrl(String serverEndpoint) throws URISyntaxException {
    IO.Options opts = new IO.Options();
    opts.forceNew = true;
    opts.query = QUERY_PERAMS_DEFAULT;
    clientSocket = IO.socket(serverEndpoint, opts);
    return this;
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
    while (!clientSocket.connected() || count > 0) {
      Thread.sleep(50);
      count--;
    }
    if (!clientSocket.connected()) {
      throw new RuntimeException("Socket relation does not connect.");
    }
    return clientSocket;
  }
}
