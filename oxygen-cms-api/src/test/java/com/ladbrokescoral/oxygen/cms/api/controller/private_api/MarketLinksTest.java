package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.MarketLinkDto;
import com.ladbrokescoral.oxygen.cms.api.entity.MarketLink;
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
public class MarketLinksTest {

  @Mock private CrudService<MarketLink> crudService;

  @InjectMocks MarketLinks marketLinks;

  private MarketLink marketLink = new MarketLink();
  private MarketLinkDto marketLinkDto;
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
    marketLinks.setUserService(userService);
    marketLinkDto =
        TestUtil.deserializeWithJackson(
            "controller/private_api/marketLink.json", MarketLinkDto.class);
    BeanUtils.copyProperties(marketLinkDto, marketLink);
    when(userService.findOne(anyString())).thenReturn(Optional.of(user));
  }

  @Test
  public void testToCreateMarketLink() {
    when(crudService.save(any(MarketLink.class))).thenReturn(marketLink);
    when(crudService.prepareModelBeforeSave(any(MarketLink.class))).thenReturn(marketLink);
    ResponseEntity<MarketLink> response = this.marketLinks.create(marketLinkDto);
    Assert.assertNotNull(response);
    Assert.assertEquals(marketLink, response.getBody());
  }

  @Test
  public void testToUpdateMarketLink() {
    when(crudService.save(any(MarketLink.class))).thenReturn(marketLink);
    when(crudService.prepareModelBeforeSave(any(MarketLink.class))).thenReturn(marketLink);
    when(crudService.findOne(anyString())).thenReturn(Optional.of(marketLink));
    when(crudService.update(any(), any())).thenReturn(marketLink);
    MarketLink response = this.marketLinks.update("123", marketLinkDto);
    Assert.assertNotNull(response);
    Assert.assertEquals(marketLink, response);
  }

  @Test
  public void testToReadMarketLink() {
    when(crudService.findOne(anyString())).thenReturn(Optional.of(marketLink));
    MarketLink response = this.marketLinks.read("123");
    Assert.assertNotNull(response);
    Assert.assertEquals(marketLink, response);
  }

  @Test
  public void testToReadByBrandMarketLink() {
    List<MarketLink> list = new ArrayList<>();
    list.add(marketLink);
    when(crudService.findByBrand(anyString())).thenReturn(list);
    List<MarketLink> response = this.marketLinks.readByBrand("bma");
    Assert.assertNotNull(response);
    Assert.assertEquals(list, response);
  }

  @Test
  public void testToDeleteMarketLink() {
    when(crudService.findOne(anyString())).thenReturn(Optional.of(marketLink));
    ResponseEntity<MarketLink> response = this.marketLinks.delete("123");
    Assert.assertNotNull(response);
    Assert.assertEquals(HttpStatus.NO_CONTENT, response.getStatusCode());
  }
}
