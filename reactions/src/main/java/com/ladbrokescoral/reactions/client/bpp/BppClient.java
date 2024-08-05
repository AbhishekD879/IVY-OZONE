package com.ladbrokescoral.reactions.client.bpp;

import com.ladbrokescoral.reactions.client.bpp.dto.UserData;
import reactor.core.publisher.Mono;

/**
 * @author PBalarangakumar 15-06-2023
 */
public interface BppClient {

  Mono<UserData> getValidUser(String token);
}
