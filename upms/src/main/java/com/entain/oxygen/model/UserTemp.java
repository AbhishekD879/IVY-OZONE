package com.entain.oxygen.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class UserTemp {

  private String originalUserName;
  private String hashedUserName;
}
