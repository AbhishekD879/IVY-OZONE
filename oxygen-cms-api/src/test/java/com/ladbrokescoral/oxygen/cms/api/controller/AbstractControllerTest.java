package com.ladbrokescoral.oxygen.cms.api.controller;

import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import org.junit.After;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

// FIXME: migrate to Configuration. Use @Import.
@ActiveProfiles("UNIT")
@RunWith(SpringRunner.class)
// @WebMvcTest({
//       Controller.class,
//       Service.class,
//     })
// @AutoConfigureMockMvc(addFilters = false)
// @MockBean(AnotherService.class)
public abstract class AbstractControllerTest extends BDDMockito {

  @Autowired protected MockMvc mockMvc;

  // FIXME: remove from fields, put into MockBeans somehow
  // Global Beans, can be used. Set to protected
  @MockBean private AuthenticationService authenticationService;
  @MockBean private UserService userService;

  @Before
  public void init() throws Exception {

    // given(repository.findById(anyString())).willReturn(Optional.of(entity));
    // given(repository.save(any(Class.class))).will(AdditionalAnswers.returnsFirstArg());

  }

  @After
  public void verify() {

    // verifyNoMoreInteractions(repository);

  }
}
