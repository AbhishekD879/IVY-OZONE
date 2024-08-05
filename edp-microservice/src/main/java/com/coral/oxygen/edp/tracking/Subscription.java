package com.coral.oxygen.edp.tracking;

import lombok.Getter;

/** Created by azayats on 18.12.17. */
@Getter
public abstract class Subscription<T, D> {

  private final String clientId;

  private final T ticket;

  private int chunksToReturn;

  public Subscription(String clientId, T ticket, int chunksToReturn) {
    this.clientId = clientId;
    this.ticket = ticket;
    this.chunksToReturn = chunksToReturn;
  }

  public abstract void emit(D data);
}
