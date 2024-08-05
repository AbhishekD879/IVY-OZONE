package com.oxygen.publisher.configuration;

import com.corundumstudio.socketio.AckMode;
import com.corundumstudio.socketio.SocketConfig;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.corundumstudio.socketio.Transport;
import com.corundumstudio.socketio.listener.ExceptionListener;
import com.corundumstudio.socketio.protocol.JsonSupport;
import io.netty.channel.ChannelHandlerContext;
import java.io.IOException;
import java.util.List;
import java.util.Objects;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Created by azayats on 30.10.17. */
@Configuration
public class SocketIOServerConfiguration {

  private static final Logger LOGGER = LoggerFactory.getLogger(SocketIOServerConfiguration.class);

  @Bean
  public SocketIOServer socketIOServer(
      @Value("${socket.websocket.port}") int port,
      @Value("${netty.use.linux.native.epoll}") boolean useLinuxEpoll,
      @Value("${netty.boss.threads}") int bossThreads,
      @Value("${netty.worker.threads}") int workerThreads,
      @Value("${socket.context}") String socketContext,
      JsonSupport jsonSupport,
      @Value("${explicitFlushAfterFlushes}") Integer explicitFlushAfterFlushes) {
    com.corundumstudio.socketio.Configuration configuration =
        new com.corundumstudio.socketio.Configuration();
    configuration.setPort(port);
    configuration.setAckMode(AckMode.AUTO);
    configuration.setBossThreads(bossThreads);
    // TODO: Linux native epoll works only on Linux OS
    if (shouldUseEpoll(useLinuxEpoll)) {
      LOGGER.info("Linux Native Epoll is {}.", useLinuxEpoll);
      configuration.setUseLinuxNativeEpoll(useLinuxEpoll);
    }
    configuration.setContext(socketContext);
    configuration.setWorkerThreads(workerThreads);
    configuration.setTransports(Transport.WEBSOCKET, Transport.POLLING);
    SocketConfig socketConfig = new SocketConfig();
    socketConfig.setReuseAddress(true);
    socketConfig.setAcceptBackLog(5_000);
    socketConfig.setTcpReceiveBufferSize(500_000);
    socketConfig.setTcpSendBufferSize(1_000_000);
    configuration.setSocketConfig(socketConfig);
    configuration.setExceptionListener(new SIOExceptionListener());

    configuration.setJsonSupport(jsonSupport);

    final SocketIOServer server = new SocketIOServer(configuration);
    if (shouldUseEpoll(useLinuxEpoll)) {
      server.setPipelineFactory(
          new EpollFlushConsolidationSocketIOChannelInitializer(explicitFlushAfterFlushes));
    }
    return server;
  }

  private boolean shouldUseEpoll(boolean useLinuxEpoll) {
    return useLinuxEpoll && Objects.equals(System.getProperty("os.name"), "Linux");
  }

  private static class SIOExceptionListener implements ExceptionListener {

    @Override
    public void onEventException(Exception ex, List<Object> args, SocketIOClient client) {
      LOGGER.error("OnEventException: ", ex);
    }

    @Override
    public void onDisconnectException(Exception ex, SocketIOClient client) {
      LOGGER.error("OnDisconnectException: ", ex);
    }

    @Override
    public void onConnectException(Exception ex, SocketIOClient client) {
      LOGGER.error("OnConnectException: ", ex);
    }

    public void onPingException(Exception ex, SocketIOClient client) {
      LOGGER.error("onPingException: ", ex);
    }

    /*
     * The exceptionCaught() event handler method is called with a Throwable when an exception was raised by Netty due
     * to an I/O error or by a handler implementation due to the exception thrown while processing events. In most
     * cases, the caught exception should be logged and its associated channel should be closed here.
     */
    @Override
    public boolean exceptionCaught(ChannelHandlerContext ctx, Throwable ex) {
      if (ex instanceof IOException
          && ex.getMessage() != null
          && ex.getMessage().indexOf("Connection reset by peer") >= 0) {
        LOGGER.info(
            "ExceptionCaught: Connection is closed from the client side. Error message '{}'",
            ex.getMessage());
        ctx.disconnect();
        return true;
      } else {
        LOGGER.error("SocketIOServerConfiguration ExceptionCaught: {}", ex.getMessage());
      }
      return false;
    }
  }
}
