package com.ladbrokescoral.oxygen.listeners;

import com.corundumstudio.socketio.listener.DefaultExceptionListener;
import com.corundumstudio.socketio.listener.ExceptionListener;
import io.netty.channel.ChannelHandlerContext;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class LiveServeSIOExceptionListener extends DefaultExceptionListener
    implements ExceptionListener {

  @Override
  public boolean exceptionCaught(ChannelHandlerContext ctx, Throwable e) throws Exception {
    ctx.disconnect();
    log.error("SocketIO exception: ", e);
    return true;
  }
}
