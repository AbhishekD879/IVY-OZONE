package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.SignPosting;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.repository.SignPostingRepository;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SignPostingServiceTest extends BDDMockito {

  @InjectMocks private SignPostingService signPostingService;
  @Mock private SignPostingRepository signPostingRepository;
  @Mock CrudService<User> userServiceObj;
  private SignPosting signPosting = createSignPosting();

  private SignPosting createSignPosting() {
    SignPosting signPosting = new SignPosting();
    signPosting.setId("616e7a3c54409d7519879827");
    signPosting.setBrand("ladbrokes");
    return signPosting;
  }

  @Before
  public void init() {

    signPostingService = new SignPostingService(signPostingRepository);
  }

  @Test
  public void testfindAll() {
    Assert.assertNotNull(signPostingService.findAll());
  }

  @Test
  public void testfindAllByBrand() {
    Assert.assertNotNull(signPostingService.findAllByBrand("ladbrokes"));
  }
}
