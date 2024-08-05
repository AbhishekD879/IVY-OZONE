package com.entain.oxygen;

import com.coral.bpp.api.model.bet.api.response.UserDataResponse;
import com.coral.bpp.api.service.BppApiAsync;
import com.entain.oxygen.exceptions.UserNotFoundException;
import com.entain.oxygen.service.BppService;
import com.entain.oxygen.service.BppServiceImpl;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@ExtendWith(MockitoExtension.class)
class BppServiceImplTest {

  private BppService bppService;

  @Mock private BppApiAsync bppApiAsyncLight;

  private static final String TOKEN = "2weXc9==";

  @BeforeEach
  public void init() {
    bppService = new BppServiceImpl(bppApiAsyncLight);
  }

  @Test
  void testForBppConnectionException() {

    Mockito.when(bppApiAsyncLight.getFavUserData(Mockito.anyString()))
        .thenReturn(Mono.justOrEmpty(Optional.empty()));

    Mono<String> mono = bppService.favUserdata(TOKEN);
    StepVerifier.create(mono)
        .expectErrorMatches(
            throwable ->
                throwable instanceof UserNotFoundException
                    && throwable
                        .getMessage()
                        .equals("failed to get resp from BPP :: User not Found"))
        .verify();
  }

  @Test
  void testForUserUnauthorizedException() {

    UserDataResponse userDataResponse = new UserDataResponse();
    userDataResponse.setUserValid(false);

    Mockito.when(bppApiAsyncLight.getFavUserData(Mockito.anyString()))
        .thenReturn(Mono.just(userDataResponse));

    Mono<String> mono = bppService.favUserdata(TOKEN);

    StepVerifier.create(mono)
        .expectErrorMatches(
            throwable ->
                throwable instanceof UserNotFoundException
                    && throwable
                        .getMessage()
                        .equals("failed to get resp from BPP :: User not Found"))
        .verify();
  }

  @Test
  void testForExpectExactUser() {
    UserDataResponse userDataResponse = new UserDataResponse();
    userDataResponse.setSportBookUserName("Jon Bones Jones");
    userDataResponse.setUserValid(true);
    userDataResponse.setOxiApiToken("12dret");
    System.out.println();
    Mockito.when(bppApiAsyncLight.getFavUserData(Mockito.anyString()))
        .thenReturn(Mono.just(userDataResponse));
    Mono<String> mono = bppService.favUserdata(TOKEN);
    StepVerifier.create(mono).expectNext("Jon Bones Jones").expectComplete().verify();
  }
}
