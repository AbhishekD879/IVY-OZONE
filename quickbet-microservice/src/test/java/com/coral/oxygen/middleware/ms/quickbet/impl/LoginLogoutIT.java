package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.LOGOUT;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.LOGOUT_SUCCESS;
import static org.assertj.core.api.Assertions.assertThat;

import com.coral.oxygen.middleware.ms.quickbet.connector.SessionManager;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import com.coral.oxygen.middleware.ms.quickbet.utils.WebSocketTestClient;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

@IntegrationTest
class LoginLogoutIT {

  @Autowired private WebSocketTestClient client;

  @Autowired private SessionManager sessionManager;

  @Autowired private SessionStorage<SessionDto> sessionStorage;

  @Test
  void shouldSaveTokenToSession() {
    // given
    String bppToken = "90v02f903fi230f72";

    // when
    client.login(bppToken);

    // then
    assertThat(loadSession().getToken()).isEqualTo(bppToken);
  }

  @Test
  void shouldRemoveTokenFromSession() {
    // given
    shouldSaveTokenToSession();

    // when
    client.emitWithWaitForResponse(LOGOUT, "{}", LOGOUT_SUCCESS);

    // then
    assertThat(loadSession().getToken()).isNull();
  }

  private SessionDto loadSession() {
    return sessionStorage.find(client.getSessionId()).get();
  }
}
