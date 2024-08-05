package com.ladbrokescoral.cashout.socketio;

import com.corundumstudio.socketio.AuthorizationListener;
import com.corundumstudio.socketio.HandshakeData;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.listener.ExceptionListener;
import io.netty.channel.ChannelHandlerContext;
import java.io.IOException;
import java.util.List;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;

@Component
public class SocketIoServerConfig {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Bean
  public AuthorizationListener authorizationListener() {
    return handshakeData -> {
      boolean hasToken = hasToken(handshakeData);
      if (!hasToken) {
        ASYNC_LOGGER.warn("No token present in connection from {}", handshakeData.getAddress());
      }
      return hasToken;
    };
  }

  @Bean
  public ExceptionListener exceptionListener() {
    return new SIOExceptionListener();
  }

  private boolean hasToken(HandshakeData data) {
    return data.getSingleUrlParam("token") != null;
  }

  private static class SIOExceptionListener implements ExceptionListener {

    @Override
    public void onEventException(Exception ex, List<Object> args, SocketIOClient client) {
      ASYNC_LOGGER.error("OnEventException: ", ex);
    }

    @Override
    public void onDisconnectException(Exception ex, SocketIOClient client) {
      ASYNC_LOGGER.error("OnDisconnectException: ", ex);
    }

    @Override
    public void onConnectException(Exception ex, SocketIOClient client) {
      ASYNC_LOGGER.error("OnConnectException: ", ex);
    }

    public void onPingException(Exception ex, SocketIOClient client) {
      ASYNC_LOGGER.error("onPingException: ", ex);
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
        ASYNC_LOGGER.error(
            "ExceptionCaught: Connection is closed from the client side. Error message '{}'",
            ex.getMessage());
        ctx.disconnect();
        return true;
      } else {
        ASYNC_LOGGER.error("SocketIOServerConfiguration ExceptionCaught: {}", ex.getMessage());
      }
      return false;
    }
  }
}
