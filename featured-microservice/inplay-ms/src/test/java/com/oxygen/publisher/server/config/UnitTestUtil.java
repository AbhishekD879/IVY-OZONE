package com.oxygen.publisher.server.config;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.junit.Assert.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doAnswer;

import com.corundumstudio.socketio.SocketIOServer;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.TypeFactory;
import com.oxygen.publisher.configuration.JsonSupportConfig;
import io.socket.client.Socket;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.CountDownLatch;
import java.util.function.Consumer;
import lombok.SneakyThrows;
import org.skyscreamer.jsonassert.JSONAssert;

public class UnitTestUtil {

  private static final ObjectMapper OBJECT_MAPPER = new JsonSupportConfig().objectMapper();
  private static final TypeFactory JSON_TYPE_FACTORY = TypeFactory.defaultInstance();

  public static CountDownLatch ioServerResponseVerification(
      Consumer<Object[]> onEmit, String expectedResponse) {
    CountDownLatch lock = new CountDownLatch(1);
    doAnswer(
            invocation -> {
              // server response
              Object[] msg = invocation.getArgument(0);
              assertTrue(msg.length > 0);
              assertThat(msg[0]).isEqualTo(expectedResponse);
              lock.countDown();
              return msg;
            })
        .when(onEmit)
        .accept(any()); // when client get response from server
    return lock;
  }

  public static CountDownLatch ioServerResponseVerification(
      Consumer<Object[]> onEmit, Object expectedResponse) {
    CountDownLatch lock = new CountDownLatch(1);
    doAnswer(
            invocation -> {
              // server response
              consumeSocketMessage(lock, invocation.getArgument(0), expectedResponse);
              return invocation.getArgument(0);
            })
        .when(onEmit)
        .accept(any()); // when client get response from server
    return lock;
  }

  @SneakyThrows
  public static void consumeSocketMessage(
      CountDownLatch lock, Object[] socketMessage, Object expectedResponse) {
    lock.countDown();
    assertTrue(socketMessage.length > 0);
    // used JsonElement to be able to get equal two Json elements with different elements
    // order
    String expectedJson = OBJECT_MAPPER.writeValueAsString(expectedResponse);
    String actualJson = String.valueOf(socketMessage[0]);
    JSONAssert.assertEquals(expectedJson, actualJson, false);
  }

  public static Set<String> getClientRooms(SocketIOServer ioServer, Socket client) {
    return ioServer.getClient(UUID.fromString(client.id())).getAllRooms();
  }

  @SneakyThrows
  public static <T> T fromFile(String name, Class<T> clazz) {
    try (InputStream stream = UnitTestUtil.class.getClassLoader().getResourceAsStream(name)) {
      return OBJECT_MAPPER.readValue(new InputStreamReader(stream, StandardCharsets.UTF_8), clazz);
    }
  }

  @SneakyThrows
  public static <T> List<T> listFromFile(String name, Class<T> clazz) {
    try (InputStream stream = UnitTestUtil.class.getClassLoader().getResourceAsStream(name)) {
      return OBJECT_MAPPER.readValue(
          new InputStreamReader(stream, StandardCharsets.UTF_8),
          JSON_TYPE_FACTORY.constructCollectionType(ArrayList.class, clazz));
    }
  }

  @SneakyThrows
  public static String fromFile(String name) {
    URI uri = UnitTestUtil.class.getClassLoader().getResource(name).toURI();
    return new String(Files.readAllBytes(Paths.get(uri)));
  }
}
