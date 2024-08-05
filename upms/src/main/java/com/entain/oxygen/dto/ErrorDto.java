package com.entain.oxygen.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class ErrorDto {
  private String errorMsg;
  private int errorCode;
}
