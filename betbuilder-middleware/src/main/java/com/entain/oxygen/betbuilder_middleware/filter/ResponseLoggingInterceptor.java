package com.entain.oxygen.betbuilder_middleware.filter;

import com.entain.oxygen.betbuilder_middleware.service.BBUtil;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.channels.Channels;
import java.nio.charset.StandardCharsets;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.jetbrains.annotations.NotNull;
import org.reactivestreams.Publisher;
import org.slf4j.MDC;
import org.springframework.context.annotation.Lazy;
import org.springframework.core.io.buffer.DataBuffer;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.http.server.reactive.ServerHttpResponseDecorator;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Lazy
@Component
public class ResponseLoggingInterceptor extends ServerHttpResponseDecorator {
  private static final Logger ASYNC_LOGGER = LogManager.getLogger();

  private final long startTime;
  private final String txnPath;
  private final String correlation;

  public ResponseLoggingInterceptor(
      ServerHttpResponse delegate, long startTime, String txnPath, String correlation) {
    super(delegate);
    this.startTime = startTime;
    this.correlation = correlation;
    this.txnPath = txnPath;
  }

  protected ByteArrayOutputStream createByteArrayOutputStream() {
    return new ByteArrayOutputStream();
  }

  @NotNull
  @Override
  public Mono<Void> writeWith(@NotNull Publisher<? extends DataBuffer> body) {
    Flux<DataBuffer> buffer = Flux.from(body);
    return super.writeWith(
        buffer.doOnNext(
            (DataBuffer dataBuffer) -> {
              ByteArrayOutputStream baos = createByteArrayOutputStream();
              try (baos) {
                if (!txnPath.equals("/actuator/health")) {
                  Channels.newChannel(baos).write(dataBuffer.toByteBuffer().asReadOnlyBuffer());
                  String bodyRes = baos.toString(StandardCharsets.UTF_8);
                  MDC.put(BBUtil.LCG_STATUS_KEY, String.valueOf(getStatusCode().value()));

                  MDC.put(BBUtil.LCG_RESPONSE_KEY, bodyRes);
                  MDC.put(BBUtil.TRANSACTION_PATH, txnPath);
                  MDC.put(BBUtil.CORRELATION_ID, correlation);
                  ASYNC_LOGGER.info(
                      "Response Time Taken :{} ms, status= {} ",
                      System.currentTimeMillis() - startTime,
                      getStatusCode());
                }
              } catch (IOException e) {
                ASYNC_LOGGER.error("{}", e.getMessage());
              } finally {
                MDC.clear();
              }
            }));
  }
}
