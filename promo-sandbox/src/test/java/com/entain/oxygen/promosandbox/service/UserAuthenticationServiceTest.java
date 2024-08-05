package com.entain.oxygen.promosandbox.service;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import com.entain.oxygen.promosandbox.dto.bpp.UserData;
import com.entain.oxygen.promosandbox.exception.BppTokenRequiredException;
import com.entain.oxygen.promosandbox.exception.InvalidBppTokenException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpMethod;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@ExtendWith(MockitoExtension.class)
class UserAuthenticationServiceTest {

  @Mock private WebClient webClient;

  @Mock WebClient.RequestBodyUriSpec requestBodyUriSpec;

  @Mock WebClient.RequestHeadersSpec requestHeadersSpec;

  @Mock WebClient.RequestBodySpec requestBodySpec;

  @Mock WebClient.ResponseSpec responseSpec;

  private UserAuthenticationService userAuthenticationService;

  @BeforeEach
  public void setUp() {
    MockitoAnnotations.openMocks(this);
    userAuthenticationService = new UserAuthenticationService(webClient);
  }

  @Test
  void validateTokenSuccessTest() {
    ReflectionTestUtils.setField(userAuthenticationService, "enableSecurity", true);
    when(webClient.method(HttpMethod.POST)).thenReturn(requestBodyUriSpec);
    when(requestBodyUriSpec.uri("/auth/userdata")).thenReturn(requestBodySpec);
    when(requestBodySpec.body(any())).thenReturn(requestHeadersSpec);
    when(requestHeadersSpec.accept(any())).thenReturn(requestBodySpec);
    UserData userData = new UserData();
    userData.setUserValid(true);
    when(requestBodySpec.retrieve()).thenReturn(responseSpec);
    when(responseSpec.bodyToMono((Class<Object>) any())).thenReturn(Mono.just(userData));

    assertTrue(userData.isUserValid());
    userAuthenticationService.validateToken("Test123", "123");
  }

  @Test
  void validateTokenInvalidTokenTest() {
    ReflectionTestUtils.setField(userAuthenticationService, "enableSecurity", true);
    when(webClient.method(HttpMethod.POST)).thenReturn(requestBodyUriSpec);
    when(requestBodyUriSpec.uri("/auth/userdata")).thenReturn(requestBodySpec);
    when(requestBodySpec.body(any())).thenReturn(requestHeadersSpec);
    when(requestHeadersSpec.accept(any())).thenReturn(requestBodySpec);
    when(requestBodySpec.retrieve()).thenReturn(responseSpec);
    UserData userData = new UserData();
    userData.setUserValid(false);
    when(responseSpec.bodyToMono((Class<Object>) any())).thenReturn(Mono.just(userData));

    assertThrows(
        InvalidBppTokenException.class,
        () -> userAuthenticationService.validateToken("Test123", "123"));
  }

  @Test
  void validateWhenTokenIsNullTest() {
    ReflectionTestUtils.setField(userAuthenticationService, "enableSecurity", true);
    when(webClient.method(HttpMethod.POST)).thenReturn(requestBodyUriSpec);
    when(requestBodyUriSpec.uri("/auth/userdata")).thenReturn(requestBodySpec);
    when(requestBodySpec.body(any())).thenReturn(requestHeadersSpec);
    when(requestHeadersSpec.accept(any())).thenReturn(requestBodySpec);
    when(requestBodySpec.retrieve()).thenReturn(responseSpec);
    when(responseSpec.bodyToMono((Class<Object>) any())).thenReturn(Mono.empty());

    assertThrows(
        InvalidBppTokenException.class,
        () -> userAuthenticationService.validateToken("Test123", "123"));
  }

  @Test
  void validateTokenFailureTest() {
    ReflectionTestUtils.setField(userAuthenticationService, "enableSecurity", true);
    assertThrows(
        InvalidBppTokenException.class,
        () -> userAuthenticationService.validateToken("Test123", "123"));
  }

  @Test
  void validateTokenEnableSecurityFalseTest() {
    ReflectionTestUtils.setField(userAuthenticationService, "enableSecurity", false);
    assertNotNull(userAuthenticationService);
    userAuthenticationService.validateToken("Test123", "123");
  }

  @Test
  void validateWhenTokenESTrueAndNoIdTest() {
    ReflectionTestUtils.setField(userAuthenticationService, "enableSecurity", true);
    assertDoesNotThrow(() -> userAuthenticationService.validateToken("Test123", ""));
    verify(webClient, never()).method(any());
  }

  @Test
  void testWhenTokenIsMissing() {
    String customerId = "value123";
    String token = null;
    assertThrows(
        BppTokenRequiredException.class,
        () -> userAuthenticationService.validateTokenAndCustomerId(token, customerId));
  }

  @Test
  void testWhenValidTokenCustIdPresent() {
    String customerId = "value345";
    String token = "datavalue";
    assertDoesNotThrow(
        () -> userAuthenticationService.validateTokenAndCustomerId(token, customerId));
  }

  @Test
  void testBothTokenAndCusIdNull() {
    String customerId = null;
    String token = null;
    assertDoesNotThrow(
        () -> userAuthenticationService.validateTokenAndCustomerId(token, customerId));
  }
}
