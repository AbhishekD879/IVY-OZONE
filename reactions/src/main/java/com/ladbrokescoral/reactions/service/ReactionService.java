package com.ladbrokescoral.reactions.service;

import com.ladbrokescoral.reactions.dto.SurfaceBetInfoRequestDTO;
import com.ladbrokescoral.reactions.dto.UserGlobalCountResponseDTO;
import com.ladbrokescoral.reactions.dto.UserReactionDTO;
import java.util.List;
import java.util.Map;
import reactor.core.publisher.Mono;

/**
 * @author PBalarangakumar 14-06-2023
 */
public interface ReactionService {

  Mono<Boolean> saveReaction(String token, String userName, UserReactionDTO userReactionDTO);

  Mono<String> updateReaction(String token, String userName, UserReactionDTO userReactionDTO);

  Mono<UserGlobalCountResponseDTO> getGlobalCount(
      String custId, List<SurfaceBetInfoRequestDTO> requestDTO);

  Mono<Map<String, Long>> collectGlobalCountFromMongo();
}
