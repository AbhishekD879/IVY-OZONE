package com.ladbrokescoral.oxygen.buildyourbetms.dto;

import lombok.Data;

@Data
public class DataResponseWrapper<T> {
  private final T data;
}
