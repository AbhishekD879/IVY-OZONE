package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.SecretBaseDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SecretDetailedDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Secret;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class SecretMapper {

  @Autowired private ModelMapper modelMapper;

  public Secret toEntity(SecretDetailedDto dto) {
    return modelMapper.map(dto, Secret.class);
  }

  public SecretDetailedDto toDetailedDto(Secret entity) {
    return modelMapper.map(entity, SecretDetailedDto.class);
  }

  public SecretBaseDto toBaseDto(Secret entity) {
    return modelMapper.map(entity, SecretBaseDto.class);
  }
}
