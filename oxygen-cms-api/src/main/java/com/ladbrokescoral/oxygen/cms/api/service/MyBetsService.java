package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.MyBetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.MyBet;
import com.ladbrokescoral.oxygen.cms.api.repository.MyBetsRepository;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
public class MyBetsService extends AbstractService<MyBet> {
  private final ModelMapper modelMapper;

  public MyBetsService(MyBetsRepository repository, ModelMapper modelMapper) {
    super(repository);
    this.modelMapper = modelMapper;
  }

  public MyBet convertDtoToEntity(MyBetDto myBetDto) {
    return modelMapper.map(myBetDto, MyBet.class);
  }
}
