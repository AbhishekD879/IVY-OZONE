package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.CouponMarketMappingEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.CouponMarketMappingRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import com.ladbrokescoral.oxygen.cms.api.service.CouponMarketMappingService;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

/** @author PBalarangakumar 20-02-2024 */
@WebMvcTest(
    value = {
      CouponMarketMappingController.class,
      CouponMarketMappingService.class,
      CouponMarketMappingEntity.class,
      CouponMarketMappingRepository.class
    })
@MockBean(BrandService.class)
@MockBean(ModelMapper.class)
@AutoConfigureMockMvc(addFilters = false)
public class CouponMarketMappingControllerTest extends AbstractControllerTest {

  private CouponMarketMappingEntity entity;
  @MockBean CouponMarketMappingRepository repository;

  @Before
  public void init() {
    entity = new CouponMarketMappingEntity();
    entity.setCouponId("couponId");
    entity.setMarketName("marketName");
    entity.setBrand("bma");
    entity.setId("123456");
    List<CouponMarketMappingEntity> entities = new ArrayList<>();
    entities.add(entity);
    when(repository.save(any())).thenReturn(entity);
    when(repository.findByBrand(any())).thenReturn(entities);
  }

  @Test
  public void testCreate() throws Exception {
    when(repository.findByCouponId(any())).thenReturn(Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/coupon-market-mapping")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateWithDuplicate() throws Exception {
    when(repository.findByCouponId(any())).thenReturn(Optional.of(entity));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/coupon-market-mapping")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdate() throws Exception {
    when(repository.findById(any())).thenReturn(Optional.of(entity));
    when(repository.findByCouponId(any())).thenReturn(Optional.empty());

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/coupon-market-mapping/123456")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateWithSameCouponId() throws Exception {
    when(repository.findById(any())).thenReturn(Optional.of(entity));
    when(repository.findOne(any())).thenReturn(Optional.of(entity));
    when(repository.findByCouponId(any())).thenReturn(Optional.of(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/coupon-market-mapping/12345")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(entity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateWithDiffRentCouponId() throws Exception {
    CouponMarketMappingEntity couponEntity = new CouponMarketMappingEntity();
    couponEntity.setCouponId("couponId2");
    couponEntity.setMarketName("marketName");
    couponEntity.setBrand("bma");
    couponEntity.setId("123456");
    when(repository.findById(any())).thenReturn(Optional.of(entity));
    when(repository.findByCouponId(any())).thenReturn(Optional.of(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/coupon-market-mapping/123456")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(couponEntity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testUpdateWithDiffRentCouponId2() throws Exception {
    CouponMarketMappingEntity couponEntity = new CouponMarketMappingEntity();
    couponEntity.setCouponId("couponId2");
    couponEntity.setMarketName("marketName");
    couponEntity.setBrand("bma");
    couponEntity.setId("1234567");
    when(repository.findById(any())).thenReturn(Optional.of(entity));
    when(repository.findByCouponId(any())).thenReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/coupon-market-mapping/123456")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(couponEntity)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateWithIdNotFound() throws Exception {
    CouponMarketMappingEntity couponEntity = new CouponMarketMappingEntity();
    couponEntity.setCouponId("couponId2");
    couponEntity.setMarketName("marketName");
    couponEntity.setBrand("bma");
    couponEntity.setId("123456");

    when(repository.findOne(any())).thenReturn(Optional.empty());
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/coupon-market-mapping/123456")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(couponEntity)))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testGetById() throws Exception {
    when(repository.findById(any())).thenReturn(Optional.of(entity));

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/coupon-market-mapping/123456")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testGetByBrand() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/coupon-market-mapping/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteById() throws Exception {

    when(repository.findById(any())).thenReturn(Optional.of(entity));
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/coupon-market-mapping/123456")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }
}
