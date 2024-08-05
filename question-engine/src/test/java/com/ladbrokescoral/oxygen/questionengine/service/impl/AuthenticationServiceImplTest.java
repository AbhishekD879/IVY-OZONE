package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.ladbrokescoral.oxygen.questionengine.model.bpp.BppTokenRequest;
import com.ladbrokescoral.oxygen.questionengine.model.bpp.UserData;
import com.ladbrokescoral.oxygen.questionengine.exception.InvalidBppTokenException;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bpp.BppService;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

import javax.servlet.http.HttpServletRequest;

import static org.mockito.Mockito.when;

@RunWith(MockitoJUnitRunner.class)
public class AuthenticationServiceImplTest {

  @Mock
  private BppService bppService;

  @Mock
  private HttpServletRequest httpServletRequest;

  @InjectMocks
  private AuthenticationServiceImpl authenticationService;

  @Test
  public void verifyUserHappyPath() {
    when(httpServletRequest.getHeader(BppTokenRequest.TOKEN_PROPERTY_NAME)).thenReturn("token-value");
    when(bppService.findUserData(new BppTokenRequest().setToken("token-value"))).thenReturn(new UserData().setUsername("test-username"));

    authenticationService.verifyUser("test-username");
  }

  @Test(expected = InvalidBppTokenException.class)
  public void verifyUserWrongUsername() {
    when(httpServletRequest.getHeader(BppTokenRequest.TOKEN_PROPERTY_NAME)).thenReturn("token-value");
    when(bppService.findUserData(new BppTokenRequest().setToken("token-value"))).thenReturn(new UserData().setUsername("wrong-test-username"));

    authenticationService.verifyUser("test-username");
  }

  @Test(expected = InvalidBppTokenException.class)
  public void verifyUserEmptyUserData() {
    when(httpServletRequest.getHeader(BppTokenRequest.TOKEN_PROPERTY_NAME)).thenReturn("token-value");
    when(bppService.findUserData(new BppTokenRequest().setToken("token-value"))).thenReturn(null);

    authenticationService.verifyUser("test-username");
  }
}
