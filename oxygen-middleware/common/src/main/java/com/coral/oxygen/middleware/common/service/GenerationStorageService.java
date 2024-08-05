package com.coral.oxygen.middleware.common.service;

import static com.coral.oxygen.middleware.common.configuration.DistributedKey.GENERATION_MAP;

import com.coral.oxygen.middleware.common.imdg.DistributedInstance;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class GenerationStorageService {

  private static final String NEWLINE_AND_SPACES_REGEX = "\\r\\n|\\r|\\n|\\s+";

  private DistributedInstance distributedInstance;

  @Autowired
  public GenerationStorageService(DistributedInstance distributedInstance) {
    this.distributedInstance = distributedInstance;
  }

  public void putLatest(GenerationKeyType generationKeyType, String value) {
    String valueToPut = String.valueOf(value);
    String valueToLog = valueToPut.replaceAll(NEWLINE_AND_SPACES_REGEX, "");
    log.info("Set latest version of {} to value: {}", generationKeyType.getKey(), valueToLog);
    distributedInstance.updateExpirableValue(
        GENERATION_MAP, generationKeyType.getKey(), valueToPut);
  }

  public String getLatest(GenerationKeyType generationKeyType) {
    return distributedInstance.getValue(GENERATION_MAP, generationKeyType.getKey());
  }
}
