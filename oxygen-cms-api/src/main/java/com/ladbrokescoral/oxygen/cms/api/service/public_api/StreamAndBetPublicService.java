package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.StreamAndBetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.StreamAndBet;
import com.ladbrokescoral.oxygen.cms.api.mapping.StreamAndBetMapper;
import com.ladbrokescoral.oxygen.cms.api.service.StreamAndBetService;
import java.util.Collection;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class StreamAndBetPublicService {

  private final StreamAndBetService service;

  public StreamAndBetPublicService(StreamAndBetService service) {
    this.service = service;
  }

  public Optional<List<StreamAndBetDto.SABChildElementDto>> findByBrand(String brand) {
    return service
        .findOneByBrand(brand)
        .map(StreamAndBet::getChildren)
        .map(Collection::stream)
        .map(value -> value.map(StreamAndBetMapper.INSTANCE::toDto).collect(Collectors.toList()));
  }
}
