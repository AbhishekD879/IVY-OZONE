package com.entain.oxygen.betbuilder_middleware.service.helper;

import com.entain.oxygen.betbuilder_middleware.api.request.Combination;
import com.entain.oxygen.betbuilder_middleware.redis.dto.CombinationCache;
import com.entain.oxygen.betbuilder_middleware.redis.dto.SelectionDto;
import java.util.List;
import org.modelmapper.ModelMapper;
import org.modelmapper.TypeToken;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class CacheServiceHelper {
  private final ModelMapper modelMapper;

  @Autowired
  public CacheServiceHelper(ModelMapper modelMapper) {
    this.modelMapper = modelMapper;
  }

  public CombinationCache buildCombinationCache(Combination combination, String hash) {
    modelMapper.map(combination.getSelections(), new TypeToken<List<SelectionDto>>() {}.getType());
    CombinationCache combinationCache = modelMapper.map(combination, CombinationCache.class);
    combinationCache.setHash(hash);
    return combinationCache;
  }
}
