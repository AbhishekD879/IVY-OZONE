package com.oxygen.publisher.configuration;

import com.corundumstudio.socketio.SocketIOChannelInitializer;
import io.netty.channel.ChannelPipeline;
import io.netty.handler.flush.FlushConsolidationHandler;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
public class EpollFlushConsolidationSocketIOChannelInitializer extends SocketIOChannelInitializer {

  private final int explicitFlushAfterFlushes;

  @Override
  protected void addSocketioHandlers(ChannelPipeline pipeline) {
    pipeline.addFirst(new FlushConsolidationHandler(explicitFlushAfterFlushes));
    super.addSocketioHandlers(pipeline);
  }
}
