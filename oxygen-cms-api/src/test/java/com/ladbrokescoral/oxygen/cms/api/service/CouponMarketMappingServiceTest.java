package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.CouponMarketMappingDto;
import com.ladbrokescoral.oxygen.cms.api.entity.CouponMarketMappingEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.CouponMarketMappingRepository;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;

/** @author PBalarangakumar 21-02-2024 */
@RunWith(MockitoJUnitRunner.class)
public class CouponMarketMappingServiceTest {

  @Mock private CouponMarketMappingRepository repository;
  @Mock private ModelMapper modelMapper;
  CouponMarketMappingService service;

  @Before
  public void setUp() {
    service = new CouponMarketMappingService(repository, modelMapper);
  }

  @Test
  public void testFindByCouponId() {

    final CouponMarketMappingEntity entity = getEntity();

    when(repository.findByCouponId("couponId")).thenReturn(Optional.of(entity));

    final Optional<CouponMarketMappingEntity> dbEntity = service.findByCouponId("couponId");

    assertTrue(dbEntity.isPresent());
    assertEquals(dbEntity.get().getCouponId(), entity.getCouponId());
  }

  @Test
  public void testFindByBrandDto() {

    final CouponMarketMappingEntity entity = getEntity();
    ArrayList<CouponMarketMappingEntity> entities = new ArrayList<>();
    entities.add(entity);

    when(repository.findByBrand("bma")).thenReturn(entities);

    final List<CouponMarketMappingDto> dbEntity = service.findByBrandDto("bma");

    assertEquals(1, dbEntity.size());
  }

  private CouponMarketMappingEntity getEntity() {

    final CouponMarketMappingEntity entity = new CouponMarketMappingEntity();
    entity.setCouponId("couponId");
    entity.setMarketName("marketName");
    entity.setBrand("bma");
    entity.setId("123456");

    return entity;
  }
}
