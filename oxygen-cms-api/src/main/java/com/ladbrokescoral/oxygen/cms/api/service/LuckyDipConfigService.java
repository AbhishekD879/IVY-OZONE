package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipConfigurationDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipConfiguration;
import com.ladbrokescoral.oxygen.cms.api.repository.LuckyDipConfigRepository;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class LuckyDipConfigService extends AbstractService<LuckyDipConfiguration> {

  private final ModelMapper modelMapper;

  @Autowired
  public LuckyDipConfigService(LuckyDipConfigRepository repository, ModelMapper modelMapper) {
    super(repository);
    this.modelMapper = modelMapper;
  }

  public LuckyDipConfiguration convertDtoToEntity(LuckyDipConfigurationDto luckyDipConfigDto) {
    return modelMapper.map(luckyDipConfigDto, LuckyDipConfiguration.class);
  }
}
