package com.coral.oxygen.middleware.ms.quickbet.impl;

import java.util.List;
import java.util.Optional;

/**
 * @author volodymyr.masliy
 */
public interface SessionStorage<T> {
  boolean refreshTtl(String sessionId);

  Optional<T> find(String sessionId);

  List<T> findAll();

  void persist(T session);
}
