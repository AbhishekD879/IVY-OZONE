package com.ladbrokescoral.oxygen.questionengine.service;

import com.ladbrokescoral.oxygen.questionengine.dto.AbstractQuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.UpsellDto;

import java.util.Optional;

public interface UpsellService {
  Optional<UpsellDto> findUpsellFor(AbstractQuizDto quiz);
}
