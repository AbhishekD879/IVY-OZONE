package com.egalacoral.spark.timeform.api;

import com.egalacoral.spark.timeform.api.connectivity.*;
import com.egalacoral.spark.timeform.api.services.AuthenticationService;
import com.egalacoral.spark.timeform.api.services.DataService;
import com.egalacoral.spark.timeform.api.services.ImageService;
import com.egalacoral.spark.timeform.model.internal.TokenData;
import java.util.HashMap;
import java.util.Map;
import okhttp3.Interceptor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class TimeFormAPIImpl implements TimeFormAPI {

  private static final transient Logger LOGGER = LoggerFactory.getLogger(TimeFormAPI.class);

  private static final String SLASH = "/";

  private final TimeFormContext context;

  private final AuthenticationService authenticationService;

  private RequestPerformer simpleRequestPerformer;

  private RequestPerformer requestPerformer;

  private String userName;

  private String password;

  private TimeFormService timeFormService;

  public TimeFormAPIImpl(
      String loginUrl,
      String dataUrl,
      String grUrlSuffix,
      String hrUrlSuffix,
      String imageUrl,
      TimeProvider timeProvider,
      FailOverStrategy failOverStrategy,
      Interceptor interceptor) {
    context =
        new TimeFormContext(
            addSlash(loginUrl), addSlash(dataUrl), grUrlSuffix, hrUrlSuffix, imageUrl);
    context.setInterceptor(interceptor);
    simpleRequestPerformer = new SimpleRequestPerformer();
    Map<Long, Integer> timeLimits = new HashMap<>();
    timeLimits.put(1000L * 60 * 60, 3000);
    timeLimits.put(1000L, 1);
    requestPerformer =
        new TimeLimitRequestPerformer(simpleRequestPerformer, timeProvider, timeLimits);
    requestPerformer =
        new FailOverRequestPerformer(requestPerformer, failOverStrategy, this::internalLogin);
    context.setRequestPerformer(requestPerformer);
    authenticationService = new AuthenticationService(context);
  }

  private static String addSlash(String url) {
    if (!url.endsWith(SLASH)) {
      url = url + SLASH;
    }
    return url;
  }

  private void internalLogin() {
    TokenData sessionToken =
        simpleRequestPerformer.invokeSync(
            authenticationService.getSessionToken(userName, password));
    LOGGER.info("Success login. {}", sessionToken);
    context.setTokenData(sessionToken);
  }

  /**
   * Login into timeform system
   *
   * @return instance of TimeFormService class which should be used for data retrivement
   */
  @Override
  public synchronized TimeFormService login(String userName, String password) {
    this.userName = userName;
    this.password = password;
    context.setUserName(userName);
    try {
      internalLogin();
    } catch (Exception e) {
      LOGGER.error("login failed", e);
      TokenData tokenData = new TokenData();
      tokenData.setAccessToken("");
      context.setTokenData(tokenData);
    }
    if (timeFormService == null) {
      timeFormService =
          new TimeFormServiceImpl(
              new DataService(context), new ImageService(context, simpleRequestPerformer));
    }
    return timeFormService;
  }
}
