package com.entain.oxygen.service;

import reactor.core.publisher.Mono;

public interface BppService {

  Mono<String> favUserdata(String token);
}
