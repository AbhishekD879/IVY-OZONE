package com.coral.oxygen.middleware.ms.quickbet.controller;

import com.coral.oxygen.middleware.ms.quickbet.connector.SessionManager;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import com.coral.oxygen.middleware.ms.quickbet.impl.SessionStorage;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Gives insight into microservice state
 *
 * @author volodymyr.masliy
 */
@RestController
@RequestMapping("/qa")
@ConditionalOnProperty(name = "qa.enabled", havingValue = "true")
public class QAController {
  @Autowired private SessionStorage<SessionDto> sessionStorage;
  @Autowired private SessionManager sessionManager;

  @GetMapping("sessions")
  public List<SessionDto> sessions() {
    return sessionStorage.findAll();
  }

  @GetMapping("attachedSessions")
  public Map<UUID, SessionDto> attachedSession() {
    return sessionManager.getAllAttachedSessions();
  }
}
