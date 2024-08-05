package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataSportDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SportDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Sport;
import com.ladbrokescoral.oxygen.cms.api.mapping.SportMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.SportRepository;
import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class SportPublicService {

  private SportRepository repository;

  public SportPublicService(SportRepository repository) {
    this.repository = repository;
  }

  public List<SportDto> find(String brand) {
    return getSports(brand).stream().map(SportMapper.INSTANCE::toDto).collect(Collectors.toList());
  }

  public List<InitialDataSportDto> findInitialData(String brand) {
    return getSports(brand).stream()
        .map(SportMapper.INSTANCE::toInitialDto)
        .collect(Collectors.toList());
  }

  public Collection<Sport> getSports(String brand) {
    return repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE);
  }
}
