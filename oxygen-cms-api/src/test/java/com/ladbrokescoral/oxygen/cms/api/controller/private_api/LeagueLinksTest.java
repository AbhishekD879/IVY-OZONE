package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.LeagueLinkDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LeagueLink;
import com.ladbrokescoral.oxygen.cms.api.entity.Name;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.entity.UserStatus;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.beans.BeanUtils;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

@RunWith(MockitoJUnitRunner.Silent.class)
public class LeagueLinksTest {

  @Mock private CrudService<LeagueLink> crudService;

  @InjectMocks LeagueLinks leagueLinks;

  private LeagueLink leagueLink = new LeagueLink();
  private LeagueLinkDto leagueLinkDto;
  private User user;

  @Before
  public void init() throws IOException {
    user =
        User.builder()
            .email("test@test.com")
            .admin(false)
            .status(UserStatus.ACTIVE)
            .password("12345")
            .name(new Name("F", "L"))
            .build();
    UserService userService = mock(UserService.class);
    leagueLinks.setUserService(userService);
    leagueLinkDto =
        TestUtil.deserializeWithJackson(
            "controller/private_api/leagueLink.json", LeagueLinkDto.class);
    BeanUtils.copyProperties(leagueLinkDto, leagueLink);
    when(userService.findOne(anyString())).thenReturn(Optional.of(user));
  }

  @Test
  public void testToCreateLeagueLink() {
    when(crudService.save(any(LeagueLink.class))).thenReturn(leagueLink);
    when(crudService.prepareModelBeforeSave(any(LeagueLink.class))).thenReturn(leagueLink);
    ResponseEntity<LeagueLink> response = this.leagueLinks.create(leagueLinkDto);
    Assert.assertNotNull(response);
    Assert.assertEquals(leagueLink, response.getBody());
  }

  @Test
  public void testToUpdateLeagueLink() {
    when(crudService.save(any(LeagueLink.class))).thenReturn(leagueLink);
    when(crudService.prepareModelBeforeSave(any(LeagueLink.class))).thenReturn(leagueLink);
    when(crudService.findOne(anyString())).thenReturn(Optional.of(leagueLink));
    when(crudService.update(any(), any())).thenReturn(leagueLink);
    LeagueLink response = this.leagueLinks.update("123", leagueLinkDto);
    Assert.assertNotNull(response);
    Assert.assertEquals(leagueLink, response);
  }

  @Test
  public void testToReadLeagueLink() {
    when(crudService.findOne(anyString())).thenReturn(Optional.of(leagueLink));
    LeagueLink response = this.leagueLinks.read("123");
    Assert.assertNotNull(response);
    Assert.assertEquals(leagueLink, response);
  }

  @Test
  public void testToReadByBrandLeagueLink() {
    List<LeagueLink> list = new ArrayList<>();
    list.add(leagueLink);
    when(crudService.findByBrand(anyString())).thenReturn(list);
    List<LeagueLink> response = this.leagueLinks.readByBrand("bma");
    Assert.assertNotNull(response);
    Assert.assertEquals(list, response);
  }

  @Test
  public void testToDeleteLeagueLink() {
    when(crudService.findOne(anyString())).thenReturn(Optional.of(leagueLink));
    ResponseEntity<LeagueLink> response = this.leagueLinks.delete("123");
    Assert.assertNotNull(response);
    Assert.assertEquals(HttpStatus.NO_CONTENT, response.getStatusCode());
  }
}
