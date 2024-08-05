package com.ladbrokescoral.oxygen.questionengine.model;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
public final class Pageable {
  private final int pageNumber;
  private final int pageSize;

  public int offset() {
    return pageNumber * pageSize;
  }

  public int limit() {
    return pageSize;
  }

  public static Pageable firstPage(int pageSize) {
    return new Pageable(0, pageSize);
  }

  public static Pageable emptyPage() {
    return new Pageable(0, 0);
  }
}
