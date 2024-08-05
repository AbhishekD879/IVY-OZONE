package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.NetworkIndicatorConfig;
import com.ladbrokescoral.oxygen.cms.api.repository.NetworkIndicatorRepository;
import java.util.Optional;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
public class NetworkIndicatorService extends SortableService<NetworkIndicatorConfig> {
  private NetworkIndicatorRepository networkIndicatorRepository;

  public NetworkIndicatorService(NetworkIndicatorRepository networkIndicatorRepository) {
    super(networkIndicatorRepository);
    this.networkIndicatorRepository = networkIndicatorRepository;
  }

  public ResponseEntity<NetworkIndicatorConfig> readOneByBrand(String brand) {
    Optional<NetworkIndicatorConfig> optionalNetworkIndicatorConfig =
        networkIndicatorRepository.findOneByBrand(brand);

    if (optionalNetworkIndicatorConfig.isPresent()) {
      NetworkIndicatorConfig networkIndicatorConfig = optionalNetworkIndicatorConfig.get();
      return new ResponseEntity<>(networkIndicatorConfig, HttpStatus.OK);
    }

    return new ResponseEntity<>(HttpStatus.NOT_FOUND);
  }
}
