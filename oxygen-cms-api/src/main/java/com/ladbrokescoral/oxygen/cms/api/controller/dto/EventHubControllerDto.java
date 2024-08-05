package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import lombok.Data;

@Data
public class EventHubControllerDto {

  private String id;

  @Brand private String brand;

  private Boolean disabled = false;

  @NotEmpty
  @Pattern(regexp = "^[a-zA-Z0-9_ ]*$", message = "should contain only letters, digits and spaces")
  private String title;

  @NotNull private Integer indexNumber;
}
