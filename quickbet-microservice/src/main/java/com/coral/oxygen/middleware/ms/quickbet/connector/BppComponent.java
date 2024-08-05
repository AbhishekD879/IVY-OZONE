package com.coral.oxygen.middleware.ms.quickbet.connector;

import com.coral.bpp.api.model.bet.api.request.UserDataDto;
import com.coral.bpp.api.model.bet.api.response.ErrorBody;
import com.coral.bpp.api.model.bet.api.response.GeneralResponse;
import com.coral.bpp.api.model.bet.api.response.UserDataResponse;
import com.coral.bpp.api.service.BppService;
import com.newrelic.api.agent.NewRelic;
import io.vavr.control.Try;
import java.net.SocketTimeoutException;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.util.Assert;

@Component
public class BppComponent {
  private final BppService bppService;

  @Autowired
  public BppComponent(BppService bppService) {
    this.bppService = bppService;
  }

  public Try<UserDataResponse> fetchUserData(String bppToken) {
    try {
      Assert.notNull(bppToken, "bppToken cannot be null");
      final GeneralResponse<UserDataResponse> generalResponse =
          bppService.userData(new UserDataDto(bppToken));
      final UserDataResponse userData = generalResponse.getBody();
      ErrorBody errorBody = generalResponse.getErrorBody();
      if (errorBody != null) {
        throw new BppErrorException("BPP returned error", errorBody);
      } else {
        if (userData == null || StringUtils.isBlank(userData.getOxiApiToken())) {
          throw new BppAuthException("No user data found for current user");
        }
        return Try.ofSupplier(() -> userData);
      }
    } catch (Exception e) {
      NewRelic.noticeError(e);
      if (e.getCause() instanceof SocketTimeoutException) {
        return Try.failure(new BppTimeoutException("BPP timed out", e.getCause()));
      }
      return Try.failure(e);
    }
  }

  public static class BppErrorException extends RuntimeException {
    private final transient ErrorBody errorBody;

    public BppErrorException(String message, ErrorBody errorBody) {
      super(message);
      this.errorBody = errorBody;
    }

    public ErrorBody getErrorBody() {
      return errorBody;
    }
  }

  public static class BppAuthException extends RuntimeException {
    public BppAuthException(String message) {
      super(message);
    }
  }

  public static class BppTimeoutException extends RuntimeException {
    public BppTimeoutException(String message, Throwable cause) {
      super(message, cause);
    }
  }
}
