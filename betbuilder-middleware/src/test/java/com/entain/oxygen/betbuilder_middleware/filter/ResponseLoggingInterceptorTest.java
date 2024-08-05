package com.entain.oxygen.betbuilder_middleware.filter;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.springframework.core.io.buffer.DataBuffer;
import org.springframework.http.HttpStatus;
import org.springframework.mock.http.server.reactive.MockServerHttpResponse;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import reactor.core.publisher.Flux;
import reactor.test.StepVerifier;

@ExtendWith(SpringExtension.class)
class ResponseLoggingInterceptorTest {
  @Mock private ByteArrayOutputStream baos;

  @Test
  void writeWith_IOException() {
    MockServerHttpResponse response = new MockServerHttpResponse();
    response.setStatusCode(HttpStatus.OK);
    DataBuffer mockDataBuffer = Mockito.mock(DataBuffer.class);
    Mockito.when(mockDataBuffer.toByteBuffer())
        .thenAnswer(
            invocation -> {
              throw new IOException("Error reading data");
            });

    Flux<DataBuffer> buffer = Flux.just(mockDataBuffer);

    long startTime = System.currentTimeMillis();
    ResponseLoggingInterceptor interceptor =
        new ResponseLoggingInterceptor(response, startTime, "/price", "abc");

    StepVerifier.create(interceptor.writeWith(buffer)).expectComplete().verify();
  }

  @Test
  void writeWith_ClosedStreamException() {

    MockServerHttpResponse response = new MockServerHttpResponse();
    response.setStatusCode(HttpStatus.OK);

    DataBuffer mockDataBuffer = Mockito.mock(DataBuffer.class);

    Mockito.when(mockDataBuffer.toByteBuffer())
        .thenAnswer(
            invocation -> {
              throw new IOException("Error reading data");
            });

    Flux<DataBuffer> buffer = Flux.just(mockDataBuffer);

    long startTime = System.currentTimeMillis();
    ResponseLoggingInterceptor interceptor =
        new ResponseLoggingInterceptor(response, startTime, "/price", "abc") {
          @Override
          protected ByteArrayOutputStream createByteArrayOutputStream() {
            return new ByteArrayOutputStream() {
              @Override
              public void close() throws IOException {
                throw new IOException("Error closing stream");
              }
            };
          }
        };

    StepVerifier.create(interceptor.writeWith(buffer)).expectComplete().verify();
  }
}
