package com.ladbrokescoral.oxygen.cms.api.entity;

import java.io.Serializable;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Name implements Serializable {

  private static final long serialVersionUID = 3217056729586763610L;

  private String first;
  private String last;
}
