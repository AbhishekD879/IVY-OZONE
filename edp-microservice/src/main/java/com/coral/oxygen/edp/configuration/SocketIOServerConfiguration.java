package com.coral.oxygen.edp.configuration;

import com.corundumstudio.socketio.AckMode;
import com.corundumstudio.socketio.SocketConfig;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.corundumstudio.socketio.Transport;
import com.corundumstudio.socketio.listener.ExceptionListener;
import com.corundumstudio.socketio.protocol.JacksonJsonSupport;
import com.corundumstudio.socketio.protocol.JsonSupport;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.netty.buffer.ByteBufOutputStream;
import io.netty.channel.ChannelHandlerContext;
import java.io.IOException;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@Slf4j
public class SocketIOServerConfiguration {

  @Bean
  public SocketIOServer socketIOServer(
      @Value("${edp.websocket.port}") int port, JsonSupport jsonSupport) {
    com.corundumstudio.socketio.Configuration configuration =
        new com.corundumstudio.socketio.Configuration();
    configuration.setContext("/edp");
    configuration.setPort(port);
    configuration.setAckMode(AckMode.AUTO);
    configuration.setTransports(Transport.WEBSOCKET, Transport.POLLING);
    SocketConfig socketConfig = new SocketConfig();
    socketConfig.setReuseAddress(true);
    configuration.setSocketConfig(socketConfig);
    configuration.setExceptionListener(new SIOExceptionListener());

    configuration.setJsonSupport(jsonSupport);

    return new SocketIOServer(configuration);
  }

  @Bean
  public JsonSupport jsonSupport(ObjectMapper mapper) {
    return new JacksonJsonSupport() {
      @Override
      public void writeValue(ByteBufOutputStream out, Object value) throws IOException {
        byte[] serializedObj = mapper.writeValueAsBytes(value);
        out.write(serializedObj, 0, serializedObj.length);
        out.flush();
      }
    };
  }

  private static class SIOExceptionListener implements ExceptionListener {

    @Override
    public void onEventException(Exception ex, List<Object> args, SocketIOClient client) {
      log.error("", ex);
    }

    @Override
    public void onDisconnectException(Exception ex, SocketIOClient client) {
      log.error("", ex);
    }

    @Override
    public void onConnectException(Exception ex, SocketIOClient client) {
      log.error("", ex);
    }

    @Override
    public void onPingException(Exception ex, SocketIOClient client) {
      log.error("", ex);
    }

    /**
     * The exceptionCaught() event handler method is called with a Throwable when an exception was
     * raised by Netty due to an I/O error or by a handler implementation due to the exception
     * thrown while processing events. In most cases, the caught exception should be logged and its
     * associated channel should be closed here.
     */
    @Override
    public boolean exceptionCaught(ChannelHandlerContext ctx, Throwable ex) {
      if (ex instanceof IOException && "Connection reset by peer".equals(ex.getMessage())) {
        log.info(
            "ExceptionCaught: Connection is closed from the client side. Error message '{}'",
            ex.getMessage());
        ctx.disconnect();
        return true;
      }
      log.error("ExceptionCaught: ", ex);
      return false;
    }
  }
}
