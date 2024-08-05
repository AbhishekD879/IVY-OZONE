package com.coral.oxygen.middleware.ms.quickbet.configuration;

import com.corundumstudio.socketio.AckMode;
import com.corundumstudio.socketio.Configuration;
import com.corundumstudio.socketio.SocketConfig;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.corundumstudio.socketio.Transport;
import com.corundumstudio.socketio.listener.ExceptionListener;
import com.corundumstudio.socketio.protocol.JacksonJsonSupport;
import com.corundumstudio.socketio.protocol.JsonSupport;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import io.netty.buffer.ByteBufOutputStream;
import io.netty.channel.ChannelHandlerContext;
import io.vavr.gson.VavrGson;
import io.vavr.jackson.datatype.VavrModule;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.List;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.slf4j.MDC;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;

@org.springframework.context.annotation.Configuration
public class SocketIOConfiguration {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Bean
  public SocketIOServer socketIOServer(
      @Value("${remote-betslip.websocket.port}") int port,
      JsonSupport jsonSupport,
      @Value("${netty.threads.worker:0}") int workersThreadsAmount,
      @Value("${netty.native-epoll}") boolean useNativeEpoll,
      @Value("${netty.ping-timeout:60000}") int pingTimeout) {
    Configuration configuration = new Configuration();
    configuration.setContext("/quickbet");
    configuration.setPort(port);
    configuration.setAckMode(AckMode.AUTO);
    configuration.setTransports(Transport.WEBSOCKET, Transport.POLLING);
    configuration.setWorkerThreads(workersThreadsAmount);
    SocketConfig socketConfig = new SocketConfig();
    socketConfig.setReuseAddress(true);
    configuration.setSocketConfig(socketConfig);
    configuration.setUseLinuxNativeEpoll(useNativeEpoll);
    configuration.setExceptionListener(new SIOExceptionListener());
    configuration.setJsonSupport(jsonSupport);
    configuration.setPingTimeout(pingTimeout);

    return new SocketIOServer(configuration);
  }

  @Bean
  public Gson gson() {
    GsonBuilder gsonBuilder = VavrGson.registerAll(new GsonBuilder());
    return gsonBuilder.create();
  }

  @Bean
  public JsonSupport jsonSupport(Gson gson) {
    return new JacksonJsonSupport() {

      @Override
      protected void init(ObjectMapper objectMapper) {
        super.init(objectMapper);
        objectMapper.registerModule(new VavrModule());
      }

      @Override
      public void writeValue(ByteBufOutputStream out, Object value) throws IOException {
        String str = gson.toJson(value);
        byte[] bytes = str.getBytes(StandardCharsets.UTF_8);
        out.write(bytes, 0, bytes.length);
        out.flush();
      }
    };
  }

  public static class SIOExceptionListener implements ExceptionListener {
    @Override
    public void onEventException(Exception ex, List<Object> args, SocketIOClient client) {
      ASYNC_LOGGER.error(ex.getMessage(), ex);
      MDC.clear();
    }

    @Override
    public void onDisconnectException(Exception ex, SocketIOClient client) {
      ASYNC_LOGGER.error(ex.getMessage(), ex);
    }

    @Override
    public void onConnectException(Exception ex, SocketIOClient client) {
      ASYNC_LOGGER.error(ex.getMessage(), ex);
    }

    @Override
    public void onPingException(Exception ex, SocketIOClient client) {
      ASYNC_LOGGER.error(ex.getMessage(), ex);
    }

    @Override
    public boolean exceptionCaught(ChannelHandlerContext ctx, Throwable ex) {
      ASYNC_LOGGER.error(ex.getMessage(), ex);
      MDC.clear();
      return false;
    }
  }
}
