package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/** Created by azayats on 23.11.17. */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class GeneralResponse<T> {
  private T data;
}
