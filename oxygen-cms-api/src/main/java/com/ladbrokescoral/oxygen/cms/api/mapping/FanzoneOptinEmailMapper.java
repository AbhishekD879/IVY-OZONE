package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.FanzoneOptinEmailDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneOptinEmail;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class FanzoneOptinEmailMapper {

  @Autowired private ModelMapper modelMapper;

  public FanzoneOptinEmail toEntity(FanzoneOptinEmailDto dto) {
    return modelMapper.map(dto, FanzoneOptinEmail.class);
  }
}
