package com.entain.oxygen.service;

import com.coral.bpp.api.model.bet.api.response.UserDataResponse;
import com.coral.bpp.api.service.BppApiAsync;
import com.entain.oxygen.exceptions.UserNotFoundException;
import lombok.RequiredArgsConstructor;
import org.apache.commons.lang3.ObjectUtils;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
@RequiredArgsConstructor
public class BppServiceImpl implements BppService {

  private final BppApiAsync bppApiAsyncLight;

  @Override
  public Mono<String> favUserdata(String token) {
    return bppApiAsyncLight
        .getFavUserData(token)
        .filter(ObjectUtils::isNotEmpty)
        .filter(UserDataResponse::getUserValid)
        .map(UserDataResponse::getSportBookUserName)
        .switchIfEmpty(Mono.defer(this::error));
  }

  private Mono<String> error() {
    return Mono.error(new UserNotFoundException("failed to get resp from BPP :: User not Found"));
  }
}
