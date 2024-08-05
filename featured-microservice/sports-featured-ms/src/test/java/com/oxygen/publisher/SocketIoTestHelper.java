package com.oxygen.publisher;

import static io.socket.client.Socket.EVENT_CONNECT;

import com.oxygen.publisher.sportsfeatured.model.PageRawIndex;
import io.socket.client.Socket;
import java.util.Arrays;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;
import java.util.function.Consumer;
import lombok.SneakyThrows;
import org.json.JSONObject;

public class SocketIoTestHelper {

  private final Socket socketClient;

  public SocketIoTestHelper(Socket socketClient) {
    this.socketClient = socketClient;
  }

  public void executeWhenConnected(Consumer<Socket> socketConsumer) {
    socketClient.on(EVENT_CONNECT, args -> socketConsumer.accept(socketClient));
  }

  @SneakyThrows
  public void makeAssertionsOnResponse(
      String eventName, Consumer<JSONObject>... responseAssertions) {
    getAssertionsOnResponse(eventName, responseAssertions)
        .ifPresent(
            ae -> {
              throw ae;
            });
  }

  @SneakyThrows
  public Optional<AssertionError> getAssertionsOnResponse(
      String eventName, Consumer<JSONObject>... responseAssertions) {
    CountDownLatch countDownLatch = new CountDownLatch(1);
    AtomicReference<AssertionError> exc = new AtomicReference<>(null);
    socketClient.on(
        eventName,
        args -> {
          JSONObject response = (JSONObject) args[0];
          System.out.println(
              "### Client + " + socketClient.id() + " with message on event=" + eventName);
          try {
            if (!(responseAssertions.length > 0)) {
              Arrays.stream(responseAssertions).forEach(assertion -> assertion.accept(response));
            }
          } catch (AssertionError assertionError) {
            exc.set(assertionError);
          } finally {
            countDownLatch.countDown();
          }
        });

    socketClient.connect();
    boolean receivedResponse = countDownLatch.await(10, TimeUnit.SECONDS);

    return Optional.ofNullable(receivedResponse ? exc.get() : notReceivedAssertionError(eventName));
  }

  private AssertionError notReceivedAssertionError(String eventName) {
    return new AssertionError(
        "Client " + socketClient.id() + " should receive message on event=" + eventName);
  }

  public static Map<String, PageRawIndex> getSportPageMapCache() {

    return Map.of(
        "0",
        PageRawIndex.fromPageId("0"),
        "16",
        PageRawIndex.fromPageId("16"),
        "160",
        PageRawIndex.fromPageId("160"),
        "10",
        PageRawIndex.fromPageId("10"),
        "22",
        PageRawIndex.fromPageId("22"),
        "8",
        PageRawIndex.fromPageId("8"));
  }
}
