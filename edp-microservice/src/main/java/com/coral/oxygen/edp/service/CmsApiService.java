package com.coral.oxygen.edp.service;

import com.ladbrokescoral.oxygen.cms.client.model.StreamAndBetDto;
import java.util.List;
import java.util.Optional;

public interface CmsApiService {
  Optional<List<StreamAndBetDto>> getStreamAndBetDto();
}
