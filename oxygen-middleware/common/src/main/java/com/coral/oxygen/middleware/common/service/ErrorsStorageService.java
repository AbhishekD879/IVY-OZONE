package com.coral.oxygen.middleware.common.service;

import static com.coral.oxygen.middleware.common.configuration.DistributedKey.ERRORS_MAP;
import static java.util.Collections.unmodifiableMap;

import com.coral.oxygen.middleware.common.imdg.DistributedInstance;
import com.coral.oxygen.middleware.common.imdg.DistributedMap;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class ErrorsStorageService {

  private final DistributedInstance distributedInstance;

  public Map<String, Object> getErrors() {
    return unmodifiableMap(getErrorMap());
  }

  public void saveError(String errorKey, String error) {
    getErrorMap().put(errorKey, error);
  }

  public void removeError(String errorKey) {
    getErrorMap().remove(errorKey);
  }

  private DistributedMap<String, Object> getErrorMap() {
    return distributedInstance.getMap(ERRORS_MAP);
  }
}
