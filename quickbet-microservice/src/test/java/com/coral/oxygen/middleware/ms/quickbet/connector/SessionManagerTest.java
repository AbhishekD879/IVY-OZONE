package com.coral.oxygen.middleware.ms.quickbet.connector;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.AssertionsForClassTypes.assertThatThrownBy;
import static org.assertj.core.api.AssertionsForClassTypes.fail;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.SessionNotFoundException;
import com.coral.oxygen.middleware.ms.quickbet.component.SessionRefresherComponent;
import com.coral.oxygen.middleware.ms.quickbet.config.InMemorySessionStorage;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import com.coral.oxygen.middleware.ms.quickbet.impl.SessionStorage;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class SessionManagerTest {
  private static final String SESSION_ID = "123";

  private SessionManager sessionManager;
  private SessionStorage<SessionDto> sessionStorage;
  private SessionRefresherComponent sessionRefresherComponent;

  @BeforeEach
  public void setUp() {
    sessionStorage = new InMemorySessionStorage();
    sessionStorage.persist(new SessionDto(SESSION_ID));
    mockSessionRefresher();
    sessionManager = new SessionManager(sessionStorage, sessionRefresherComponent);
  }

  private void mockSessionRefresher() {
    sessionRefresherComponent = new SessionRefresherComponent(sessionStorage, 10l);
  }

  @Test
  public void testFetchSession() {
    try {
      Session session = sessionManager.loadPersistedSession(SESSION_ID);

      assertThat(session.sessionId()).isEqualTo(SESSION_ID);
    } catch (SessionNotFoundException e) {
      fail("Should fetch session");
    }
  }

  @Test
  public void testFetchMissingSession() {
    assertThatThrownBy(() -> sessionManager.loadPersistedSession("321"))
        .isInstanceOf(SessionNotFoundException.class)
        .hasMessage("ID: 321");
  }

  @Test
  public void testAttachSession() throws SessionNotFoundException {
    UUID clientId = UUID.randomUUID();

    assertThat(sessionManager.getAttachedSession(clientId)).isNull();
    sessionManager.attachSession(clientId, sessionManager.loadPersistedSession(SESSION_ID));
    Session attachedSession = sessionManager.getAttachedSession(clientId);
    assertThat(attachedSession).isNotNull();
    assertThat(attachedSession.sessionId()).isEqualTo(SESSION_ID);
  }

  @Test
  public void testAttachSameSessionTwice() throws SessionNotFoundException {
    UUID clientId = UUID.randomUUID();
    Session session1 = sessionManager.loadPersistedSession(SESSION_ID);
    sessionManager.attachSession(clientId, session1);
    Session session2 = sessionManager.loadPersistedSession(SESSION_ID);
    sessionManager.attachSession(clientId, session2);
    Session attachedSession = sessionManager.getAttachedSession(clientId);
    assertThat(attachedSession).isSameAs(session2);
    assertThat(attachedSession).isNotSameAs(session1);
  }

  @Test
  public void testCreateAndAttach() {
    UUID clientId = UUID.randomUUID();
    sessionManager.createAndAttachNewSession(clientId);
    assertThat(sessionManager.getAttachedSession(clientId)).isNotNull();
  }

  @Test
  public void testDetach() throws SessionNotFoundException {
    UUID clientId = UUID.randomUUID();
    sessionManager.attachSession(clientId, sessionManager.loadPersistedSession(SESSION_ID));
    assertThat(sessionManager.getAttachedSession(clientId)).isNotNull();
    sessionManager.detachSession(clientId);
    assertThat(sessionManager.getAttachedSession(clientId)).isNull();
  }

  @Test
  public void detachWhenThereIsNoSession() {
    try {
      sessionManager.detachSession(UUID.randomUUID());
    } catch (Exception e) {
      fail("Shouldn't throw an exception");
    }
  }

  @Test
  public void detachWithNullClientId() {
    try {
      sessionManager.detachSession(null);
    } catch (Exception e) {
      fail("Shouldn't throw an exception");
    }
  }
}
