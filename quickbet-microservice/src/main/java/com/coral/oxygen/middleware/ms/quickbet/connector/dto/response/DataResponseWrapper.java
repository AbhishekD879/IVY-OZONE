package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * @author volodymyr.masliy
 */
@Data
@AllArgsConstructor
public class DataResponseWrapper<T> {
  private T data;
}
