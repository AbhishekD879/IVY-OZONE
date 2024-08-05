package com.ladbrokescoral.cashout.service.updates;

import reactor.core.Disposable;
import reactor.core.publisher.FluxSink;

public interface BufferedDisposable<T> {
  Disposable getDisposable();

  FluxSink<T> getSink();
}
