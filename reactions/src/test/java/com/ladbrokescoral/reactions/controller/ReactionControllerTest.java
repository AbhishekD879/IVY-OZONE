package com.ladbrokescoral.reactions.controller;

import static org.mockito.Mockito.*;

import com.ladbrokescoral.reactions.config.ReactiveMongoConfig;
import com.ladbrokescoral.reactions.dto.Reaction;
import com.ladbrokescoral.reactions.dto.UserGlobalCountInfo;
import com.ladbrokescoral.reactions.dto.UserGlobalCountResponseDTO;
import com.ladbrokescoral.reactions.dto.UserReactionDTO;
import com.ladbrokescoral.reactions.exception.ServiceExecutionException;
import com.ladbrokescoral.reactions.repository.mongo.MongoUserRepository;
import com.ladbrokescoral.reactions.repository.redis.RedisOperations;
import com.ladbrokescoral.reactions.scheduler.ReactionsCleanupScheduledTask;
import com.ladbrokescoral.reactions.service.ReactionService;
import java.io.IOException;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.reactive.WebFluxTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.reactive.server.WebTestClient;
import reactor.core.publisher.Mono;

@WebFluxTest(ReactionController.class)
@Import(ReactiveMongoConfig.class)
class ReactionControllerTest {
  @Autowired private WebTestClient webTestClient;

  @Autowired private ReactionController reactionController;

  @MockBean private ReactionService reactionService;

  @MockBean private ReactionsCleanupScheduledTask reactionsCleanupScheduledTask;
  @MockBean private RedisOperations redisOperations;

  @MockBean private MongoUserRepository userRepository;

  private UserReactionDTO userReactionDTO;

  @BeforeEach
  void init() throws IOException {
    userReactionDTO = new UserReactionDTO("1", "1", "1", Reaction.REACTION1);
  }

  @Test
  void testSaveReaction() throws IOException {
    when(reactionService.saveReaction("token", "userName", userReactionDTO))
        .thenReturn(Mono.just(Boolean.TRUE));
    webTestClient
        .post()
        .uri("/reactions")
        .contentType(MediaType.APPLICATION_JSON)
        .header("token", "token")
        .header("userName", "username")
        .bodyValue(userReactionDTO)
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody(Boolean.class);
  }

  @Test
  void testUpdateReaction() throws IOException {
    when(reactionService.saveReaction("token", "userName", userReactionDTO))
        .thenReturn(Mono.just(Boolean.TRUE));
    webTestClient
        .put()
        .uri("/reactions")
        .contentType(MediaType.APPLICATION_JSON)
        .header("token", "token")
        .header("userName", "username")
        .bodyValue(userReactionDTO)
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody(String.class);
  }

  @Test
  void testCleanupMongoOldRecords() throws Exception {
    when(reactionsCleanupScheduledTask.cleanupProcess()).thenReturn(Mono.just(true));
    webTestClient
        .delete()
        .uri("/reactions")
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody(Void.class);
  }

  @Test
  void testRedisCleanUp() throws Exception {
    when(redisOperations.cleanUpAllRedisKeys()).thenReturn(Mono.just("test"));
    webTestClient
        .delete()
        .uri("/reactions/redis/cleanup")
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody(Void.class);
  }

  @Test
  void testCleanupMongoOldRecordsException() throws Exception {
    doThrow(new ServiceExecutionException("Error"))
        .when(reactionsCleanupScheduledTask)
        .cleanupProcess();
    webTestClient
        .delete()
        .uri("/reactions")
        .exchange()
        .expectStatus()
        .is5xxServerError()
        .expectBody(Void.class);
  }

  @Test
  void testGetGlobalCount() {
    UserGlobalCountInfo userGlobalCountInfo = new UserGlobalCountInfo(1l, 1l, 1l, "1");
    Map<String, UserGlobalCountInfo> reactions = new HashMap<>();
    reactions.put("1", userGlobalCountInfo);
    when(reactionService.getGlobalCount("custId", Collections.emptyList()))
        .thenReturn(Mono.just(new UserGlobalCountResponseDTO("1", reactions)));
    webTestClient
        .post()
        .uri("/reactions/{custId}", "custId")
        .bodyValue(Collections.emptyList())
        .exchange()
        .expectStatus()
        .isOk()
        .expectBody(UserGlobalCountResponseDTO.class)
        .isEqualTo(new UserGlobalCountResponseDTO("1", reactions));
  }
}
