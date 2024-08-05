package com.oxygen.publisher.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.Objects;
import lombok.RequiredArgsConstructor;
import okhttp3.HttpUrl;
import org.springframework.stereotype.Component;
import retrofit2.Converter;
import retrofit2.Retrofit;
import retrofit2.converter.jackson.JacksonConverterFactory;

/**
 * Manages {@link Retrofit} clients creation.
 *
 * @author tvuyiv
 */
@Component
@RequiredArgsConstructor
public class RetrofitClientFactory {

  private final ObjectMapper objectMapper;

  /**
   * Create a HTTP {@link Retrofit} relation of the given class, host, port and {@link
   * Converter.Factory}.
   *
   * @param host the host
   * @param port the port
   * @param client the relation class
   * @param <T> relation type
   * @param converterFactory factory to create serializer/deserializer
   * @return built {@link Retrofit} relation
   */
  public <T> T createClient(
      String host, Integer port, Class<T> client, Converter.Factory converterFactory) {
    Objects.requireNonNull(host);
    Objects.requireNonNull(port);

    return new Retrofit.Builder()
        .baseUrl(new HttpUrl.Builder().scheme("http").host(host).port(port).build())
        .addConverterFactory(converterFactory)
        .build()
        .create(client);
  }

  /**
   * Create a HTTP {@link Retrofit} relation of the given class, host and port. Uses Jackson for
   * serialization/deserialization.
   *
   * @param host the host
   * @param port the port
   * @param client the relation class
   * @param <T> relation type
   * @return built {@link Retrofit} relation
   */
  public <T> T createClient(String host, Integer port, Class<T> client) {
    return createClient(host, port, client, JacksonConverterFactory.create(objectMapper));
  }
}
