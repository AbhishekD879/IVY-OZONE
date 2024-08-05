package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DataSelection {

  @NotBlank private String selectionType;

  @NotBlank
  // only integer allowed. Cannot simply change the type to int - will cause a lot of problem for UI
  // can be comma-separated ints for race type Ids
  @Pattern(regexp = "[0-9,]+", message = "allowed only digits and comma if applicable")
  private String selectionId;
}
