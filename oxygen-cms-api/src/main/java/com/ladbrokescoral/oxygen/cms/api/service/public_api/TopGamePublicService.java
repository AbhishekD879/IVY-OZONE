package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.TopGameDto;
import com.ladbrokescoral.oxygen.cms.api.entity.TopGame;
import com.ladbrokescoral.oxygen.cms.api.mapping.TopGameMapper;
import com.ladbrokescoral.oxygen.cms.api.service.TopGameService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class TopGamePublicService {

  private final TopGameService service;

  public TopGamePublicService(TopGameService service) {
    this.service = service;
  }

  public List<TopGameDto> findByBrand(String brand) {
    List<TopGame> topGameCollection = service.findAllByBrandSorted(brand);
    return topGameCollection.stream()
        .map(TopGameMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
