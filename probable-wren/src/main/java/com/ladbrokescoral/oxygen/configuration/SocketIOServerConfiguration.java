package com.ladbrokescoral.oxygen.configuration;

import com.corundumstudio.socketio.AckMode;
import com.corundumstudio.socketio.SocketConfig;
import com.corundumstudio.socketio.SocketIOServer;
import com.corundumstudio.socketio.Transport;
import com.corundumstudio.socketio.protocol.JacksonJsonSupport;
import com.corundumstudio.socketio.protocol.JsonSupport;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.listeners.LiveServeSIOExceptionListener;
import io.netty.buffer.ByteBufOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Slf4j
@Configuration
public class SocketIOServerConfiguration {

  @Bean
  public SocketIOServer socketIOServer(
      @Value("${server.websocket.port}") int port,
      @Value("${netty.threads.worker}") int workersThreadsAmount,
      @Value("${netty.threads.boss}") int bossThreadsAmount,
      @Value("${netty.use.linux.native.epoll}") boolean useLinuxEpoll,
      JsonSupport jsonSupport) {
    com.corundumstudio.socketio.Configuration configuration =
        new com.corundumstudio.socketio.Configuration();
    configuration.setContext("/websocket");
    configuration.setPort(port);
    configuration.setAckMode(AckMode.AUTO);
    configuration.setTransports(Transport.WEBSOCKET);
    configuration.setBossThreads(bossThreadsAmount);
    configuration.setWorkerThreads(workersThreadsAmount);
    configuration.setWebsocketCompression(true);
    SocketConfig socketConfig = new SocketConfig();
    socketConfig.setReuseAddress(true);
    configuration.setSocketConfig(socketConfig);
    configuration.setJsonSupport(jsonSupport);
    configuration.setExceptionListener(new LiveServeSIOExceptionListener());

    return new SocketIOServer(configuration);
  }

  @Bean
  public JsonSupport jsonSupport(ObjectMapper liveServObjectMapper) {
    return new JacksonJsonSupport() {
      @Override
      public void writeValue(ByteBufOutputStream out, Object value) throws IOException {
        String str = liveServObjectMapper.writeValueAsString(value);
        byte[] bytes = str.getBytes(StandardCharsets.UTF_8);
        out.write(bytes, 0, bytes.length);
        out.flush();
      }
    };
  }
}
