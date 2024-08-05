package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.MaintenancePageDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.MaintenancePageMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.MaintenancePageExtendedRepository;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class MaintenancePagePublicService {

  private final MaintenancePageExtendedRepository extendedRepository;

  public MaintenancePagePublicService(MaintenancePageExtendedRepository extendedRepository) {
    this.extendedRepository = extendedRepository;
  }

  public List<MaintenancePageDto> findMaintenanePages(String brand, String deviceType) {

    return extendedRepository.findMaintenancePages(brand, deviceType).stream()
        .map(MaintenancePageMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
