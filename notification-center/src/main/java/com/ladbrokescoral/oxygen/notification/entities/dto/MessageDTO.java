package com.ladbrokescoral.oxygen.notification.entities.dto;

import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor(staticName = "from")
@Data
public class MessageDTO {
  @NotNull private final String message;
}
