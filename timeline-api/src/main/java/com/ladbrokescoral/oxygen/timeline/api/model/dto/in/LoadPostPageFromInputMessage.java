package com.ladbrokescoral.oxygen.timeline.api.model.dto.in;

import com.ladbrokescoral.oxygen.timeline.api.model.dto.out.OutputMessageDto;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class LoadPostPageFromInputMessage extends InputMessage {
  private OutputMessageDto.TimeBasedId from;
}
