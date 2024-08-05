package com.oxygen.publisher.service;

import static com.oxygen.publisher.context.AbstractSessionContext.IO_SERVER_HEALTH_CHECK_ROOM_NAME;

import com.corundumstudio.socketio.SocketIOServer;
import com.newrelic.api.agent.NewRelic;
import com.oxygen.health.api.ReloadableService;
import io.socket.client.IO;
import io.socket.client.Socket;
import java.net.URISyntaxException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;

@Slf4j
public abstract class AbstractIoServerHealthIndicatorService implements ReloadableService {

  @Autowired private SocketIOServer socketIOServer;

  @Value("${socket.context}")
  private String serverPath;

  @Value("${socket.websocket.port}")
  private String serverPort;

  private static final String IO_SERVER_URL = "http://127.0.0.1:";

  @Value("${socket.websocket.health.timeout:3}")
  private static int healthTimeout = 3;

  private Socket clientSocket;
  private volatile CountDownLatch lock;

  private volatile boolean isOnService;
  private volatile boolean ioServerStatus;
  private ScheduledExecutorService executorService;

  protected abstract String getQueryParams();

  @Override
  public void start() {
    if (isOnService) {
      return;
    }

    IO.Options opts = new IO.Options();
    opts.query = getQueryParams();
    opts.path = serverPath;
    try {
      clientSocket = IO.socket(IO_SERVER_URL + serverPort, opts);
    } catch (URISyntaxException e) {
      throw new IllegalStateException(e);
    }
    clientSocket.on(
        IO_SERVER_HEALTH_CHECK_ROOM_NAME,
        args -> {
          lock.countDown();
        });
    // async connect
    clientSocket.connect();
    executorService = Executors.newSingleThreadScheduledExecutor();
    executorService.scheduleAtFixedRate(this::checkServerStatus, 0, 10, TimeUnit.SECONDS);
    isOnService = true;
  }

  // time consuming operation (max 2 seconds)
  private void checkServerStatus() {
    try {
      // session may be closed due to session ttl
      if (!clientSocket.connected()) {
        clientSocket.connect();
      }
      ioServerStatus = false;
      lock = new CountDownLatch(1);

      clientSocket.emit(IO_SERVER_HEALTH_CHECK_ROOM_NAME, "");
      // if no response more than 2 seconds, assume that IO server is dead
      ioServerStatus = lock.await(healthTimeout, TimeUnit.SECONDS);
      if (!ioServerStatus) {
        int clients = socketIOServer.getAllClients().size();
        log.warn(
            "No response from socket.io server after {}s. isOnService={}; ioServerStatus={}; clients#={}",
            healthTimeout,
            isOnService,
            ioServerStatus,
            clients);
        NewRelic.noticeError(
            "No response from socket.io server in " + healthTimeout + "s. Clients#=" + clients);
      }
    } catch (InterruptedException ex) {
      log.warn(
          "Failed to connect to socketIO server. It's expected while application is starting.", ex);
      NewRelic.noticeError(ex);
      Thread.currentThread().interrupt();
    }
  }

  @Override
  public boolean isHealthy() {
    return isOnService && ioServerStatus && !executorService.isShutdown();
  }

  @Override
  public void evict() {}

  @Override
  public void onFail(Exception ex) {
    evict();
  }
}
