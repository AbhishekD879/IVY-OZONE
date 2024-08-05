package com.coral.oxygen.middleware.ms.quickbet.connector;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.coral.bpp.api.model.bet.api.response.ErrorBody;
import com.coral.bpp.api.model.bet.api.response.GeneralResponse;
import com.coral.bpp.api.model.bet.api.response.UserDataResponse;
import com.coral.bpp.api.service.BppService;
import io.vavr.control.Try;
import java.net.SocketTimeoutException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

class BppComponentTest {
  private BppComponent bppComponent;
  private BppService bppService;

  @BeforeEach
  void setUp() {
    bppService = Mockito.mock(BppService.class);
    bppComponent = new BppComponent(bppService);
  }

  @Test
  void testUserDataReturnedSuccessfully() {
    UserDataResponse userDataResponse = new UserDataResponse();
    userDataResponse.setOxiApiToken("123");
    userDataResponse.setSportBookUserName("Test");
    when(bppService.userData(any())).thenReturn(new GeneralResponse<>(userDataResponse, null));

    Try<UserDataResponse> userData = bppComponent.fetchUserData("123");

    assertThat(userData.isSuccess()).isTrue();
    assertThat(userData.get().getOxiApiToken()).isEqualTo("123");
    assertThat(userData.get().getSportBookUserName()).isEqualTo("Test");
  }

  @Test
  void testErrorBodyReturned() {
    ErrorBody errorBody = new ErrorBody();
    errorBody.setCode("1");
    errorBody.setMessage("Test");
    when(bppService.userData(any())).thenReturn(new GeneralResponse<>(null, errorBody));

    Try<UserDataResponse> userData = bppComponent.fetchUserData("123");
    assertThat(userData.isFailure()).isTrue();
    userData.onFailure(
        (e) -> {
          assertThat(e).isInstanceOf(BppComponent.BppErrorException.class);

          ErrorBody error = ((BppComponent.BppErrorException) e).getErrorBody();
          assertThat(error.getCode()).isEqualTo("1");
        });
  }

  @Test
  void testEmptyUserDataReturned() {
    when(bppService.userData(any())).thenReturn(new GeneralResponse<>(null, null));
    Try<UserDataResponse> userData = bppComponent.fetchUserData("123");
    assertThat(userData.isSuccess()).isFalse();
    assertThat(userData.isFailure()).isTrue();
    userData.onFailure(e -> assertThat(e).isInstanceOf(BppComponent.BppAuthException.class));
  }

  @Test
  void testBppTimeout() {
    when(bppService.userData(any())).thenThrow(new RuntimeException(new SocketTimeoutException()));

    Try<UserDataResponse> userData = bppComponent.fetchUserData("123");

    assertThat(userData.isFailure()).isTrue();

    userData.onFailure(e -> assertThat(e).isInstanceOf(BppComponent.BppTimeoutException.class));
  }

  @Test
  void checkNpe() {
    when(bppService.userData(any())).thenReturn(new GeneralResponse<>(null, null));

    Try<UserDataResponse> userData = bppComponent.fetchUserData(null);

    assertThat(userData.isFailure()).isTrue();
    assertThat(userData.getCause()).isInstanceOf(IllegalArgumentException.class);
  }
}
